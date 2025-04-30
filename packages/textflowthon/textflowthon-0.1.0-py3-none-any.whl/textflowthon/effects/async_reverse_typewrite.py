import asyncio
from rich.text import Text

async def async_reverse_typewrite(tc: "TextFlowThon", text: str, file: object = None) -> None:
    """
    Asynchronously animate text with a reverse typewriter effect (right-to-left).

    Args:
        tc (TextFlowThon): The TextFlowThon instance (for config and helpers).
        text (str): The text to animate.
        file (object, optional): Output stream (default: tc.console's file).

    Returns:
        None
    """
    text = text.rstrip()
    out_console = tc.console if file is None else tc._make_console(file)
    n = len(text)
    for i in range(1, n + 1):
        frame = text[-i:]
        tc._clear_line(out_console)
        text_obj = Text(frame + tc.cursor, style=tc._get_style())
        out_console.print(text_obj, end='\r', soft_wrap=True)
        await asyncio.sleep(tc.delay)
    # Final full reveal
    tc._clear_line(out_console)
    text_obj = Text(text, style=tc._get_style())
    out_console.print(text_obj, end='\r', soft_wrap=True)
    await asyncio.sleep(tc.delay)
    out_console.print()  # move to next line
