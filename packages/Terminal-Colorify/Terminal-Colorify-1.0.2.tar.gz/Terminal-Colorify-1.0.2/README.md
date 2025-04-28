Terminal-Colorify 
Terminal-Colorify lets you add colors, backgrounds, gradients, rainbows, and animated effects to your Python terminal apps!

Features
Text color & background color

Bold, underline, blinking effects

Custom RGB colors

Rainbow text

Gradient text

Flashing text (animation)

Save styled text to files

Progress bars

Prebuilt theme styles

Installation
```
pip install Terminal-Colorify
```
Basic Usage


```
from colors import Colors
# Basic colored text
print(Colors.set_color(color="red", text="Red Text!"))

# Colored text with background
print(Colors.set_color(color="yellow", bg="blue", text="Yellow on Blue!"))

# Using RGB
print(Colors.set_color(rgb=(123, 45, 67), text="Custom RGB Color!"))

# Bold and Underline
print(Colors.set_color(color="green", text="Bold Underlined!", bold=True, underline=True))
```
# Advanced Features
```
# Rainbow text
print(Colors().rainbow_text("Rainbow magic "))

# Gradient text
print(Colors().gradient_text("Smooth Gradient!", start_color=(255, 0, 0), end_color=(0, 0, 255)))

# Flashing text
Colors().flashing_text("Warning!!!", color="red", flashes=5, speed=0.5)

# Save colorful text to a file
Colors().save_styled_text(
    text="Saved colorful text!",
    filename="output.txt",
    color="cyan",
    bg="black",
    bold=True
)

# Progress bar
Colors().progress_bar(total=50)

# Themes (prebuilt styles)
print(Colors().theme("warning", "Caution Ahead!"))
```
Available Themes:
warning — Yellow text with red background

info — Cyan text

success — Green bold text

error — Red bold underline text

neutral — White text, gray background

Color Names Available:
red

green

blue

yellow

magenta

cyan

white

black

gray

(plus any RGB you want!)

Perfect for CLI apps, games, fun terminals, and cool dev tools.
Let your text shine like never before !

