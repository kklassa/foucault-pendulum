import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def compute_trajectory(
        lat: float, 
        length: float,
        t: int,
        time_frames: np.ndarray,
        g: float = 3.7,
        omega: float = 7.088e-5 * 10 ** 3, 
    ) -> (float, float):
    """
    Computes the trajectory of the Foucault pendulum.

    :param lamda: Latitude where the pendulum is located.
    :param length: Length of the pendulum.
    :param t: Index of the current point in time.
    :param T: Array of time points at which to compute the pendulum's position.
    :param g: Acceleration due to gravity.
    :param omega: Angular velocity of the planet's rotation. (7.2921e-5)
    :return: Arrays of x and y coordinates of the pendulum's position until the current point in time.
    """
    # Frequency of the pendulum's oscillation
    freq = np.sqrt(g / length)

    # Compute x and y coordinates
    x = (
        np.cos(freq * time_frames[:t] - omega * np.sin(lat) * time_frames[:t]) +
        np.cos(freq * time_frames[:t] + omega * np.sin(lat) * time_frames[:t])
    )
    y = (
        np.sin(freq * time_frames[:t] - omega * np.sin(lat) * time_frames[:t]) -
        np.sin(freq * time_frames[:t] + omega * np.sin(lat) * time_frames[:t])
    )

    return x, y

fig, ax = plt.subplots()
plt.title('Foucault Pendulum Path')
plt.xlabel('x position')
plt.ylabel('y position')
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect('equal', 'box')
line, = ax.plot([], [], lw=2)

lat = 0.9 * np.pi
length = 150

g_earth = 9.81
g_mars = 3.7
omega_earth = 7.2921e-5
omega_mars = 7.088e-5

T = np.arange(0, 200, 0.5)

def animate(t):
    x, y = compute_trajectory(lat, length, t, T)
    line.set_data(x, y)
    return line,

ani = FuncAnimation(fig, animate, frames=len(T), blit=True, interval=50)
plt.show()