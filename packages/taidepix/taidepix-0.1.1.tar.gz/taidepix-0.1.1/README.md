# Taidepix

A command-line interface (CLI) tool for applying various dithering algorithms to images and displaying the results directly in your terminal using ASCII, block characters, Braille patterns, or full color.

## Features

*   **Multiple Dithering Algorithms:**
    *   Floyd-Steinberg
    *   Simple Threshold
    *   Random Dithering
    *   Ordered Dithering (Bayer Matrix)
    *   Atkinson
    *   Burkes
    *   Sierra
    *   Jarvis, Judice, and Ninke (JJN)
    *   Stucki
*   **Flexible Output Modes:**
    *   Standard ASCII characters (`--charset ascii`)
    *   Block characters (`--charset blocks`)
    *   Braille patterns for higher detail (`--charset braille`)
    *   Full 24-bit color output (`--color`)
*   **Customizable Output Width:** Control the width of the terminal output.

## Installation

You can install Taidepix directly from PyPI using pip:

```bash
pip install taidepix
```

Or, if you prefer to install CLI tools in isolated environments, you can use pipx:

```bash
pipx install taidepix
```

**Development Installation:**

If you want to install it for development (e.g., after cloning the repository):

```bash
# Clone the repository (if you haven't already)
# git clone https://github.com/Aresga/Taidepix/
# cd Taidepix

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install in editable mode
pip install -e .
```

## Dependencies

*   [Pillow](https://python-pillow.org/) (>=9.0.0)
*   [NumPy](https://numpy.org/) (>=1.21.0)

These will be installed automatically when you install Taidepix using pip.

## Usage

The basic command structure is:

```bash
taidepix <image_path> [options]
```

**Arguments:**

*   `image_path`: (Required) Path to the input image file.

**Options:**

*   `--width` or `-w`: Set the output width in characters (default: 80).
*   `--algorithm` or `-a`: Choose the dithering algorithm (default: `floyd_steinberg`). Available: `floyd_steinberg`, `simple_threshold`, `random`, `ordered`, `atkinson`, `burkes`, `sierra`, `jjn`, `stucki`.
*   `--charset` or `-c`: Choose the character set for non-color output (default: `ascii`). Available: `ascii`, `blocks`, `braille`.
*   `--color`: Enable 24-bit color output (uses block characters, overrides dithering and charset).
*   `--version`: Show the program's version number and exit.
*   `--help` or `-h`: Show the help message and exit.

**Examples:**

```bash
# Dither 'image.jpg' using Floyd-Steinberg (default) and ASCII output
taidepix pictures/image.jpg

# Dither 'photo.png' using Atkinson dithering, width 100, block characters
taidepix photo.png -w 100 -a atkinson -c blocks

# Display 'logo.gif' using Braille characters
taidepix logo.gif --charset braille

# Display 'art.tif' in full color
taidepix art.tif --color

# Dither 'scenery.jpeg' using Stucki algorithm, width 120
taidepix scenery.jpeg -a stucki -w 120
```

## Screenshots

Here are some examples of Taidepix in action:

**ASCII Output:**
![Taidepix ASCII output example](screenshots/Screenshot%202025-04-27%20at%2019.12.39.png)

**Block Character Output:**
![Taidepix Block character output example](screenshots/Screenshot%202025-04-27%20at%2019.14.09.png)

**Color Output:**
![Taidepix Color output example](screenshots/Screenshot%202025-04-27%20at%2019.15.24.png)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
