import random
import time
from typing import Optional, TYPE_CHECKING
from rich.text import Text
if TYPE_CHECKING:
    from ..core import TextFlowThon

def _make_typo(text: str) -> str:
    # Randomly choose a typo: swap, omit, insert, wrong char
    if not text:
        return text
    typo_type = random.choice(["swap", "omit", "insert", "wrong"])
    idx = random.randint(0, len(text) - 1)
    if typo_type == "swap" and len(text) > 1 and idx < len(text) - 1:
        chars = list(text)
        chars[idx], chars[idx+1] = chars[idx+1], chars[idx]
        return "".join(chars)
    elif typo_type == "omit":
        return text[:idx] + text[idx+1:]
    elif typo_type == "insert":
        insert_char = random.choice("abcdefghijklmnopqrstuvwxyz")
        return text[:idx] + insert_char + text[idx:]
    elif typo_type == "wrong":
        wrong_char = random.choice("abcdefghijklmnopqrstuvwxyz")
        return text[:idx] + wrong_char + text[idx+1:]
    return text

def novice_type(
    tc: "TextFlowThon",
    text: str,
    file: Optional[object] = None,
    error_rate: float = 0.15,
    max_mistakes: int = 2,
    correction_delay: float = 0.5,
    backspace_delay: float = 0.03,
) -> None:
    """
    Synchronously animate text as if typed by a novice, making and correcting mistakes.

    Args:
        tc: The TextFlowThon instance (for config and helpers).
        text (str): The text to animate.
        file (object, optional): Output stream (default: tc.console's file).
        error_rate (float, optional): Probability of making a mistake per character.
        max_mistakes (int, optional): Max mistakes before correction (randomized up to this).
        correction_delay (float, optional): Delay before noticing and correcting mistakes.
        backspace_delay (float, optional): Delay between backspace steps.
    """
    out_console = tc.console if file is None else tc._make_console(file)
    i = 0
    correct_so_far = ""
    while i < len(text):
        mistakeful = correct_so_far
        error_indices = []
        n_mistakes = random.randint(1, max_mistakes)
        # Type up to n_mistakes (with some being errors)
        for _ in range(n_mistakes):
            if i >= len(text):
                break
            char = text[i]
            if random.random() < error_rate:
                error_indices.append(len(mistakeful))
                char = _make_typo(char)
            mistakeful += char
            i += 1
            tc._clear_line(out_console)
            out_console.print(Text(mistakeful, style=tc._get_style()), end='\r', soft_wrap=True)
            time.sleep(tc.delay)
        # If mistakes were made, pause and correct
        if error_indices:
            time.sleep(correction_delay)
            first_mistake = error_indices[0]
            # Animate backspacing to the first mistake
            while len(mistakeful) > len(correct_so_far) + first_mistake:
                mistakeful = mistakeful[:-1]
                tc._clear_line(out_console)
                out_console.print(Text(mistakeful, style=tc._get_style()), end='\r', soft_wrap=True)
                time.sleep(backspace_delay)
            # Retype the correct text from the first mistake onward
            for j in range(len(correct_so_far) + first_mistake, min(len(correct_so_far) + n_mistakes, len(text))):
                mistakeful += text[j]
                tc._clear_line(out_console)
                out_console.print(Text(mistakeful, style=tc._get_style()), end='\r', soft_wrap=True)
                time.sleep(tc.delay)
            correct_so_far = mistakeful
        else:
            correct_so_far = mistakeful
    tc._clear_line(out_console)
    out_console.print(Text(correct_so_far, style=tc._get_style()), end='\r', soft_wrap=True)
    # Iteratively correct mistakes (may introduce new ones) until correct
    while correct_so_far != text:
        # Find first mismatch
        mismatch = 0
        while mismatch < min(len(correct_so_far), len(text)) and correct_so_far[mismatch] == text[mismatch]:
            mismatch += 1
        # Animate backspacing to the mismatch
        while len(correct_so_far) > mismatch:
            correct_so_far = correct_so_far[:-1]
            tc._clear_line(out_console)
            out_console.print(Text(correct_so_far, style=tc._get_style()), end='\r', soft_wrap=True)
            time.sleep(backspace_delay)
        # Retype a chunk (3-6 chars) from mismatch, possibly with new mistakes
        chunk_size = random.randint(3, 6)
        new_chunk = ""
        for j in range(mismatch, min(mismatch + chunk_size, len(text))):
            char = text[j]
            if random.random() < error_rate:
                char = _make_typo(char)
            new_chunk += char
            tc._clear_line(out_console)
            out_console.print(Text(correct_so_far + new_chunk, style=tc._get_style()), end='\r', soft_wrap=True)
            time.sleep(tc.delay)
        correct_so_far += new_chunk
        time.sleep(correction_delay)
    # Final output: clear and print only the correct line
    tc._clear_line(out_console)
    out_console.print(Text(text, style=tc._get_style()))
