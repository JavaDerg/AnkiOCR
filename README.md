# AnkiOCR

<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

## Introduction
Create an [Anki](https://github.com/ankitects/anki "Anki")-Learn-Deck fully automatic from existing cards with Optical-Character-Recognition.
## Getting Started

### Pre-requisites
- Python 3.7+
- Pytesseract with your needed Language Package`sudo apt install tesseract-ocr-[language code]`
- Anki-Desktop

### Installation
- Go to the [Release Section](https://github.com/Hugo54x/AnkiOCR/releases "Release Section") and grab a copy of this project.
- Extract the archive and open a command prompt in the folder (`Shift + Right Click`on Windows). 
- Run `pip3 install -r requirements.txt`

### Usage
- Put your `.jpg` Files into `./img/`
- Run `python3 ./AnkiOCR.py`
- Import `./output.csv` into Anki-Desktop

## FAQ
Q: Can I create my own keywords list?
A: Sure, follow the guide in the [Wiki](https://github.com/hugo54x/AnkiOCR/wiki/ "Wiki").

Q: Can I use AnkiOCR with my existing hand-written cards?
A: At the moment not.

Q: Will there be Multi-Threading/Processing?
A: At the moment Pytesseract is using multiple cores. It has to be measured, if for the other parts of the code the speed improvements are justifying the additional work.
## Contact
Check out my [Github Proflie](https://github.com/Hugo54x "Github Proflie").
## License
This project is licensed under a custom license. See [LICENSE.md](https://github.com/Hugo54x/AnkiOCR/blob/main/LICENSE.md "LICENSE.md") for more infos.
