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

    def set_color(self, color=None, text="", rgb=None, bold=False, underline=False):
        if color:
            self.color = color.lower() if color in Colors.color_map else ""
        if rgb:
            self.rgb = rgb
        self.bold = bold
        self.underline = underline
        return self.style(text)

    def style(self, text):
        style_code = ""

        # Determine RGB (use color_map if no rgb is provided)
        if self.rgb:
            r, g, b = self.rgb
        elif self.color:
            r, g, b = Colors.color_map.get(self.color, (255, 255, 255))  # Default to white
        else:
            r, g, b = (255, 255, 255)  # Default to white

        # Color
        style_code += f"\033[38;2;{r};{g};{b}m"

        # Bold
        if self.bold:
            style_code += "\033[1m"

        # Underline
        if self.underline:
            style_code += "\033[4m"

        return f"{style_code}{text}\033[0m"


# Create an instance of Colors globally
color = Colors()

# Example usage with named color
print(color.set_color(color="green", text="Green Text", bold=True, underline=True))

# Example usage with custom RGB
print(color.set_color(rgb=(255, 0, 0), text="Custom RGB Red Text", bold=True, underline=True))
