from rich.color import Color
import warnings

def derive_rain_trail_colors(fg: str) -> list[str]:
    """
    Derive trail colors for Matrix rain effect from the fg color.

    The trail consists of:
    - bold fg (for the lead)
    - normal fg
    - dim fg
    - '#003300' (Matrix green fade)
    - '#001a00' (Matrix green fade)

    If the fg color cannot be parsed, falls back to fg for the first three.
    Logs a warning if color parsing fails.

    Args:
        fg (str): Foreground color for the rain effect.

    Returns:
        list[str]: List of color styles for the rain trail.
    """
    try:
        _ = Color.parse(fg)
        return [
            f"bold {fg}",
            fg,
            f"dim {fg}",
            "#003300",
            "#001a00"
        ]
    except Exception:
        warnings.warn(f"[TextFlowThon] Could not parse fg color '{fg}', falling back to plain color.")
        return [fg, fg, fg, "#003300", "#001a00"]
