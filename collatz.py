import argparse
import yaml
from pathlib import Path
import collatz_utils as utils
from sympy import sympify
import os
import matplotlib.pyplot as plt
import cv2
import numpy as np

def load_config(config_path):
    # Loads yaml config file
    if config_path and Path(config_path).is_file():
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}

def parse_angle(value):
    # Properly reads angles
    if isinstance(value, (float, int)):
        return float(value)
    try:
        return float(sympify(value))
    except Exception as e:
        raise ValueError(f"Angolo non valido: '{value}'") from e

def parse_args():
    # Parses arguments from CLI
    parser = argparse.ArgumentParser(description="Visualizzazione congettura di Collatz")
    parser.add_argument('--config', type=str, help='path to config file', default='configs/config.yaml')
    parser.add_argument('--theta', type=float, help='bending angle')
    parser.add_argument('--start_angle', type=float, help='starting angle')
    parser.add_argument('--color', type=str, help='lines color (es: "#FFFF00")')
    parser.add_argument('--n', type=int, help='number of integers to plot')
    parser.add_argument('--line_width', type=float, help='width of the plot lines')
    parser.add_argument('--alpha', type=float, help='alpha of the plot lines')
    parser.add_argument('--save_video', type=bool, help='wether to save a video or not')
    parser.add_argument('--video_path', type=str, help='where to save the video file')
    parser.add_argument('--fps', type=int, help='fps of the video')
    parser.add_argument('--save_plot', type=bool, help='wether to save the final image')
    parser.add_argument('--show_plot', type=float, help='wether to show instantly the final image')
    parser.add_argument('--plot_path', type=float, help='where to save the plot file')
    args = parser.parse_args()
    return vars(args)

def normalize_params(params):
    # If needed, converts angles in config
    if 'theta' in params:
        params['theta'] = parse_angle(params['theta'])
    if 'start_angle' in params:
        params['start_angle'] = parse_angle(params['start_angle'])
    return params

def merge_config_and_args(yaml_config, cli_args):
    # Overrides yaml config value only if the CLI value is present
    return {**yaml_config, **{k: v for k, v in cli_args.items() if v is not None}}

def get_parameters():
    # Merges cli args with config args
    cli_args = parse_args()
    yaml_config = load_config(cli_args.get("config"))
    merged = merge_config_and_args(yaml_config, cli_args)
    return normalize_params(merged)


if __name__ == "__main__":
    # Get parameters
    config = get_parameters()

    # Start numbers
    starts = range(2, config['n'])

    # Directory making
    if config['save_video']:
        savedir = '/'.join(config['video_path'].split('/')[:-1])
        if not os.path.exists(savedir):
            os.makedirs(savedir)
        xlim, ylim = utils.plot_limits(starts = starts,
                                       theta = config['theta'],
                                       start_angle = config['start_angle'])
    if config['save_plot']:
        savedir = '/'.join(config['plot_path'].split('/')[:-1])
        if not os.path.exists(savedir):
            os.makedirs('/'.join(config['plot_path'].split('/')[:-1]))

    # Starting points and first frame
    start_points = [(0, 0) for _ in range(len(starts))]
    fig = plt.figure(figsize=(15, 15), facecolor='black')
    if config['save_video']:
        plt.xlim(xlim)
        plt.ylim(ylim)
    plt.axis('equal')
    plt.axis('off')
    if config['save_video']:
        plt.autoscale(False)
    plt.plot(0, 0, '.', color=config['color'], markersize=8, alpha=config['alpha'])
    if config['save_video']:
        firstFrame, ncols, nrows = utils.render_frame(fig)
        video = cv2.VideoWriter(config['video_path'], cv2.VideoWriter_fourcc(*'XVID'), config['fps'], (ncols, nrows))
        video.write(firstFrame)

    # Parameters to find next points in the plot
    segments = np.array([1 if n != 1 else 0 for n in starts])
    angles = np.full(len(starts), config['start_angle'])
    angles += np.where(np.array(starts) % 2 == 0, -config['theta'], config['theta'])
    new_numbers = utils.next_sequence_points(starts)

    # Loop until all numbers are 1
    while any(n != 1 for n in new_numbers):
        # Computing all new points for the plot
        new_points = [(x + l * np.cos(a), y + l * np.sin(a))
                      for (x, y), l, a in zip(start_points, segments, angles)]

        # Video/plot updating
        for (x0, y0), (x1, y1) in zip(start_points, new_points):
            plt.plot([x0, x1], [y0, y1], '-', color=config['color'], alpha=config['alpha'], linewidth=config['line_width'])
        if config['save_video']:
            frame, _, _ = utils.render_frame(fig)
            video.write(frame)

        # Parameters to find next points in the plot
        new_numbers = utils.next_sequence_points(new_numbers)
        start_points = new_points
        segments = [1 if n != 1 else 0 for n in new_numbers]
        angles += np.where(np.array(new_numbers) % 2 == 0, -config['theta'], config['theta'])

    # Video and figure closing
    if config['save_video']:
        video.release()

    # Plot showing, saving and closing
    if config['save_plot']:
        plt.savefig(config['plot_path'])
    if config['show_plot']:
        plt.show(block=True)
    cv2.destroyAllWindows()
    plt.close()