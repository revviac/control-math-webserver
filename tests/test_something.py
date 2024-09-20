import numpy as np
import pytest

from src.models.control_systems import TransferMatrix

from src.routers.control import LsimRequest


@pytest.fixture
def gain() -> list[list[float]]:
    return [
        [-0.45, 0, 0, 0, 0.05, 0],
        [0, 3, 0, 0, 0, -0.03],
        [0, -0.8, -0.1, 0, 0, 0.08],
        [0, 0, 0, -15, 0, 0],
        [0, -0.2, 0, 0, 0, 0.02],
        [0, 0, 0, -2.5, 0, 0],
    ]


@pytest.fixture
def tau() -> list[list[float]]:
    return [
        [7, 1, 1, 1, 7, 1],
        [1, 9, 1, 1, 1, 9],
        [1, 7, 12, 1, 1, 7],
        [1, 1, 1, 10, 1, 1],
        [1, 12, 1, 1, 1, 12],
        [1, 1, 1, 8, 1, 1],
    ]


@pytest.fixture
def delay() -> list[list[float]]:
    return [
        [6, 0, 0, 0, 6, 0],
        [0, 3, 0, 0, 0, 3],
        [0, 1, 3, 0, 0, 1],
        [0, 0, 0, 1, 0, 0],
        [0, 4, 0, 0, 0, 4],
        [0, 0, 0, 1, 0, 0],
    ]


@pytest.fixture
def numerator_coefficients(gain: list[list[float]]) -> list[list[list[float]]]:
    """
    [[k_ij]] -> [[[k_ij]]]
    """
    return [[[value] for value in row] for row in gain]


@pytest.fixture
def denominator_coefficients(tau: list[list[float]]) -> list[list[list[float]]]:
    """
    [[t_ij]] -> [[[t_ij, 1]]]
    """
    return [[[value, 1] for value in row] for row in tau]


@pytest.fixture
def transfer_matrix(
    numerator_coefficients: list[list[list[float]]],
    denominator_coefficients: list[list[list[float]]],
    delay: list[list[float]],
) -> TransferMatrix:
    return TransferMatrix(
        numerator_coefficients=numerator_coefficients,
        denominator_coefficients=denominator_coefficients,
        delay=delay,
    )


def test_able_to_create_lti(transfer_matrix: TransferMatrix):
    lti = transfer_matrix.as_lti_system()  # noqa
    pass


def test_get_request(transfer_matrix: TransferMatrix):
    N = 121
    mv_history = np.zeros(shape=(N, 6))
    mv_history[:, :4] = [145, 44, 860, 83.5]
    T = np.linspace(0, N - 1, num=N)

    request = LsimRequest(
        transfer_matrix=transfer_matrix,
        mv_history=mv_history.tolist(),
        observation_time=T.tolist(),
    )

    request_json = request.model_dump_json()  # noqa
    pass
