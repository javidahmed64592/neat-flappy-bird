import numpy as np
from typing import List, Optional
from src.objects.pipe import Pipe


def get_closest_pipe(pipes: List["Pipe"], bird_pos_x: float) -> Optional["Pipe"]:
    """
    Determine which pipe pair is closest to and in front of the birds.

    Parameters:
        pipes (List(Pipe)): List of pipe pairs currently on screen
        bird_pos_x (float): x position of the birds

    Returns:
        closest (Pipe): Pipe closest to the birds
    """
    dist = np.inf
    closest = None

    for pipe in pipes:
        pipe_dist = pipe.x + pipe.width - bird_pos_x
        if 0 < pipe_dist < dist:
            dist = pipe_dist
            closest = pipe

    return closest
