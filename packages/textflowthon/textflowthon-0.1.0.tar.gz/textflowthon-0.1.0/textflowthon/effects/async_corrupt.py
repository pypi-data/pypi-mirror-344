import random
import asyncio
from typing import Optional, Sequence
from rich.text import Text

async def async_corrupt(
    tc: "TextFlowThon",
    text: str,
    file: Optional[object] = None,
    cycles: int = 4,
    corrupt_sections: int = 2,
    corrupt_duration: float = 0.25,
    symbols: Sequence[str] = "@#$%&*?!",
) -> None:
    """
    Asynchronously show the message, then repeatedly corrupt random sections with gibberish before restoring.
    """
    out_console = tc.console if file is None else tc._make_console(file)
    tc._clear_line(out_console)
    out_console.print(Text(text, style=tc._get_style()), end='\r', soft_wrap=True)
    await asyncio.sleep(tc.delay * 2)
    for _ in range(cycles):
        corrupt_indices = sorted(random.sample(range(len(text)), min(corrupt_sections, len(text))))
        corrupted = list(text)
        for idx in corrupt_indices:
            corrupted[idx] = random.choice(symbols)
        tc._clear_line(out_console)
        out_console.print(Text(''.join(corrupted), style=tc._get_style()), end='\r', soft_wrap=True)
        await asyncio.sleep(corrupt_duration)
        tc._clear_line(out_console)
        out_console.print(Text(text, style=tc._get_style()), end='\r', soft_wrap=True)
        await asyncio.sleep(tc.delay * 2)
    tc._clear_line(out_console)
    out_console.print(Text(text, style=tc._get_style()))
