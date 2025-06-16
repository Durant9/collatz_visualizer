import numpy as np

def next_sequence_points(start_points):
    '''
    Takes a list of numbers and for each one gives the next one following the 3x+1 rule
    :param start_points: list of starting numbers
    :return: list of next numbers
    '''
    return [n // 2 if n % 2 == 0 else 3 * n + 1 if n != 1 else 1 for n in start_points]

def render_frame(fig):
    '''
    Takes a plt.figure() and makes it a video frame
    :param fig: plt.figure() object to be converted into a frame
    :return: the resulting frame and its dimentions
    '''
    buf = BytesIO()
    fig.savefig(buf, format='png', facecolor=fig.get_facecolor(), bbox_inches='tight')
    buf.seek(0)
    img = Image.open(buf).convert("RGB")  
    frame = np.array(img)
    nrows, ncols = frame.shape[:2]
    return frame, ncols, nrows

def plot_limits(starts, theta, start_angle):
    '''
    Takes the parameters of the collatz sequence and gives the axis limits that allow to see the whole tree. The
    length of the segments is assumed to be 1
    :param starts: starting numbers of the sequence
    :param theta: bending angle
    :param start_angle: starting angle
    :return: axis limits
    '''
    # Starting points
    all_points = []
    start_points = [(0, 0) for _ in range(len(starts))]
    all_points.extend(start_points)

    # First iteration
    segments = np.array([1 if n != 1 else 0 for n in starts])
    angles = np.full(len(starts), start_angle)
    angles += np.where(np.array(starts) % 2 == 0, -theta, theta)
    new_numbers = next_sequence_points(starts)

    # Loop until all numbers are 1
    while any(n != 1 for n in new_numbers):
        # Computing all new points for the plot
        new_points = [(x + l * np.cos(a), y + l * np.sin(a))
                      for (x, y), l, a in zip(start_points, segments, angles)]
        all_points.extend(new_points)

        # Computing next sequence numbers
        new_numbers = next_sequence_points(new_numbers)
        start_points = new_points
        segments = [1 if n != 1 else 0 for n in new_numbers]
        angles += np.where(np.array(new_numbers) % 2 == 0, -theta, theta)

    # Setting the axis limits, with 5% tolerance
    xlim = (np.min([p[0] for p in all_points]), np.max([p[0] for p in all_points]))
    ylim = (np.min([p[1] for p in all_points]), np.max([p[1] for p in all_points]))
    x_size = xlim[1] - xlim[0]
    y_size = ylim[1] - ylim[0]
    return (xlim[0] - 0.05*x_size, xlim[1] + 0.05*x_size), (ylim[0] - 0.05*y_size, ylim[1] + 0.05*y_size)
