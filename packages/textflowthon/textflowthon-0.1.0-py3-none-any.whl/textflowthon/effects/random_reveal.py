import time
import random
from rich.text import Text
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..core import TextFlowThon

def random_reveal(tc: "TextFlowThon", text: str, file: object = None, mask: str = "_") -> None:
    """
    Synchronously animate text by revealing characters in random order.

    Args:
        tc: The TextFlowThon instance (for config and helpers).
        text (str): The text to animate.
        file (object, optional): Output stream (default: tc.console's file).
        mask (str, optional): Placeholder character for unrevealed letters (default: '_').

    Returns:
        None
    """
    text = text.rstrip()
    out_console = tc.console if file is None else tc._make_console(file)
    revealed = [False if c != " " else True for c in text]
    display = [mask if c != " " else " " for c in text]
    indices = [i for i, c in enumerate(text) if c != " "]
    random.shuffle(indices)
    for idx in indices:
        revealed[idx] = True
        display[idx] = text[idx]
        to_show = "".join(display)
        tc._clear_line(out_console)
        text_obj = Text(to_show + tc.cursor, style=tc._get_style())
        out_console.print(text_obj, end='\r', soft_wrap=True)
        time.sleep(tc.delay)
    # Final full reveal
    tc._clear_line(out_console)
    text_obj = Text(text, style=tc._get_style())
    out_console.print(text_obj, end='\r', soft_wrap=True)
    time.sleep(tc.delay)
    out_console.print()  # move to next line
