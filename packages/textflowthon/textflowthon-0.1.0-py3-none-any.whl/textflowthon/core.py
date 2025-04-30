"""
TextFlow
=======
Cast your words, typewriter style.

TextFlow is a plug-and-play Python library for animating text in the terminal with a typewriter effect.

Features:
- Color support (per-line or per-character)
- Customizable speed, width, and cursor

Usage:
    from textflowthon import TextFlow
    tc = TextFlow(width=60, delay=0.03, cursor='|', fg='cyan')
    tc.typewrite("Hello, world!")

You can also use the generator:
    tc = TextFlow()
    for frame in tc.frames("Hello, world!"):
        ...

Run this file directly to see a demo.
"""
import os
from rich.console import Console
from .effects.typewrite import typewrite
from .effects.async_typewrite import async_typewrite
from .effects.reverse_typewrite import reverse_typewrite
from .effects.async_reverse_typewrite import async_reverse_typewrite
from .effects.random_reveal import random_reveal
from .effects.async_random_reveal import async_random_reveal
from .effects.glitch import glitch_typewrite
from .effects.async_glitch import async_glitch_typewrite
from .effects.matrix_rain import matrix_rain
from .effects.async_matrix_rain import async_matrix_rain
from .effects.novice_type import novice_type
from .effects.async_novice_type import async_novice_type
from .effects.corrupt import corrupt
from .effects.async_corrupt import async_corrupt
from .effects.marquee import marquee
from .effects.async_marquee import async_marquee
from .effects.boot_sequence import boot_sequence
from .effects.async_boot_sequence import async_boot_sequence

