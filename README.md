# Checkers Game

A Python implementation of the classic Checkers game with an AI opponent, built using Pygame.

## Features

- Classic 8x8 Checkers gameplay
- Red (human) vs White (AI) gameplay
- Visual highlights for valid moves
- Turn indicator and piece counters
- Win detection
- Reset button
- Simple AI opponent using minimax algorithm

## Installation Instructions

### Prerequisites

Before running the game, you'll need to have Python and pip installed on your system.

#### Installing Python and pip

1. **For Windows:**
   - Download Python from [python.org](https://www.python.org/downloads/)
   - Run the installer
   - Check "Add Python to PATH" during installation
   - Python and pip will be installed automatically

2. **For macOS:**
   - Python is pre-installed, but it's recommended to install the latest version:
     - Using Homebrew: `brew install python`
     - Or download from [python.org](https://www.python.org/downloads/macos/)
   - pip will be included with the installation

3. **For Linux (Ubuntu/Debian):**
   - Open terminal and run:
     ```bash
     sudo apt update
     sudo apt install python3 python3-pip
     ```

### Installing the Game

1. **Clone or download the repository**
   - If you have git installed:
     ```bash
     git clone https://github.com/2005Andrei/checkers.git
     cd checkers-game
     ```
   - Or download the ZIP file and extract it

2. **Install required dependencies**
   - Open terminal at folder and run in your terminal/command prompt:
    ```bash
    pip install -r requirements.txt
    ```
   - Run the following command in your terminal/command prompt:
     ```bash
     pip install pygame numpy
     ```

## How to Run the Game

1. Navigate to the game directory in your terminal/command prompt
2. Run the game with:
   ```bash
   python checkers.py
   ```

## Gameplay

- Red pieces are controlled by the human player
- White player pieces are controlled by the AI
- Red moves first
- Click the "Reset" button at the bottom right to reset the game

## Potential issues

1. Python not found
    - Ensure python is installed and on your PATH
    - Try running with python3 instead of python, or vice versa
2. Pygame installation fails
    - Try upgrading pip first with ```bash pip install --upgrade pip```
    - Then try installing Pygame again


Enjoy the game!