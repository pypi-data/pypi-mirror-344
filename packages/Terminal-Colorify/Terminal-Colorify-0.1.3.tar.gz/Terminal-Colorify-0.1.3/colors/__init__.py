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

    @staticmethod
    def set_color(color, text):
        # Make color lowercase for case insensitivity
        color = color.lower() if color in Colors.color_map else ""
        return Colors.style(color, text)

    @staticmethod
    def style(color, text):
        style_code = ""

        if color:
            r, g, b = Colors.color_map.get(color, (255, 255, 255))
            style_code += f"\033[38;2;{r};{g};{b}m"

        return f"{style_code}{text}\033[0m"
