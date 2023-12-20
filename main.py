import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import streamlit as st
import streamlit.components.v1 as components
from compute_trajectory import compute_trajectory
from functools import partial

matplotlib.rcParams['animation.embed_limit'] = 2 ** 30

fig, ax = plt.subplots()
plt.title('Foucault Pendulum Path')
plt.xlabel('x position')
plt.ylabel('y position')
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect('equal', 'box')
line, = ax.plot([], [], lw=2)

def animate(t, lat, length, T, g, omega):
    x, y = compute_trajectory(lat, length, t, T, g, omega)
    line.set_data(x, y)
    return line,

planets = {
    "Mercury": (3.7, 1.24e-6),
    "Venus": (8.87, -2.992e-7),
    "Earth": (9.81, 7.292e-5),
    "Mars": (3.71, 7.088e-5),
    "Jupiter": (24.79, 1.758e-4),
    "Saturn": (10.44, 1.653e-4),
    "Uranus": (8.87, -1.012e-4),
    "Neptune": (11.15, 1.083e-4),
    "Custom": (None, None),
}

planet = st.selectbox("Choose a planet", list(planets.keys()), index=None, placeholder="Choose a planet")

if planet is not None:
    g, omega = planets[planet]
else:
    g, omega = None, None

if planet == "Custom":
    g = st.number_input("Enter g", value=None)
    omega = st.number_input("Enter omega [10^-4 rad/s]", value=None, format="%.8f") * 1e-4

if None not in (g, omega) and planet != "Custom":
    st.text(f"Chosen g: {g}m/s^2")
    st.text(f"Chosen rotational velocity: {omega}rad/s")

lat = st.slider("Enter latitude", min_value=-89.9, max_value=89.9, format="%.2f")
length = st.number_input("Enter length [m]", value=None, format="%.7f")
framerate = st.number_input("Enter framerate", value=30, max_value=60, min_value=1, format="%d")

T = np.arange(0, 200, 10 / framerate)

if None not in (g, omega, lat, length):
    ani = FuncAnimation(fig, partial(animate, lat=lat, length=length, T=T, g=g, omega=omega), frames=len(T), blit=True, interval=1000/framerate)
    st.title("Foucault Pendulum Path")
    components.html(ani.to_jshtml(), height=1000, width=1000)