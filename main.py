import ast
from functools import partial

import clipboard
import folium
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import streamlit as st
import streamlit.components.v1 as components
from streamlit_folium import folium_static

from compute_trajectory import compute_trajectory


matplotlib.rcParams["animation.embed_limit"] = 2**30

fig, ax = plt.subplots()
plt.title("Foucault Pendulum Path")
plt.xlabel("x position")
plt.ylabel("y position")
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect("equal", "box")
(line,) = ax.plot([], [], lw=2)


def animate(t, lat, length, T, g, omega):
    x, y = compute_trajectory(lat, length, t, T, g, omega)
    line.set_data(x, y)
    line.set_color("#FF4B4B")
    return (line,)


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

st.set_page_config(page_title="Focault Pendulum", page_icon=":cyclone:")

if "planet" not in st.session_state:
    st.session_state["planet"] = None
    st.session_state["g"] = None
    st.session_state["omega"] = None
    st.session_state["lat"] = None
    st.session_state["length"] = None
    st.session_state["framerate"] = None
    st.session_state["simulation_length"] = None
    st.session_state["lat"] = None
    st.session_state["location"] = [52.237, 21.017]

st.sidebar.title("Configure Simulation")

with st.sidebar:
    planet = st.selectbox(
        "Choose a Planet",
        list(planets.keys()),
        index=2,
        placeholder="Choose a planet",
    )

    if planet is not None:
        g, omega = planets[planet]
        st.session_state["planet"] = planet
        st.session_state["g"] = g
        st.session_state["omega"] = omega
    else:
        g, omega = None, None
        st.session_state["planet"] = None
        st.session_state["g"] = None
        st.session_state["omega"] = None

    if planet == "Custom":
        g = st.number_input("Enter g:", value=None)
        st.session_state["g"] = g

    if g is not None:
        st.text(f"Chosen Gravitational Acceleration: {g}m/s^2")

    if planet == "Custom":
        omega = st.number_input("Enter Omega [10^-4 rad/s]:", value=None, format="%.8f")
        if omega is not None:
            omega *= 1e-4
        st.session_state["omega"] = omega

    if omega is not None:
        st.text(f"Chosen Rotational Velocity: {omega}rad/s")

    if planet == "Earth":
        m = folium.Map(
            location=st.session_state["location"],
            zoom_start=5,
            tiles="cartodb positron",
        )
        folium.ClickForMarker().add_to(m)
        folium.ClickForLatLng(
            format_str='"[" + lat + "," + lng + "]"', alert=False
        ).add_to(m)
        folium_static(m)
        if st.button("Use Selected Location"):
            location = ast.literal_eval(clipboard.paste())
            st.session_state["location"] = location
            lat, _ = location
            st.session_state["lat"] = lat
            st.rerun()
        if st.session_state['lat']:
            st.text(f"Chosen Latitude: {st.session_state['lat']}")
    else:
        lat = st.slider("Pick Latitude", min_value=-89.9, max_value=89.9, format="%.2f")
        st.session_state["lat"] = lat

    length = st.number_input(
        "Enter Pendulum Length [m]", value=67.0, format="%.2f", min_value=0.0
    )
    st.session_state["length"] = length

    framerate = st.number_input(
        "Enter Simulation Framerate", value=30, max_value=60, min_value=1, format="%d"
    )
    st.session_state["framerate"] = framerate

    simulation_length = st.number_input(
        "Enter Simulation Length", value=200, max_value=600, min_value=1, format="%d"
    )
    st.session_state["simulation_length"] = simulation_length

    start = st.button("Start Animation")

st.title("Foucault Pendulum Path Simulation")
if start:
    simulation_length = st.session_state["simulation_length"]
    framerate = st.session_state["framerate"]
    T = np.arange(0, simulation_length, 10 / framerate)
    g = st.session_state["g"]
    omega = st.session_state["omega"]
    lat = st.session_state["lat"]
    length = st.session_state["length"]
    if None not in (g, omega, lat, length):
        ani = FuncAnimation(
            fig,
            partial(animate, lat=lat, length=length, T=T, g=g, omega=omega),
            frames=len(T),
            blit=True,
            interval=1000 / framerate,
        )
        with st.spinner("Rendering the Animation..."):
            rendered_ani = ani.to_jshtml()
        components.html(rendered_ani, height=600, width=600)
    else:
        st.error("Please fill in all fields")
