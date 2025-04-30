import asyncio
from typing import Optional, List
from rich.console import Console
from rich.text import Text
from rich.style import Style

async def async_boot_sequence(
    message: str,
    file: Optional[object] = None,
    delay: float = 0.06,
    bios_lines: Optional[List[str]] = None,
    highlight_color: str = "bright_green",
    bios_color: str = "bright_white",
    mem_color: str = "cyan",
    error_color: str = "bright_red",
    boot_ok: bool = True,
) -> None:
    """
    Asynchronously simulate a retro terminal boot sequence with BIOS/firmware lines, memory checks, and a final highlighted message.
    """
    console = Console(file=file, force_terminal=True)
    default_bios = [
        "PhoenixBIOS 4.0 Release 6.0     Copyright 1985-1988 Phoenix Technologies Ltd.",
        "CPU = Intel(R) 8086, RAM = 640 KB",
        "640K System RAM Passed",
        "384K Extended RAM Passed",
        "Keyboard... Detected",
        "Mouse... Detected",
        "Fixed Disk 0: ST506",
        "ATAPI CD-ROM: Detected",
        "Detecting IDE Primary Master... OK",
        "Detecting IDE Primary Slave... None",
        "Detecting IDE Secondary Master... OK",
        "Detecting IDE Secondary Slave... None",
        "CMOS Battery... OK",
        "Initializing USB Controllers ... Done",
        "Boot from CD/DVD... Failed",
        "Boot from Hard Disk... OK",
    ]
    bios_lines = bios_lines or default_bios
    mem_checks = [
        "Performing Memory Test... ",
        "Checking Extended Memory... ",
        "Checking Cache Memory... ",
    ]
    # BIOS lines
    for line in bios_lines:
        console.print(Text(line, style=bios_color))
        await asyncio.sleep(delay)
    # Memory checks
    for line in mem_checks:
        console.print(Text(line, style=mem_color), end="")
        await asyncio.sleep(delay * 4)
        console.print(Text("[ OK ]", style="bold green"))
        await asyncio.sleep(delay)
    # Boot status
    if boot_ok:
        console.print(Text("\nBoot Device: Hard Disk - Success", style="bold green"))
    else:
        console.print(Text("\nBoot Device: Hard Disk - ERROR", style=error_color))
    await asyncio.sleep(delay * 3)
    # Final message
    console.print()
    console.print(Text(message, style=Style(color=highlight_color, bold=True)), justify="center")
    await asyncio.sleep(1.2)
