import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex


def generate_colors_between(start_color, end_color, n) -> list:
    start_color = np.array(start_color) / 255.0
    end_color = np.array(end_color) / 255.0
    Color_list = [
        tuple(COLOR * 255) for COLOR in [start_color + t * (end_color - start_color) for t in np.linspace(0, 1, n)]
    ]
    return [to_hex(np.array(C) / 255.0) for C in Color_list]


if __name__ == '__main__':
    number_of_color = 50
    intermediate_colors = generate_colors_between((0, 0, 0), (255, 255, 255), number_of_color)
    print(intermediate_colors)
