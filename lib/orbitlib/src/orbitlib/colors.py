


from dataclasses import dataclass


@dataclass
class Colors:
    """Class to hold all color constants."""
    BACKGROUND: tuple[int, int, int] = (0, 0, 0)
    FOREGROUND: tuple[int, int, int] = (255, 255, 255)
    GRID: tuple[int, int, int] = (50, 50, 50)
    SELECTION: tuple[int, int, int] = (255, 0, 0)
    

    RED: tuple[int, int, int] = (255, 0, 0)
    LIGHT_RED: tuple[int, int, int] = (255, 102, 102)
    DARK_RED: tuple[int, int, int] = (153, 0, 0)
    
    ORANGE: tuple[int, int, int] = (255, 165, 0)
    LIGHT_ORANGE: tuple[int, int, int] = (255, 204, 153)
    DARK_ORANGE: tuple[int, int, int] = (204, 119, 34)
    
    GREEN: tuple[int, int, int] = (0, 255, 0)
    LIGHT_GREEN: tuple[int, int, int] = (102, 255, 102)
    DARK_GREEN: tuple[int, int, int] = (0, 153, 0)
    
    BLUE: tuple[int, int, int] = (0, 0, 255)
    LIGHT_BLUE: tuple[int, int, int] = (102, 102, 255)
    DARK_BLUE: tuple[int, int, int] = (0, 0, 153)

    CYAN: tuple[int, int, int] = (0, 255, 255)
    LIGHT_CYAN: tuple[int, int, int] = (102, 255, 255)
    DARK_CYAN: tuple[int, int, int] = (0, 153, 153)

    YELLOW: tuple[int, int, int] = (255, 255, 0)
    LIGHT_YELLOW: tuple[int, int, int] = (255, 255, 102)
    DARK_YELLOW: tuple[int, int, int] = (204, 204, 0)

    MAGENTA: tuple[int, int, int] = (255, 0, 255)
    LIGHT_MAGENTA: tuple[int, int, int] = (255, 102, 255)
    DARK_MAGENTA: tuple[int, int, int] = (153, 0, 153)

    PURPLE: tuple[int, int, int] = (128, 0, 128)
    LIGHT_PURPLE: tuple[int, int, int] = (204, 153, 255)
    DARK_PURPLE: tuple[int, int, int] = (75, 0, 130)

    BROWN: tuple[int, int, int] = (165, 42, 42)
    LIGHT_BROWN: tuple[int, int, int] = (222, 184, 135)
    DARK_BROWN: tuple[int, int, int] = (101, 67, 33)

    WHITE: tuple[int, int, int] = (255, 255, 255)
    BLACK: tuple[int, int, int] = (0, 0, 0)
    LIGHT_GRAY: tuple[int, int, int] = (211, 211, 211)
    DARK_GRAY: tuple[int, int, int] = (169, 169, 169)
