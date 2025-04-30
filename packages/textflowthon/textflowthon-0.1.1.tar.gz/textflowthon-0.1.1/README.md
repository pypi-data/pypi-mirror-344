# TextFlowthon

A modular Python library for animating text output in the terminal with typewriter and other effects. Supports sync/async, custom fonts, and more.

---

## Project Structure

TextFlowthon is fully modular. All animation effects are implemented as separate modules in the `textflowthon/effects/` directory:

```
textflowthon/
├── __init__.py
├── core.py
├── fonts.py
├── utils.py
├── effects/
│   ├── __init__.py
│   ├── typewrite.py
│   ├── async_typewrite.py
│   ├── reverse_typewrite.py
│   ├── async_reverse_typewrite.py
│   ├── random_reveal.py
│   ├── async_random_reveal.py
│   ├── glitch.py
│   ├── async_glitch.py
│   ├── matrix_rain.py
│   ├── async_matrix_rain.py
│   ├── novice_type.py
│   ├── async_novice_type.py
│   ├── corrupt.py
│   ├── async_corrupt.py
│   ├── marquee.py
│   ├── async_marquee.py
│   ├── boot_sequence.py
│   ├── async_boot_sequence.py
│   ├── ...
├── ...
examples/
├── sync_typewrite_ex.py
├── async_typewrite_ex.py
├── figlet_font_ex.py
├── async_figlet_font_ex.py
├── random_reveal_ex.py
├── async_random_reveal_ex.py
├── reverse_typewrite_ex.py
├── async_reverse_typewrite_ex.py
├── glitch_ex.py
├── async_glitch_ex.py
├── matrix_rain_ex.py
├── async_matrix_rain_ex.py
├── novice_type_ex.py
├── async_novice_type_ex.py
├── corrupt_ex.py
├── async_corrupt_ex.py
├── marquee_ex.py
├── async_marquee_ex.py
├── boot_sequence_ex.py
├── async_boot_sequence_ex.py
├── list_effects.py
├── showoff_all_examples.py
├── ...
docs/
├── README.md
├── advanced.md
├── index.md
├── usage_guide.md
├── contributing.md
├── ...
tests/
├── test_core.py
├── test_figlet_font.py
├── test_random_reveal.py
├── test_reverse_typewrite.py
├── test_errors.py
├── test_glitch.py
├── test_matrix_rain.py
├── test_novice_type.py
├── test_corrupt.py
├── test_marquee.py
├── test_boot_sequence.py
├── ...
pyproject.toml
```

- To add a new effect, create a new file in `effects/` and wire it up in `core.py`.

---

## Examples

See the `examples/` directory for scripts demonstrating every effect and feature, including:
- **Typewriter Effect**: Classic left-to-right animation, with support for custom cursor, color, and font.
- **Reverse Typewriter**: Animate text right-to-left, with all the same customization options.
- **Random Reveal**: Characters are revealed in random order (customizable mask character).
- **Glitch Effect**: Characters flicker through random symbols before resolving to the final text.
- **Matrix Rain**: Matrix-style falling code effect (sync and async), with customizable colors for rain and message, and advanced trail color logic.
- **Novice Type**: Simulates a novice typist making multiple mistakes before backspacing and correcting them, for a realistic "learning" typewriter effect. Supports both sync and async usage, with customizable error rate and correction timing.
- **Corrupt Effect**: The message is instantly shown, then random sections are repeatedly replaced with gibberish/symbols ("corrupted") and restored, before settling on the correct text. Great for horror, glitch, or suspenseful moments. Supports sync and async.
- **Marquee/Crawl**: Text scrolls horizontally, like a news ticker or Star Wars crawl. Supports sync and async, with customizable width, speed, padding, and color.
- **Boot Sequence Effect**: Simulate a retro terminal boot sequence, including BIOS/firmware lines, memory checks, device detection, and a final highlighted message. Fully customizable and perfect for tech/cyberpunk demos!

All effects support both synchronous and asynchronous (asyncio) usage, and output can be directed to any file-like stream.

## Marquee Effect

TextFlowThon provides smooth, highly customizable marquee (scrolling text) effects for the terminal, both synchronous and asynchronous.

### Features
- Smooth, in-place scrolling using Rich Live (no ANSI escape codes)
- Full color support (standard, bright, hex)
- Bidirectional (bounce) scrolling
- Custom padding character
- Seamless, natural centering at end of animation
- Identical API for sync and async usage

---

## Installation

### Recommended: Using `uv`

