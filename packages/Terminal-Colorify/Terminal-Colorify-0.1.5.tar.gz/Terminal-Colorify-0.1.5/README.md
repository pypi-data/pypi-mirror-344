# Terminal-Colorify

A simple Python module for adding colors to text in the terminal.

## Installation and Usage

# Install the package
```bash
pip install Terminal-Colorify
```

# Example Python usage
```
import colors
```

# Set a simple color
```
print(Colors.set_color("yellow", "Hello, world!"))
```

# Set RGB color
```
print(Colors.set_color(rgb=(255, 0, 0), text="Red Text"))
```

# Use bold and underline styles
```
print(Colors.set_color("blue", "Bold Blue Text", bold=True))
print(Colors.set_color("green", "Underlined Green Text", underline=True))
```