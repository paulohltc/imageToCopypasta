# imageToCopypasta

This code transforms an image to a copypasta (unicode art) that fits in Twitch and Google meet chat.






## Character used

[Repl.it link, click in run](https://repl.it/@lehydra/unicodeCharacter#main.py)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install OpenCV.

```bash
pip install opencv-python
```

## Usage

```bash
python -ht ht -lt lt -g g
```

In where "ht" is the high threshold value of intensity gradient, "lt" is the low threshold value gradient and "g" for the grayscale you want to highlight (either 0 or 255, default is 0).

In the example used in "output.txt", it was used these parameters:

```bash
python -ht 50 -lt 150 -g 255
```

