import asyncio
from rich.text import Text
from ..fonts import render_figlet

# Asynchronous typewriter effect (left-to-right)
async def async_typewrite(tc: "TextFlowThon", text: str, file: object = None) -> None:
    """
    Asynchronously animate text with a typewriter effect.

    Args:
        tc (TextFlowThon): The TextFlowThon instance (for config and helpers).
        text (str): The text to animate.
        file (object, optional): Output stream (default: tc.console's file).

    Returns:
        None
    """
    text = text.rstrip()
    if getattr(tc, 'font', None):
        text = render_figlet(text, tc.font)
    out_console = tc.console if file is None else tc._make_console(file)
    paragraphs = text.split('\n')
    for para_idx, para in enumerate(paragraphs):
        lines = tc._wrap(para)
        for line_idx, line in enumerate(lines):
            sent_text = ""
            for idx, letter in enumerate(line):
                sent_text += letter
                is_last_letter = (idx == len(line) - 1)
                if not is_last_letter:
                    tc._clear_line(out_console)
                    text_obj = Text(sent_text + tc.cursor, style=tc._get_style())
                    out_console.print(text_obj, end='\r', soft_wrap=True)
                    await asyncio.sleep(tc.delay)
            tc._clear_line(out_console)
            text_obj = Text(sent_text, style=tc._get_style())
            out_console.print(text_obj, end='\r', soft_wrap=True)
            await asyncio.sleep(tc.delay)
            out_console.print()  # move to next line
