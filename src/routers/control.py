from functools import cached_property

from fastapi import APIRouter
import control.matlab as ctm
from pydantic import BaseModel, model_validator, Field

from src.models.control_systems import TransferMatrix
import numpy as np
from numpy import typing as npt

router = APIRouter()


class LsimRequest(BaseModel):
    transfer_matrix: TransferMatrix = Field()
    mv_history: list[list[float]] = Field()
    observation_time: list[float] = Field()

    @cached_property
    def mv_history_array(self) -> npt.NDArray[np.float32]:
        return np.array(self.mv_history)

    @cached_property
    def observation_time_array(self) -> npt.NDArray[np.float32]:
        return np.array(self.observation_time)

    @model_validator(mode="after")
    def validate_request(self):
        history = self.mv_history_array
        num_observations, num_mvs = history.shape
        if num_mvs != self.transfer_matrix.num_cols:
            raise ValueError(
                f"Expected {self.transfer_matrix.num_cols} columns, but found {num_mvs}"
            )
        if len(self.observation_time_array) != num_observations:
            raise ValueError(
                f"Expected {num_observations} points to be passed in observation_time, "
                f"found {len(self.observation_time_array)}"
            )
        return self


class LsimResponse(BaseModel):
    cv_values: list[list[float]]
    T: list[float]
    state: list[list[float]]


@router.post("/lsim")
def lsim(request: LsimRequest):
    lsim_response: tuple[
        npt.NDArray[np.float32], npt.NDArray[np.float32], npt.NDArray[np.float32]
    ] = ctm.lsim(
        sys=request.transfer_matrix.as_lti_system(),
        U=request.mv_history_array,
        T=request.observation_time_array,
    )

    y_out, T, x_out = lsim_response

    return LsimResponse(cv_values=y_out.tolist(), T=T.tolist(), state=x_out.tolist())
