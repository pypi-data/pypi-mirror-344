import random
import time
import sys


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
        "orange": (255, 165, 0),
        "violet": (238, 130, 238),
        "indigo": (75, 0, 130),
    }

    def __init__(self):
        self.color = ""
        self.rgb = None
        self.bg = ""
        self.bg_rgb = None
        self.bold = False
        self.underline = False
        self.blink = False
        self.invert = False

    @classmethod
    def set_color(cls, color=None, text="", rgb=None, bold=False, underline=False, bg=None, bg_rgb=None, blink=False, invert=False):
        color_instance = cls()
        color_instance.color = color.lower() if color else ""
        color_instance.rgb = rgb
        color_instance.bold = bold
        color_instance.underline = underline
        color_instance.blink = blink
        color_instance.invert = invert
        color_instance.bg = bg
        color_instance.bg_rgb = bg_rgb
        return color_instance.style(text)

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

        # Background color
        if self.bg_rgb:
            r, g, b = self.bg_rgb
        elif self.bg:
            r, g, b = Colors.color_map.get(self.bg, (0, 0, 0))  # Default to black
        style_code += f"\033[48;2;{r};{g};{b}m"

        # Bold
        if self.bold:
            style_code += "\033[1m"

        # Underline
        if self.underline:
            style_code += "\033[4m"

        # Blinking Text
        if self.blink:
            style_code += "\033[5m"

        # Inverted colors
        if self.invert:
            style_code += "\033[7m"

        return f"{style_code}{text}\033[0m"

    # Random color generator
    @staticmethod
    def random_color():
        return random.choice(list(Colors.color_map.keys()))

    # Gradient text
    def gradient_text(self, text, start_rgb, end_rgb):
        gradient_text = ""
        text_length = len(text)
        for i in range(text_length):
            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * (i / text_length))
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * (i / text_length))
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * (i / text_length))
            gradient_text += f"\033[38;2;{r};{g};{b}m{text[i]}"
        return f"{gradient_text}\033[0m"

    # Rainbow text
    def rainbow_text(self, text):
        rainbow = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
        rainbow_text = ""
        color_index = 0
        for char in text:
            color = rainbow[color_index % len(rainbow)]
            rainbow_text += self.set_color(color=color, text=char)
            color_index += 1
        return rainbow_text

    # Save styled text to a file
    def save_to_file(self, text, filename="styled_output.txt"):
        styled_text = self.style(text)
        with open(filename, "w") as file:
            file.write(styled_text)
        print(f"Styled text saved to {filename}")

    # Flash the terminal text between two colors
    def flash_text(self, text, color1="red", color2="blue", delay=0.5, repeat=5):
        for _ in range(repeat):
            print(self.set_color(color=color1, text=text))
            time.sleep(delay)
            print(self.set_color(color=color2, text=text))
            time.sleep(delay)

    # Animated progress bar
    def progress_bar(self, total=100, color="green"):
        for i in range(total + 1):
            percent = (i / total) * 100
            bar = "#" * int(i / total * 40)
            sys.stdout.write(f"\r[{bar:<40}] {percent:.2f}%")
            sys.stdout.flush()
            time.sleep(0.1)
        print()

    # Apply predefined themes (dark, light, ocean)
    def apply_theme(self, theme="dark"):
        themes = {
            "dark": {"fg": "white", "bg": "black"},
            "light": {"fg": "black", "bg": "white"},
            "ocean": {"fg": "cyan", "bg": "blue"},
        }
        theme_colors = themes.get(theme, themes["dark"])
        return self.set_color(color=theme_colors["fg"], bg=theme_colors["bg"], text="This is a themed text!")


# Example usage:

# Color text with random color
print(Colors.set_color(color=Colors.random_color(), text="Random Color Text"))

# Gradient text from red to blue
print(Colors.set_color(text="Gradient Text", rgb=(255, 0, 0)))
print(Colors().gradient_text("This is a gradient", (255, 0, 0), (0, 0, 255)))

# Rainbow text
print(Colors().rainbow_text("This is rainbow text!"))

# Save styled text to file
color = Colors()
color.save_to_file("This text is saved with color!", "color_text.txt")

# Flashing text
color.flash_text("Flashing Text!", color1="red", color2="blue")

# Animated progress bar
color.progress_bar(50, color="green")

# Predefined themes
print(color.apply_theme("dark"))
print(color.apply_theme("light"))
print(color.apply_theme("ocean"))