class TextFlow:
    """
    TextFlow animates text in the terminal with a typewriter effect.

    Args:
        width (int): Maximum line width before wrapping.
        delay (float): Delay between characters (seconds).
        cursor (str): Cursor character to show during typing.
        fg (str, optional): Foreground color name (Rich-compatible, e.g. 'yellow1').
        bg (str, optional): Background color name (Rich-compatible, e.g. 'red').
        font (str, optional): ASCII/FIGlet font name (pyfiglet-compatible, e.g. 'slant').

    Methods:
        typewrite(text, file=None): Synchronously animates the text to the terminal or a file.
        async_typewrite(text, file=None): Asynchronously animates the text to the terminal or a file.
        frames(text): Yield each frame of the animation as a string.
        random_reveal(text, file=None, mask="_"): Animates text by revealing characters in random order.
        async_random_reveal(text, file=None, mask="_"): Asynchronously animates text by revealing characters in random order.
        reverse_typewrite(text, file=None): Synchronously animates the text in the terminal with a typewriter effect from right to left.
        async_reverse_typewrite(text, file=None): Asynchronously animates the text in the terminal with a typewriter effect from right to left.
        glitch(text, file=None, steps=8, delay=0.03): Synchronously animates the text with a glitch effect.
        async_glitch(text, file=None, steps=8, delay=0.03): Asynchronously animates the text with a glitch effect.
        matrix_rain(width=80, height=24, delay=0.05, duration=2.0, charset=None, fg="green1", msg_fg="#39FF14", file=None): Matrix-style rain animation (sync).
        async_matrix_rain(width=80, height=24, delay=0.05, duration=2.0, charset=None, fg="green1", msg_fg="#39FF14", file=None): Matrix-style rain animation (async).
        novice_type(text, file=None, error_rate=0.15, max_mistakes=2, correction_delay=0.5, backspace_delay=0.03): Synchronously animate text as if typed by a novice, making and correcting mistakes.
        async_novice_type(text, file=None, error_rate=0.15, max_mistakes=2, correction_delay=0.5, backspace_delay=0.03): Asynchronously animate text as if typed by a novice, making and correcting mistakes.
        corrupt(text, file=None, cycles=4, corrupt_sections=2, corrupt_duration=0.25, symbols="@#$%&*?!"): Synchronously show the message, then repeatedly corrupt random sections with gibberish before restoring.
        async_corrupt(text, file=None, cycles=4, corrupt_sections=2, corrupt_duration=0.25, symbols="@#$%&*?!"): Asynchronously show the message, then repeatedly corrupt random sections with gibberish before restoring.
        marquee(text, file=None, width=40, delay=0.06, padding=8, loop=1, fg=None, bounce=False, pad_char=" "): Synchronously scroll text horizontally like a marquee/news ticker.
        async_marquee(text, file=None, width=40, delay=0.06, padding=8, loop=1, fg=None, bounce=False, pad_char=" "): Asynchronously scroll text horizontally like a marquee/news ticker.
        boot_sequence(message, file=None, delay=0.06, bios_lines=None, highlight_color="bright_green", bios_color="bright_white", mem_color="cyan", error_color="bright_red", boot_ok=True): Simulate a retro terminal boot sequence with BIOS/firmware lines, memory checks, and a final highlighted message.
        async_boot_sequence(message, file=None, delay=0.06, bios_lines=None, highlight_color="bright_green", bios_color="bright_white", mem_color="cyan", error_color="bright_red", boot_ok=True): Asynchronously simulate a retro terminal boot sequence with BIOS/firmware lines, memory checks, and a final highlighted message.

    Example:
        tc = TextFlow(fg="yellow1", bg="red")
        tc.typewrite("Hello!")
    """
    def __init__(self, width: int = 79, delay: float = 0.05, cursor: str = '|', fg: str = "green4", bg: str = None, font: str = None) -> None:
        """
        Initialize a TextFlow instance for terminal text animation.

        Args:
            width (int, optional): Maximum line width before wrapping. Default is 79.
            delay (float, optional): Delay between characters (seconds). Default is 0.05.
            cursor (str, optional): Cursor character to show during typing. Default is '|'.
            fg (str, optional): Foreground color name (Rich-compatible). Default is 'green4'.
            bg (str, optional): Background color name (Rich-compatible). Default is None.
            font (str, optional): ASCII/FIGlet font name (pyfiglet-compatible). Default is None.
        """
        self.width = width
        self.delay = delay
        self.cursor = cursor
        self.fg = fg
        self.bg = bg
        self.console = Console()
        self.font = font

    def frames(self, text: str) -> str:
        """
        Yields each frame of the typewriter animation as a string.
        Useful for custom rendering or testing.

        Args:
            text (str): The text to animate.

        Yields:
            str: The next frame of the animation.
        """
        paragraphs = text.rstrip().split('\n')
        for para in paragraphs:
            lines = self._wrap(para)
            for line in lines:
                sent_text = ""
                for idx, letter in enumerate(line):
                    sent_text += letter
                    yield sent_text + self.cursor
                yield sent_text

    def _clear_line(self, out_console: Console) -> None:
        """
        Clears the current line from cursor position to the end using only carriage return and space padding for cross-platform compatibility.

        Args:
            out_console (Console): The Rich Console object to clear the line on.
        """
        # Find terminal width or default to 80
        try:
            width = out_console.width if hasattr(out_console, 'width') else 80
        except Exception:
            width = 80
        out_console.file.write('\r' + ' ' * width + '\r')
        out_console.file.flush()

    def _make_console(self, file: object) -> Console:
        """
        Create a Rich Console for a specific output file.

        Args:
            file (object): Output stream.

        Returns:
            Console: A Rich Console instance for the file.
        """
        return Console(file=file)

    def _wrap(self, text: str) -> list:
        """
        Wrap the text to the specified width.

        Args:
            text (str): The text to wrap.

        Returns:
            list: List of wrapped lines.
        """
        import textwrap
        return textwrap.wrap(text, width=self.width)

    def typewrite(self, text: str, file: object = None) -> None:
        """
        Synchronously animate text with a typewriter effect.
        """
        return typewrite(self, text, file)

    async def async_typewrite(self, text: str, file: object = None) -> None:
        """
        Asynchronously animate text with a typewriter effect.
        """
        return await async_typewrite(self, text, file)

    def reverse_typewrite(self, text: str, file: object = None) -> None:
        """
        Synchronously animate text with a reverse typewriter effect.
        """
        return reverse_typewrite(self, text, file)

    async def async_reverse_typewrite(self, text: str, file: object = None) -> None:
        """
        Asynchronously animate text with a reverse typewriter effect.
        """
        return await async_reverse_typewrite(self, text, file)

    def random_reveal(self, text: str, file: object = None, mask: str = "_") -> None:
        """
        Synchronously animate text by revealing characters in random order.
        """
        return random_reveal(self, text, file, mask)

    async def async_random_reveal(self, text: str, file: object = None, mask: str = "_") -> None:
        """
        Asynchronously animate text by revealing characters in random order.
        """
        return await async_random_reveal(self, text, file, mask)

    def glitch(self, text: str, file: object = None, steps: int = 8, delay: float = 0.03) -> None:
        """
        Synchronously animate text with a glitch effect.
        """
        return glitch_typewrite(text, file=file, steps=steps, delay=delay)

    async def async_glitch(self, text: str, file: object = None, steps: int = 8, delay: float = 0.03) -> None:
        """
        Asynchronously animate text with a glitch effect.
        """
        return await async_glitch_typewrite(text, file=file, steps=steps, delay=delay)

    def matrix_rain(self, text: str = None, width: int = 80, height: int = 24, delay: float = 0.05, duration: float = 2.0, charset: list = None, fg: str = "green4", msg_fg: str = "green1", file: object = None) -> None:
        """
        Matrix-style rain animation (sync).
        """
        return matrix_rain(text=text, width=width, height=height, delay=delay, duration=duration, charset=charset, fg=fg, msg_fg=msg_fg, file=file)

    async def async_matrix_rain(self, text: str = None, width: int = 80, height: int = 24, delay: float = 0.05, duration: float = 2.0, charset: list = None, fg: str = "green4", msg_fg: str = "green1", file: object = None) -> None:
        """
        Matrix-style rain animation (async).
        """
        return await async_matrix_rain(text=text, width=width, height=height, delay=delay, duration=duration, charset=charset, fg=fg, msg_fg=msg_fg, file=file)

    def novice_type(self, text: str, file: object = None, error_rate: float = 0.15, max_mistakes: int = 2, correction_delay: float = 0.5, backspace_delay: float = 0.03) -> None:
        """
        Synchronously animate text as if typed by a novice, making and correcting mistakes.
        """
        return novice_type(self, text, file, error_rate, max_mistakes, correction_delay, backspace_delay)

    async def async_novice_type(self, text: str, file: object = None, error_rate: float = 0.15, max_mistakes: int = 2, correction_delay: float = 0.5, backspace_delay: float = 0.03) -> None:
        """
        Asynchronously animate text as if typed by a novice, making and correcting mistakes.
        """
        return await async_novice_type(self, text, file, error_rate, max_mistakes, correction_delay, backspace_delay)

    def corrupt(self, text: str, file: object = None, cycles: int = 4, corrupt_sections: int = 2, corrupt_duration: float = 0.25, symbols: str = "@#$%&*?!") -> None:
        """
        Synchronously show the message, then repeatedly corrupt random sections with gibberish before restoring.
        """
        return corrupt(self, text, file, cycles, corrupt_sections, corrupt_duration, symbols)

    async def async_corrupt(self, text: str, file: object = None, cycles: int = 4, corrupt_sections: int = 2, corrupt_duration: float = 0.25, symbols: str = "@#$%&*?!") -> None:
        """
        Asynchronously show the message, then repeatedly corrupt random sections with gibberish before restoring.
        """
        return await async_corrupt(self, text, file, cycles, corrupt_sections, corrupt_duration, symbols)

    def marquee(self, text: str, file: object = None, width: int = 40, delay: float = 0.06, padding: int = 8, loop: int = 1, fg: str = None, bounce: bool = False, pad_char: str = " ") -> None:
        """
        Synchronously scroll text horizontally like a marquee/news ticker.
        Supports standard, bright, and RGB color, bidirectional (bounce) mode, and custom padding characters.
        """
        return marquee(self, text, file, width, delay, padding, loop, fg, bounce, pad_char)

    async def async_marquee(self, text: str, file: object = None, width: int = 40, delay: float = 0.06, padding: int = 8, loop: int = 1, fg: str = None, bounce: bool = False, pad_char: str = " ") -> None:
        """
        Asynchronously scroll text horizontally like a marquee/news ticker.
        Supports standard, bright, and RGB color, bidirectional (bounce) mode, and custom padding characters.
        """
        return await async_marquee(self, text, file, width, delay, padding, loop, fg, bounce, pad_char)

    def boot_sequence(self,
        message: str,
        file: object = None,
        delay: float = 0.06,
        bios_lines: list = None,
        highlight_color: str = "bright_green",
        bios_color: str = "bright_white",
        mem_color: str = "cyan",
        error_color: str = "bright_red",
        boot_ok: bool = True,
    ) -> None:
        """
        Simulate a retro terminal boot sequence with BIOS/firmware lines, memory checks, and a final highlighted message.
        """
        return boot_sequence(
            message=message,
            file=file,
            delay=delay,
            bios_lines=bios_lines,
            highlight_color=highlight_color,
            bios_color=bios_color,
            mem_color=mem_color,
            error_color=error_color,
            boot_ok=boot_ok
        )

    async def async_boot_sequence(self,
        message: str,
        file: object = None,
        delay: float = 0.06,
        bios_lines: list = None,
        highlight_color: str = "bright_green",
        bios_color: str = "bright_white",
        mem_color: str = "cyan",
        error_color: str = "bright_red",
        boot_ok: bool = True,
    ) -> None:
        """
        Asynchronously simulate a retro terminal boot sequence with BIOS/firmware lines, memory checks, and a final highlighted message.
        """
        return await async_boot_sequence(
            message=message,
            file=file,
            delay=delay,
            bios_lines=bios_lines,
            highlight_color=highlight_color,
            bios_color=bios_color,
            mem_color=mem_color,
            error_color=error_color,
            boot_ok=boot_ok
        )

    def _get_style(self) -> str:
        """
        Helper to build the Rich style string for the current color and background color.

        Returns:
            str: Rich style string.
        """
        style = ""
        if self.fg:
            style += f"{self.fg} "
        if self.bg:
            style += f"on {self.bg} "
        return style.strip()

    @staticmethod
    def list_effects() -> None:
        """
        Print the available animation effects in TextFlow.
        """
        EFFECTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'textflowthon', 'effects')
        print("Available animation effects in TextFlow:")
        for fname in sorted(os.listdir(EFFECTS_DIR)):
            if fname.endswith('.py') and not fname.startswith('__'):
                print(" -", fname.replace('.py', ''))
