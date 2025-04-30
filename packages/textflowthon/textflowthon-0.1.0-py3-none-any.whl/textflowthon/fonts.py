import pyfiglet


def render_figlet(text: str, font: str) -> str:
    """
    Render text as ASCII art using the provided FIGlet font.

    Args:
        text (str): The text to render.
        font (str): The FIGlet font name (must be installed).

    Returns:
        str: The rendered ASCII art string. If font fails, returns plain text.
    """
    try:
        return pyfiglet.Figlet(font=font).renderText(text)
    except Exception:
        return text  # Fallback to plain text if font fails
