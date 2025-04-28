# Terminal-Colorify

A simple Python module for adding colors to text in the terminal.

## Installation and Usage

```bash
# Install the package
pip install Terminal-Colorify
```

# Example Python usage
```
import colors
```

# Set a simple color
```
print(colors.Colors.set_color("yellow", "Hello, world!"))
```

# Set RGB color
```
print(colors.Colors.set_color(rgb=(255, 0, 0), text="Red Text"))
```

# Use bold and underline styles
```
print(colors.Colors.set_color("blue", "Bold Blue Text", bold=True))
print(colors.Colors.set_color("green", "Underlined Green Text", underline=True))
```