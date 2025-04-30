import random
import time
from typing import Optional, Sequence
from rich.text import Text

def corrupt(
    tc: "TextFlowThon",
    text: str,
    file: Optional[object] = None,
    cycles: int = 4,
    corrupt_sections: int = 2,
    corrupt_duration: float = 0.25,
    symbols: Sequence[str] = "@#$%&*?!",
) -> None:
    """
    Synchronously show the message, then repeatedly corrupt random sections with gibberish before restoring.

    Args:
        tc (TextFlowThon): The TextFlowThon instance (for config and helpers).
        text (str): The text to animate.
        file (object, optional): Output stream (default: tc.console's file).
        cycles (int): Number of corruption cycles.
        corrupt_sections (int): Number of random sections to corrupt per cycle.
        corrupt_duration (float): Duration (seconds) each corruption lasts.
        symbols (Sequence[str]): Symbols to use for corruption.
    """
    out_console = tc.console if file is None else tc._make_console(file)
    # Show the correct message
    tc._clear_line(out_console)
    out_console.print(Text(text, style=tc._get_style()), end='\r', soft_wrap=True)
    time.sleep(tc.delay * 2)
    for _ in range(cycles):
        # Corrupt random sections
        corrupt_indices = sorted(random.sample(range(len(text)), min(corrupt_sections, len(text))))
        corrupted = list(text)
        for idx in corrupt_indices:
            corrupted[idx] = random.choice(symbols)
        tc._clear_line(out_console)
        out_console.print(Text(''.join(corrupted), style=tc._get_style()), end='\r', soft_wrap=True)
        time.sleep(corrupt_duration)
        # Restore
        tc._clear_line(out_console)
        out_console.print(Text(text, style=tc._get_style()), end='\r', soft_wrap=True)
        time.sleep(tc.delay * 2)
    tc._clear_line(out_console)
    out_console.print(Text(text, style=tc._get_style()))
