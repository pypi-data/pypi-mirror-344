# Utility functions for TextFlowThon

def clear_line(console) -> None:
    """
    Clear the current line in the terminal for the given Rich Console.

    Args:
        console (Console): The Rich Console to clear the line on.
    """
    console.file.write("\x1b[K")
    console.file.flush()
