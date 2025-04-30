import os
import random
import time
import sys
from rich.console import Console
from rich.live import Live
from rich.text import Text
from rich.color import Color
from typing import Optional, List
from .rain_colors import derive_rain_trail_colors

def matrix_rain(
    text: Optional[str] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    delay: float = 0.05,
    duration: float = 2.0,
    charset: Optional[List] = None,
    fg: str = "green4",
    msg_fg: str = "green1",
    file: Optional[object] = None
) -> None:
    """
    Synchronous Matrix-style rain animation. If width/height are None, autodetect terminal size.

    Args:
        text: Message to reveal in the rain (centered, multi-line supported).
        width: Width of the rain area (defaults to terminal width).
        height: Height of the rain area (defaults to terminal height minus 2).
        delay: Time between rain frames (seconds).
        duration: Total animation duration (seconds).
        charset: List of characters for rain (default: A-Z, 0-9, symbols).
        fg: Foreground color for rain (Rich color name or hex). Used for lead and trail colors.
        msg_fg: Foreground color for the revealed message.
        file: Output stream (default: sys.stdout).

    Rain trail colors:
        - Lead: bold fg
        - Trail: fg, dim fg
        - Last two: hardcoded Matrix green fades (#003300, #001a00)
        - If fg cannot be parsed, falls back to fg for first three trail colors.

    Returns:
        None
    """
    if charset is None:
        charset = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*+-")
    if width is None or height is None:
        try:
            size = os.get_terminal_size()
            if width is None:
                width = size.columns
            if height is None:
                height = size.lines - 2  # Leave space for prompt
        except OSError:
            width = width or 80
            height = height or 24
    console = Console(file=file, force_terminal=True, color_system="auto")
    columns = width
    rows = height
    drops = [random.randint(0, rows-1) for _ in range(columns)]
    # --- Multi-line Message Handling ---
    multiline = text.splitlines() if text else []
    lines_in_msg = len(multiline)
    msg_height = lines_in_msg
    # Center message block vertically and horizontally
    msg_top = (rows - msg_height) // 2 if msg_height < rows else 0
    msg_lefts = [ (columns - len(line)) // 2 if len(line) < columns else 0 for line in multiline ]
    revealed = [ [False]*len(line) for line in multiline ] if multiline else []
    # Track reveal cycles for each message character
    reveal_count = [ [0]*len(line) for line in multiline ] if multiline else []

    # --- Matrix Rain Advanced Features ---
    trail_length = 6
    lead_color = f"bold {fg}"
    trail_colors = derive_rain_trail_colors(fg)
    unicode_charset = list("ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜｦﾝ")
    use_unicode = any(ord(c) > 127 for c in charset)  # crude check if user passed unicode charset
    glitch_charset = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*+-░▒▓█")
    # Each drop is a list of y positions for the trail
    drop_trails = [[drops[i] - t for t in range(trail_length)] for i in range(columns)]

    # Track when message is fully revealed
    msg_fully_revealed_time = None

    def all_revealed_twice():
        return all(all(cnt >= 2 for cnt in row) for row in reveal_count) if reveal_count else True

    # Use a blueish-green color for message to stand out more
    message_color = f"bold {msg_fg}"

    def render_buffer(final_reveal=False):
        buffer = [[(" ", fg) for _ in range(columns)] for _ in range(rows)]
        # Draw message (revealed by rain only, per line, with cycling reveal)
        for l_idx, line in enumerate(multiline):
            msg_row = msg_top + l_idx
            msg_offset = msg_lefts[l_idx]
            for i, ch in enumerate(line):
                col = msg_offset + i
                if 0 <= col < columns and 0 <= msg_row < rows:
                    if final_reveal:
                        buffer[msg_row][col] = (ch, message_color)
                    else:
                        # Reveal only if the rain head passes over
                        if drops[col] == msg_row:
                            if revealed[l_idx][i] == False:
                                reveal_count[l_idx][i] += 1
                            revealed[l_idx][i] = True
                        # Hide again after a short time (simulate falling)
                        elif revealed[l_idx][i] and random.random() < 0.03:
                            revealed[l_idx][i] = False
                        if revealed[l_idx][i]:
                            buffer[msg_row][col] = (ch, message_color)
        # Draw rain (unchanged)
        for col in range(columns):
            drop_trails[col] = [(drops[col] - t) % rows for t in range(trail_length)]
            for t, y in enumerate(drop_trails[col]):
                if t == 0:
                    color = lead_color
                    char = random.choice(unicode_charset) if use_unicode and random.random() < 0.2 else random.choice(charset)
                else:
                    color = trail_colors[min(t-1, len(trail_colors)-1)]
                    if random.random() < 0.1:
                        char = random.choice(glitch_charset)
                    else:
                        char = random.choice(unicode_charset) if use_unicode and random.random() < 0.1 else random.choice(charset)
                # Don't overwrite revealed message
                is_msg = False
                for l_idx, line in enumerate(multiline):
                    msg_row = msg_top + l_idx
                    msg_offset = msg_lefts[l_idx]
                    if text and y == msg_row and msg_offset <= col < msg_offset+len(line) and (final_reveal or revealed[l_idx][col - msg_offset]):
                        is_msg = True
                        break
                if not is_msg:
                    buffer[y][col] = (char, color)
        # Advance drops
        if not final_reveal:
            for i in range(columns):
                if random.random() < 0.02:
                    drops[i] = 0
                else:
                    drops[i] = (drops[i] + 1) % rows
        lines = []
        for row in buffer:
            text_line = Text()
            for char, color in row:
                text_line.append(char, style=color)
            lines.append(text_line)
        return Text("\n").join(lines)

    with Live(console=console, screen=False, auto_refresh=False) as live:
        start = time.time()
        msg_fully_revealed_time = None
        final_message_done = False
        while True:
            if final_message_done:
                live.update(render_buffer(final_reveal=True), refresh=True)
                break
            live.update(render_buffer(), refresh=True)
            if all_revealed_twice():
                if msg_fully_revealed_time is None:
                    msg_fully_revealed_time = time.time()
                elif time.time() - msg_fully_revealed_time >= duration:
                    final_message_done = True
                    continue
            elif time.time() - start > 60 * 60:  # safety timeout
                break
            time.sleep(delay)

    # After animation, DO NOT print the final message centered. The message should remain embedded in the rain grid.
    # (No extra print here)
