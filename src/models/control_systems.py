from functools import cached_property
import numpy as np

from pydantic import BaseModel, model_validator
import control as ct


__all__ = ("TransferMatrix",)


class TransferMatrix(BaseModel):
    numerator_coefficients: list[list[list[float]]]
    denominator_coefficients: list[list[list[float]]]
    delay: list[list[float]]
    pade_order: int = 10

    @cached_property
    def num_rows(self) -> int:
        return len(self.numerator_coefficients)

    @cached_property
    def num_cols(self):
        return len(self.denominator_coefficients)

    @model_validator(mode="after")
    def validate_matrix(self) -> "TransferMatrix":
        if len(self.denominator_coefficients) != self.num_rows:
            raise ValueError(
                f"Expected denominator coefficients to have {self.num_rows} rows, "
                f"found {len(self.denominator_coefficients)}"
            )
        if len(self.denominator_coefficients[0]) != self.num_cols:
            raise ValueError(
                f"Expected denominator coefficients to have {self.num_rows} rows, "
                f"found {len(self.denominator_coefficients[0])}"
            )
        if len(self.delay) != self.num_rows:
            raise ValueError(
                f"Expected delay coefficients to have {self.num_rows} rows, "
                f"found {len(self.delay)}"
            )
        if len(self.delay[0]) != self.num_cols:
            raise ValueError(
                f"Expected delay coefficients to have {self.num_rows} rows, "
                f"found {len(self.delay[0])}"
            )

        if self.pade_order < 0:
            raise ValueError("Pade approximation order must be positive or 0")

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                delay = self.delay[i][j]
                if delay < 0:
                    raise ValueError(f"Delay at [{i}, {j}] is negative")
                if len(self.numerator_coefficients[i][j]) >= len(
                    self.denominator_coefficients[i][j]
                ):
                    raise ValueError(
                        f"The system is indeterminate: number of numerator coefficients at [{i}, {j}] "
                        f"({self.numerator_coefficients[i][j]}) is more than or equal to the number "
                        f"of denominator coefficients ({self.denominator_coefficients[i][j]})"
                    )
                if len(self.numerator_coefficients[i][j]) == 0:
                    raise ValueError(
                        f"The numerator coefficients at [{i}, {j}] are empty"
                    )
                if len(self.denominator_coefficients[i][j]) == 0:
                    raise ValueError(
                        f"The denominator coefficients at [{i}, {j}] are empty"
                    )
        return self

    def as_lti_system(self) -> ct.LTI:
        """
        Returns the transfer matrix as control.LTI linear time-invariant system
        """
        tf_numerator = []
        tf_denominator = []
        for i in range(self.num_rows):
            numerator_row = []
            denominator_row = []
            for j in range(self.num_cols):
                num_pade, den_pade = ct.pade(self.delay[i][j], n=self.pade_order)
                num = np.polymul(self.numerator_coefficients[i][j], num_pade)
                den = np.polymul(self.denominator_coefficients[i][j], den_pade)
                numerator_row.append(num)
                denominator_row.append(den)
            tf_numerator.append(numerator_row)
            tf_denominator.append(denominator_row)
        tf = ct.tf(tf_numerator, tf_denominator)
        return tf
