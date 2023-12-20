import numpy as np


def compute_trajectory(
    lat_degrees: float,
    length: float,
    t: int,
    time_frames: np.ndarray,
    g: float,
    omega: float,
) -> (float, float):
    """
    Computes the trajectory of the Foucault pendulum.

    :param lamda: Latitude where the pendulum is located.
    :param length: Length of the pendulum.
    :param t: Index of the current point in time.
    :param T: Array of time points at which to compute the pendulum's position.
    :param g: Acceleration due to gravity.
    :param omega: Angular velocity of the planet's rotation.
    :return: Arrays of x and y coordinates of the pendulum's position until the current point in time.
    """
    # Frequency of the pendulum's oscillation
    freq = np.sqrt(g / length)

    lat = lat_degrees * np.pi / 180
    omega = omega * 10**3

    # Compute x and y coordinates
    x = np.cos(freq * time_frames[:t] - omega * np.sin(lat) * time_frames[:t]) + np.cos(
        freq * time_frames[:t] + omega * np.sin(lat) * time_frames[:t]
    )
    y = np.sin(freq * time_frames[:t] - omega * np.sin(lat) * time_frames[:t]) - np.sin(
        freq * time_frames[:t] + omega * np.sin(lat) * time_frames[:t]
    )

    return x, y
