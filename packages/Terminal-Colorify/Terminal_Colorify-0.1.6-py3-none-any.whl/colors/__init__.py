class Colors:
    color_map = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "magenta": (255, 0, 255),
        "cyan": (0, 255, 255),
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "gray": (169, 169, 169),
    }

    @classmethod
    def set_color(cls, color=None, text="", rgb=None, bold=False, underline=False):
        style_code = ""

        # Determine RGB
        if rgb:
            r, g, b = rgb
        elif color:
            r, g, b = cls.color_map.get(color.lower(), (255, 255, 255))
        else:
            r, g, b = (255, 255, 255)

        # Color
        style_code += f"\033[38;2;{r};{g};{b}m"

        # Bold
        if bold:
            style_code += "\033[1m"

        # Underline
        if underline:
            style_code += "\033[4m"

        return f"{style_code}{text}\033[0m"


