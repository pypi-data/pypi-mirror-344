import random
import asyncio
from typing import Optional, List, Callable
from rich.text import Text

async def async_novice_type(
    tc: "TextFlowThon",
    text: str,
    file: Optional[object] = None,
    error_rate: float = 0.15,
    max_mistakes: int = 2,
    correction_delay: float = 0.5,
    backspace_delay: float = 0.03,
) -> None:
    """
    Asynchronously animate text as if typed by a novice, making and correcting mistakes iteratively.
    """
    async def _make_typo(text: str) -> str:
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
    out_console = tc.console if file is None else tc._make_console(file)
    i = 0
    correct_so_far = ""
    while i < len(text):
        mistakeful = correct_so_far
        error_indices = []
        n_mistakes = random.randint(1, max_mistakes)
        for _ in range(n_mistakes):
            if i >= len(text):
                break
            char = text[i]
            if random.random() < error_rate:
                error_indices.append(len(mistakeful))
                char = await _make_typo(char)
            mistakeful += char
            i += 1
            tc._clear_line(out_console)
            out_console.print(Text(mistakeful, style=tc._get_style()), end='\r', soft_wrap=True)
            await asyncio.sleep(tc.delay)
        if error_indices:
            await asyncio.sleep(correction_delay)
            first_mistake = error_indices[0]
            while len(mistakeful) > len(correct_so_far) + first_mistake:
                mistakeful = mistakeful[:-1]
                tc._clear_line(out_console)
                out_console.print(Text(mistakeful, style=tc._get_style()), end='\r', soft_wrap=True)
                await asyncio.sleep(backspace_delay)
            for j in range(len(correct_so_far) + first_mistake, min(len(correct_so_far) + n_mistakes, len(text))):
                mistakeful += text[j]
                tc._clear_line(out_console)
                out_console.print(Text(mistakeful, style=tc._get_style()), end='\r', soft_wrap=True)
                await asyncio.sleep(tc.delay)
            correct_so_far = mistakeful
        else:
            correct_so_far = mistakeful
    tc._clear_line(out_console)
    out_console.print(Text(correct_so_far, style=tc._get_style()), end='\r', soft_wrap=True)
    # Iteratively correct mistakes (may introduce new ones) until correct
    while correct_so_far != text:
        mismatch = 0
        while mismatch < min(len(correct_so_far), len(text)) and correct_so_far[mismatch] == text[mismatch]:
            mismatch += 1
        while len(correct_so_far) > mismatch:
            correct_so_far = correct_so_far[:-1]
            tc._clear_line(out_console)
            out_console.print(Text(correct_so_far, style=tc._get_style()), end='\r', soft_wrap=True)
            await asyncio.sleep(backspace_delay)
        chunk_size = random.randint(3, 6)
        new_chunk = ""
        for j in range(mismatch, min(mismatch + chunk_size, len(text))):
            char = text[j]
            if random.random() < error_rate:
                char = await _make_typo(char)
            new_chunk += char
            tc._clear_line(out_console)
            out_console.print(Text(correct_so_far + new_chunk, style=tc._get_style()), end='\r', soft_wrap=True)
            await asyncio.sleep(tc.delay)
        correct_so_far += new_chunk
        await asyncio.sleep(correction_delay)
    tc._clear_line(out_console)
    out_console.print(Text(text, style=tc._get_style()))
