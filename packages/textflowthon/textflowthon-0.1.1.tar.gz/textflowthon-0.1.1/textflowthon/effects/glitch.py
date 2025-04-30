import random
import time
import sys
from typing import Optional

GLITCH_CHARS = list("@#$%&*?!/\\|[]{}()<>-=+~^0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")

def glitch_frames(text: str, steps: int = 8, delay: float = 0.03, mask: Optional[str] = None):
    """
    Yields frames where each character rapidly flickers through random symbols before settling into the correct letter.
    """
    n = len(text)
    order = list(range(n))
    for step in range(steps):
        frame = []
        # Settle up to step+1 characters (left to right)
        for i in range(n):
            if i < (step + 1):
                frame.append(text[i])
            else:
                frame.append(random.choice(GLITCH_CHARS))
        yield ''.join(frame)
        time.sleep(delay)
    # Final frame: show the actual text
    yield text

def glitch_typewrite(text: str, file: object = None, steps: int = 8, delay: float = 0.03) -> None:
    """
    Synchronously animate text with a glitch effect (random character flicker).

    Args:
        text (str): The text to animate.
        file (object, optional): Output stream (default: sys.stdout).
        steps (int, optional): Number of randomization steps per character (default: 8).
        delay (float, optional): Time between frames in seconds (default: 0.03).

    Returns:
        None
    """
    file = file or sys.stdout
    charset = "@#$%&*?!/\\|[]{}()<>-=+~^0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    length = len(text)
    current = [' ' for _ in range(length)]
    for i in range(length):
        for _ in range(steps):
            for j in range(i, length):
                current[j] = random.choice(charset)
            frame = ''.join(current)
            padded_frame = frame.ljust(length)
            print('\r' + padded_frame, end='', file=file, flush=True)
            time.sleep(delay)
        current[i] = text[i]
    # Final render
    print('\r' + ''.join(current).ljust(length), file=file, flush=True)
