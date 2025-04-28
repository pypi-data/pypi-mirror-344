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

    def __init__(self):
        self.color = ""
        self.rgb = None
        self.bg = ""
        self.bg_rgb = None
        self.bold = False
        self.underline = False

    def set_color(self, color, text):
        self.color = color.lower() if color in Colors.color_map else ""
        return self.style(text)

    def style(self, text):
        style_code = ""

        if self.color:
            r, g, b = Colors.color_map.get(self.color, (255, 255, 255))
            style_code += f"\033[38;2;{r};{g};{b}m"

        return f"{style_code}{text}\033[0m"


# Create an instance of Colors globally
color = Colors()
