import time
from typing import Optional
from rich.text import Text
from rich.console import Console
from rich.live import Live

def _parse_color(color: Optional[str]) -> str:
    if not color:
        return ""
    color = color.lower().strip()
    return color

def marquee(
    tc: "TextFlowThon",
    text: str,
    file: Optional[object] = None,
    width: int = 40,
    delay: float = 0.07,
    padding: int = 40,
    loop: int = 1,
    fg: Optional[str] = None,
    bounce: bool = False,
    pad_char: str = " ",
) -> None:
    """
    Synchronously scroll text horizontally like a marquee/news ticker.
    100% Rich-based using Live for in-place animation.
    Supports color, bounce, and custom padding.
    """
    pad = pad_char * max(padding, width)
    scroll_text = pad + text + pad
    style = _parse_color(fg or getattr(tc, 'fg', None) or "white")
    output = file or None
    console = Console(file=output, force_terminal=True)
    center_start = (width - len(text)) // 2
    with Live(Text("", style=style), console=console, refresh_per_second=int(1/delay)) as live:
        for bounce_num in range(loop):
            indices = list(range(len(scroll_text) - width + 1))
            if bounce:
                indices = indices + indices[::-1][1:-1]
            for i in indices:
                window = scroll_text[i:i+width]
                if len(window) < width:
                    window = window.ljust(width, pad_char)
                live.update(Text(window, style=style))
                time.sleep(delay)
                pos = window.find(text)
                # Only stop when centered AND it's the last bounce
                if (
                    bounce_num == loop - 1
                    and pos == center_start
                ):
                    live.update(Text(window, style=style))
                    time.sleep(0.6)
                    return
