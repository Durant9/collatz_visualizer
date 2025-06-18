import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from collatz_utils import plot_limits, next_sequence_points
from math import pi
import imageio
import tempfile
import os

# Parsing angles in the form 'pi/2'
def parse_angle(expr):
    try:
        return eval(expr, {"pi": pi, "np": np, "__builtins__": {}})
    except:
        st.error(f"Angolo non valido: '{expr}'")
        return None

def render_frame(fig):
    fig.canvas.draw()
    buf = fig.canvas.buffer_rgba()
    ncols, nrows = fig.canvas.get_width_height()
    frame = np.frombuffer(buf, dtype=np.uint8).reshape(nrows, ncols, 4)
    return frame[:, :, :3]

st.set_page_config(layout="wide")
st.title("Collatz Conjecture Visualizer")

# Sidebar - parameters
with st.sidebar:
    st.header("Parameters")
    n = st.number_input("N", min_value=2, max_value=1000, value=50)
    theta_str = st.text_input("Theta", value="pi/30")
    start_angle_str = st.text_input("Starting angle", value="pi/2")
    line_width = st.number_input("Line width", min_value=0.1, max_value=2.01, value=0.5, step=0.1)
    alpha = st.number_input("Transparency (0-1)", min_value=0.0, max_value=1.01, value=0.7, step=0.05)
    fps = st.number_input("Video FPS", min_value=1, max_value=61, value=10, step=1)
    color = st.color_picker("Color", "#FFFF00")

if st.button("Generate"):
    theta = parse_angle(theta_str)
    start_angle = parse_angle(start_angle_str)

    if theta is None or start_angle is None:
        st.stop()

    starts = list(range(2, n))

    xlim, ylim = plot_limits(starts=starts, theta=theta, start_angle=start_angle)
    start_points = [(0, 0) for _ in starts]

    fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
    ax.set_facecolor('black')
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect('equal')
    plt.axis('off')
    plt.plot(0, 0, '.', color=color, markersize=8, alpha=alpha)

    segments = np.array([1 if x != 1 else 0 for x in starts])
    angles = np.full(len(starts), start_angle)
    angles += np.where(np.array(starts) % 2 == 0, -theta, theta)
    new_numbers = next_sequence_points(starts)

    while any(n != 1 for n in new_numbers):
        new_points = [(x + l * np.cos(a), y + l * np.sin(a))
                      for (x, y), l, a in zip(start_points, segments, angles)]

        for (x0, y0), (x1, y1) in zip(start_points, new_points):
            plt.plot([x0, x1], [y0, y1], '-', color=color, alpha=alpha, linewidth=line_width)

        new_numbers = next_sequence_points(new_numbers)
        start_points = new_points
        segments = [1 if n != 1 else 0 for n in new_numbers]
        angles += np.where(np.array(new_numbers) % 2 == 0, -theta, theta)

    st.pyplot(fig)

animate = st.button("Animate")
if animate:
    theta = parse_angle(theta_str)
    start_angle = parse_angle(start_angle_str)
    if theta is None or start_angle is None:
        st.stop()

    starts = list(range(2, n))
    xlim, ylim = plot_limits(starts=starts, theta=theta, start_angle=start_angle)
    start_points = [(0, 0) for _ in starts]

    segments = np.array([1 if x != 1 else 0 for x in starts])
    angles = np.full(len(starts), start_angle)
    angles += np.where(np.array(starts) % 2 == 0, -theta, theta)
    new_numbers = next_sequence_points(starts)

    fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
    ax.set_facecolor('black')
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect('equal')
    plt.axis('off')
    plt.plot(0, 0, '.', color=color, markersize=8, alpha=alpha)

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmpfile:
        tmpfile_path = tmpfile.name
    writer = imageio.get_writer(tmpfile_path, mode='I', fps=10, format="ffmpeg", codec="libx264")

    steps = 0
    while any(n != 1 for n in new_numbers):
        new_points = [(x + l * np.cos(a), y + l * np.sin(a))
                      for (x, y), l, a in zip(start_points, segments, angles)]

        for (x0, y0), (x1, y1) in zip(start_points, new_points):
            plt.plot([x0, x1], [y0, y1], '-', color=color, alpha=alpha, linewidth=line_width)

        if steps % 2 == 0:
            frame = render_frame(fig)
            writer.append_data(frame)

        new_numbers = next_sequence_points(new_numbers)
        start_points = new_points
        segments = [1 if n != 1 else 0 for n in new_numbers]
        angles += np.where(np.array(new_numbers) % 2 == 0, -theta, theta)

        steps += 1

    writer.close()
    with open(tmpfile_path, 'rb') as f:
        video_bytes = f.read()
    os.remove(tmpfile_path)
    st.video(video_bytes)

    st.success("Animation completed")
