# Columns: A Full-Stack Python Game

A graphical implementation of the classic puzzle game **Columns**, built with Python and the **Pygame** library. This project focuses on the strict separation of game logic from graphical rendering, utilizing Object-Oriented Programming (OOP) to create a scalable and maintainable codebase.

---

## 🚀 Features

* **MVC Architecture**: Strict separation between the game engine (`columns_logic.py`) and the graphical user interface (`project5.py`).
* **Robust Game Logic**: Complex matching algorithms that detect vertical, horizontal, and diagonal matches of 3 or more jewels.
* **Real-time Physics**: Implementation of "Falling," "Landed," and "Frozen" states for the game's fallers.
* **Dynamic Rendering**: Supports window resizing with automatic graphical scaling to fit the new aspect ratio.
* **User Interaction**: Real-time event handling for keyboard inputs (Arrow keys and Spacebar).

---

## 🛠️ Technical Stack

* **Language**: Python 3.13
* **Libraries**: [Pygame](https://www.pygame.org/)
* **Design Patterns**: Model-View-Controller (MVC), State Management, Event-Driven Programming.

---

## 🎮 How to Play

### Installation

1. Ensure you have **Python 3.13** (or later) installed.
2. Install the Pygame library using pip:

```bash
pip install pygame
```

### Running the Game

Navigate to the `src` folder and execute the main script:

```bash
python project5.py
```

### Controls

| Key | Action |
| :--- | :--- |
| **Left / Right Arrows** | Move the faller horizontally |
| **Spacebar** | Rotate the jewels within the faller |
| **Gravity** | The game "ticks" every second, causing the faller to descend |

---

## 🧠 Key Learnings

* **Algorithmic Efficiency**: Optimized the matching logic to efficiently scan the 2D grid after every "freeze" state.
* **Collision Detection**: Managed the complex interaction between the moving faller and the static frozen jewels on the board.
* **Version Control**: Leveraged Git for repository management, ensuring a clean and professional commit history.