[`uv`](https://github.com/astral-sh/uv) is a modern Python package and environment manager that is:
- **Extremely fast** (Rust-powered, up to 100x faster than pip)
- **All-in-one** (manages venvs, installs, and dependencies)
- **Reliable** (lockfiles, reproducible builds)
- **Drop-in replacement** for pip/venv

#### Install `uv`:
- With pip:
  ```sh
  pip install uv
  ```
- With Homebrew (macOS/Linux):
  ```sh
  brew install astral-sh/uv/uv
  ```
- Or download from [GitHub Releases](https://github.com/astral-sh/uv/releases)

#### Quickstart:
```sh
uv init # Initialize a new project
uv add textflowthon rich # Install dependencies
uv run your_script.py # Run your script
```

### Manual (pip/venv)

1. Create a virtual environment:
   ```sh
   python -m venv .venv
   ```
2. Activate it:
   - Windows:
     ```sh
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```sh
     source .venv/bin/activate
     ```
3. Install dependencies:
   ```sh
   pip install textflowthon rich
   ```
4. Run your scripts as usual:
   ```sh
   python your_script.py
   ```

---

### Usage Example (Sync)
```python
from textflowthon import TextFlowThon
import sys

tc = TextFlowThon()
tc.marquee(
    "TYPECAST MARQUEE EFFECT!",
    file=sys.stdout,
    width=40,
    delay=0.07,
    padding=40,
    loop=2,
    fg="red",         # any Rich color name or hex
    bounce=True,       # bidirectional
    pad_char="-"      # custom padding
)
```

### Usage Example (Async)
```python
import sys
import asyncio
from textflowthon import TextFlowThon

tc = TextFlowThon()

async def main():
    await tc.async_marquee(
        "TYPECAST MARQUEE EFFECT!",
        file=sys.stdout,
        width=40,
        delay=0.07,
        padding=40,
        loop=2,
        fg="red",
        bounce=True,
        pad_char="-"
    )

if __name__ == "__main__":
    asyncio.run(main())
```

### Parameters
- `text`: The message to scroll
- `file`: Output stream (default: sys.stdout)
- `width`: Width of the visible window
- `delay`: Delay between frames (seconds)
- `padding`: Spaces or characters to pad before/after message
- `loop`: Number of bounce cycles before stopping
- `fg`: Foreground color (Rich color name or hex)
- `bounce`: Enable bidirectional scrolling
- `pad_char`: Character used for padding

### Behavior
- The marquee bounces for `loop` cycles and only stops when the message is perfectly centered.
- No ANSI codes are used; all output is handled by Rich for maximum compatibility.

See `examples/marquee_ex.py` and `examples/async_marquee_ex.py` for full demos.

## Boot Sequence Effect

Simulate a retro terminal boot sequence, including BIOS/firmware lines, memory checks, device detection, and a final highlighted message. Fully customizable and perfect for tech/cyberpunk demos!

### Usage Example (Sync)
```python
from textflowthon import TextFlowThon
import sys

tc = TextFlowThon()
tc.boot_sequence(
    message="WELCOME TO TYPECAST OS!",
    file=sys.stdout,
    delay=0.08,
    highlight_color="bright_green",
    bios_color="bright_white",
    mem_color="cyan",
    error_color="bright_red",
    boot_ok=True
)
```

### Usage Example (Async)
```python
import sys
import asyncio
from textflowthon import TextFlowThon

tc = TextFlowThon()

async def main():
    await tc.async_boot_sequence(
        message="ASYNC BOOT: WELCOME TO TYPECAST OS!",
        file=sys.stdout,
        delay=0.08,
        highlight_color="bright_green",
        bios_color="bright_white",
        mem_color="cyan",
        error_color="bright_red",
        boot_ok=True
    )

if __name__ == "__main__":
    asyncio.run(main())
```

### Parameters
- `message`: The final message to display, centered and highlighted
- `file`: Output stream (default: sys.stdout)
- `delay`: Delay between BIOS/firmware lines (seconds)
- `bios_lines`: Optional custom list of BIOS/firmware lines
- `highlight_color`: Color for the final message
- `bios_color`: Color for BIOS/firmware lines
- `mem_color`: Color for memory check lines
- `error_color`: Color for error messages
- `boot_ok`: Whether to show a successful or error boot status

### Behavior
- Animates a full boot sequence, then centers and highlights your message.
- Both sync and async APIs are available with identical parameters and behavior.
- All output is handled by Rich for color and styling.

See `examples/boot_sequence_ex.py` and `examples/async_boot_sequence_ex.py` for full demos.

## Usage

```python
from textflowthon import TextFlowThon

tc = TextFlowThon(width=60, delay=0.04, fg="cyan", cursor="▍")
tc.typewrite("Hello, world!")

# Async usage
import asyncio
asyncio.run(tc.async_typewrite("Async hello!"))

# Reverse typewriter
from textflowthon import TextFlowThon
tc = TextFlowThon()
tc.reverse_typewrite("Backwards!")

# Random reveal
from textflowthon import TextFlowThon
tc = TextFlowThon()
tc.random_reveal("Surprise!", mask="*")

# Glitch effect
from textflowthon import TextFlowThon
tc = TextFlowThon()
tc.glitch("Glitchy text!", steps=10, delay=0.02)

# Matrix rain
from textflowthon import TextFlowThon
tc = TextFlowThon()
tc.matrix_rain(text="NEON GREEN!", width=60, height=18, delay=0.04, duration=3.0, fg="green4", msg_fg="green1")

# Novice Type
from textflowthon import TextFlowThon

tc = TextFlowThon(fg="yellow", cursor="_")
tc.novice_type("This is a demo of the novice type effect!", error_rate=0.2, max_mistakes=3, correction_delay=0.4, backspace_delay=0.04)

# Async
import asyncio
tc = TextFlowThon(fg="yellow", cursor="_")
asyncio.run(tc.async_novice_type("Async novice typewriter demo!", error_rate=0.2, max_mistakes=3, correction_delay=0.4, backspace_delay=0.04))

# Corrupt Effect

tc = TextFlowThon(fg="magenta", cursor="_")
tc.corrupt("CORRUPTION IN PROGRESS!", cycles=5, corrupt_sections=4, corrupt_duration=0.18, symbols="@#$%&*?!")

# Async
import asyncio
tc = TextFlowThon(fg="magenta", cursor="_")
asyncio.run(tc.async_corrupt("ASYNC CORRUPTION IN PROGRESS!", cycles=5, corrupt_sections=4, corrupt_duration=0.18, symbols="@#$%&*?!"))

See the [usage guide](docs/usage_guide.md) for more details and advanced examples.

---

For installation, usage, and contribution instructions, see the docs/ directory.