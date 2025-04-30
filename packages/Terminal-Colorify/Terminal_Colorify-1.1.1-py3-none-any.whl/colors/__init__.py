import sys
import random
import time

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

    themes = {
        "dark": {"color": "white"},
        "light": {"color": "black"},
        "ocean": {"rgb": (0, 128, 255)},
        "warning": {"color": "yellow", "bg": "red", "bold": True},
        "info": {"color": "cyan"},
        "success": {"color": "green", "bold": True},
        "error": {"color": "red", "bold": True, "underline": True},
        "neutral": {"color": "white", "bg": "gray"},
        "coolblue": {"color": "blue", "bg": "cyan"},
        "sunset": {"color": "magenta", "bg": "yellow", "bold": True},
        "mint": {"color": "green", "bg": "cyan"},
    }

    def __init__(self):
        self.color = ""
        self.rgb = None
        self.bg = ""
        self.bg_rgb = None
        self.bold = False
        self.underline = False

    @classmethod
    def set_color(cls, color=None, text="", rgb=None, bg=None, bg_rgb=None, bold=False, underline=False):
        style_code = ""

        # Text color
        if rgb:
            r, g, b = rgb
            style_code += f"\033[38;2;{r};{g};{b}m"
        elif color and color in cls.color_map:
            r, g, b = cls.color_map[color]
            style_code += f"\033[38;2;{r};{g};{b}m"

        # Background color
        if bg_rgb:
            r, g, b = bg_rgb
            style_code += f"\033[48;2;{r};{g};{b}m"
        elif bg and bg in cls.color_map:
            r, g, b = cls.color_map[bg]
            style_code += f"\033[48;2;{r};{g};{b}m"

        # Bold
        if bold:
            style_code += "\033[1m"

        # Underline
        if underline:
            style_code += "\033[4m"

        return f"{style_code}{text}\033[0m"

    @classmethod
    def random_color(cls):
        return random.choice(list(cls.color_map.keys()))

    @classmethod
    def gradient_text(cls, text, start_color, end_color):
        result = ""
        length = len(text)
        for i, char in enumerate(text):
            r = int(start_color[0] + (end_color[0] - start_color[0]) * i / max(length - 1, 1))
            g = int(start_color[1] + (end_color[1] - start_color[1]) * i / max(length - 1, 1))
            b = int(start_color[2] + (end_color[2] - start_color[2]) * i / max(length - 1, 1))
            result += f"\033[38;2;{r};{g};{b}m{char}"
        return result + "\033[0m"

    @classmethod
    def rainbow_text(cls, text):
        rainbow_colors = [
            (255, 0, 0), (255, 127, 0), (255, 255, 0),
            (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)
        ]
        result = ""
        for i, char in enumerate(text):
            r, g, b = rainbow_colors[i % len(rainbow_colors)]
            result += f"\033[38;2;{r};{g};{b}m{char}"
        return result + "\033[0m"

    def flash_text(self, text, color1="red", color2="blue", times=5, delay=0.5):
        for _ in range(times):
            sys.stdout.write("\r" + self.set_color(color=color1, text=text))
            sys.stdout.flush()
            time.sleep(delay)
            sys.stdout.write("\r" + self.set_color(color=color2, text=text))
            sys.stdout.flush()
            time.sleep(delay)
        print("\033[0m")  # Reset at end

    def progress_bar(self, percent, color="green", bar_color="gray", width=30):
        done = int(width * percent / 100)
        filled = "=" * done
        empty = " " * (width - done)

        # color for the inside bar
        bar_text = self.set_color(color=color, text=filled + empty)

        # color for the brackets
        left_bracket = self.set_color(color=bar_color, text="[")
        right_bracket = self.set_color(color=bar_color, text="]")

        sys.stdout.write(f"\r{left_bracket}{bar_text}{right_bracket} {percent}%")
        sys.stdout.flush()

    @classmethod
    def apply_theme(cls, theme_name, text="Sample Text"):
        theme = cls.themes.get(theme_name.lower())
        if not theme:
            return f"Theme '{theme_name}' not found."
        return cls.set_color(
            color=theme.get("color"),
            bg=theme.get("bg"),
            rgb=theme.get("rgb"),
            bg_rgb=theme.get("bg_rgb"),
            bold=theme.get("bold", False),
            underline=theme.get("underline", False),
            text=text
        )

    @classmethod
    def list_themes(cls):
        print("Available Themes:")
        for name in cls.themes:
            preview = cls.apply_theme(name, text=name.capitalize())
            print(f"  {preview}")

    def bg_progress_bar(self, percent, color="green", bar_color="gray", width=30):
        char = "G"
        done = int(width * percent / 100)
        remaining = width - done

        # Fill color (char and background same)
        if color in self.color_map:
            r, g, b = self.color_map[color]
            fill = f"\033[38;2;{r};{g};{b}m\033[48;2;{r};{g};{b}m{char * done}\033[0m"
        else:
            fill = char * done

        # Unfilled part with no color
        empty = " " * remaining

        # Brackets foreground color
        if bar_color in self.color_map:
            r2, g2, b2 = self.color_map[bar_color]
            bracket_color = f"\033[38;2;{r2};{g2};{b2}m"
        else:
            bracket_color = ""

        # Output with colored brackets
        sys.stdout.write(
            f"\r{bracket_color}[{fill}{empty}{bracket_color}]{self.set_color(text=f' {percent}%', color=color)}")
        sys.stdout.flush()


