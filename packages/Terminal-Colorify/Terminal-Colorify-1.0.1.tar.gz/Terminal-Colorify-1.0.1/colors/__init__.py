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
        "purple": (128, 0, 128)
    }

    themes = {
        "dark": {"color": "white", "bg": "black"},
        "light": {"color": "black", "bg": "white"},
        "ocean": {"color": "cyan", "bg": "blue"},
    }

    @classmethod
    def set_color(cls, text="", color=None, rgb=None, bg=None, bg_rgb=None, bold=False, underline=False, start_color=None, end_color=None):
        if start_color and end_color:
            return cls.gradient_text(text, start_color, end_color, bold, underline)
        else:
            return cls.style(text, color, rgb, bg, bg_rgb, bold, underline)

    @classmethod
    def style(cls, text, color=None, rgb=None, bg=None, bg_rgb=None, bold=False, underline=False):
        style_code = ""

        # Text color
        if rgb:
            r, g, b = rgb
            style_code += f"\033[38;2;{r};{g};{b}m"
        elif color:
            r, g, b = cls.color_map.get(color.lower(), (255, 255, 255))
            style_code += f"\033[38;2;{r};{g};{b}m"

        # Background color
        if bg_rgb:
            r, g, b = bg_rgb
            style_code += f"\033[48;2;{r};{g};{b}m"
        elif bg:
            r, g, b = cls.color_map.get(bg.lower(), (0, 0, 0))
            style_code += f"\033[48;2;{r};{g};{b}m"

        if bold:
            style_code += "\033[1m"
        if underline:
            style_code += "\033[4m"

        return f"{style_code}{text}\033[0m"

    @classmethod
    def gradient_text(cls, text, start_color, end_color, bold=False, underline=False):
        gradient_text = ""
        length = max(len(text), 1)
        r1, g1, b1 = start_color
        r2, g2, b2 = end_color

        for i, char in enumerate(text):
            r = int(r1 + (r2 - r1) * i / length)
            g = int(g1 + (g2 - g1) * i / length)
            b = int(b1 + (b2 - b1) * i / length)

            style_code = f"\033[38;2;{r};{g};{b}m"
            if bold:
                style_code += "\033[1m"
            if underline:
                style_code += "\033[4m"

            gradient_text += f"{style_code}{char}"

        return gradient_text + "\033[0m"

    @classmethod
    def random_color(cls):
        return random.choice(list(cls.color_map.keys()))

    def rainbow_text(self, text):
        rainbow_colors = ["red", "yellow", "green", "cyan", "blue", "magenta"]
        colored_text = ""

        for i, char in enumerate(text):
            color = rainbow_colors[i % len(rainbow_colors)]
            colored_text += Colors.style(char, color=color)

        return colored_text

    def save_to_file(self, text, filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)

    def flash_text(self, text, color1="red", color2="blue", flashes=5, delay=0.5):
        for _ in range(flashes):
            print(Colors.style(text, color=color1), end="\r")
            time.sleep(delay)
            print(Colors.style(text, color=color2), end="\r")
            time.sleep(delay)
        print(Colors.style(text, color=color1))

    def progress_bar(self, percent, color="green", width=30):
        filled_length = int(width * percent // 100)
        bar = '█' * filled_length + '-' * (width - filled_length)
        print(f"\r{Colors.style(f'|{bar}| {percent}%', color=color)}", end="\r")
        if percent == 100:
            print()

    def apply_theme(self, theme_name):
        theme = Colors.themes.get(theme_name.lower())
        if not theme:
            return "Theme not found."
        return Colors.set_color(text=f"Applied {theme_name} theme", color=theme["color"], bg=theme["bg"])

