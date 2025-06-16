# Collatz Visualizer
Toolkit to visualize the collatz conjecture

## Installation and usage
Install the dependencies with 
```
pip install -r requirements.txt
```
Then run the main code with
```
python collatz.py
```
### Parameters
It's possible to pass the parameters via CLI or the yaml config file (template [here](./configs/config.yaml)). Here's a description of the parameters:

- --**n** (*int*): Number of integers to plot. It's computed the collatz sequence for all the starting numbers between 2 and n;
- --**theta** (*float*): Bending angle, in radiants. Determines, for every step in a sequence, how much the segment has to rotate;
- --**start_angle** (*float*): Starting angle for the first segment, in radiants;
- --**color** (*str*): Color of the lines in the plot, in exadecimal notation (es #FFFF00);
- --**line_width** (*float*): Width of the lines in the plot;
- --**alpha** (*float*): Transparency of the lines in the plot. Must be between 0 and 1;
- --**save_video** (*bool*): Wether to save a video of the construction of the collatz tree;
- --**video_path** (*str*): Path where to save the output video;
- --**fps** (*int*): fps of the producted video;
- --**save_plot** (*bool*): Wether to save the final image of the collatz tree;
- --**show_plot** (*bool*): Wether to instantly show the final image of the collatz tree;
- --**plot_path** (*str*): Path where to save the output video

## Particular examples
<p align="center"><img width="500" alt="image" src="plots/collatz_pi3.png"></p>
