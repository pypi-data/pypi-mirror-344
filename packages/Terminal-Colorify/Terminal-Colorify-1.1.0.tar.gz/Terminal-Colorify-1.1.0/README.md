# Terminal-Colorify
```Terminal-Colorify``` is a simple and powerful python library to color your terminal output easily with RGB, gradients, rainbows, backgrounds, flashing text, themes, and more.

## Installation
```bash
pip install Terminal-Colorify
```

## Features

Set text color using RGB or predefined names

Set background color

Bold and underline styles

Generate random colors

Create gradient colored text

Create rainbow colored text

Flash text between two colors

Animated progress bar

Built-in themes (warning, success, info, error, etc.)

## Usage
```python
from colors import Colors
import time
# Set a named color
print(Colors.set_color(color="green", text="Green Text", bold=True, underline=True))

# Set a custom RGB color
print(Colors.set_color(rgb=(255, 0, 0), text="Custom Red"))

# Random color
print(Colors.set_color(color=Colors.random_color(), text="Random Color Text"))

# Gradient text
print(Colors.gradient_text("Gradient Text", (255, 0, 0), (0, 0, 255)))

# Rainbow text
print(Colors.rainbow_text("Rainbow Text!"))

# Flashing text
color = Colors()
color.flash_text("Flashing Text!", color1="red", color2="blue", times=5, delay=0.5)

# Progress bar
for i in range(101):
    color.progress_bar(i, color="green")
    time.sleep(0.05)
print()

# Apply a theme
print(Colors.apply_theme("success"))

# List all themes
Colors.list_themes()
```

## Available Themes

```warning``` — Yellow text with red background

```info``` — Cyan text

```success``` — Green bold text

```error``` — Red bold underline text

```neutral``` — White text with gray background

```dark```, ```light```, ```ocean```, ```coolblue```, ```sunset```, ```mint``` and more

## License

##### This project is open source and available under the MIT License.