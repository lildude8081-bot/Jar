# Linux Jar File Manager 🫙

A unique, lightweight, and modular file manager built for Linux using **Python 3** and **PyQt6**. It features a creative visual metaphor where your personal files float at the top of the jar, while the heavy core operating system sits at the bottom.

## 🫙 The Metaphor
Unlike traditional twin-panel file managers, **Linux Jar File Manager** organizes your storage into two distinct vertical layers:
*   **UPPER LAYER:** Your Home directory (`~/`), where your everyday user files and scripts float safely.
*   **LOWER LAYER:** The System Root (`/`), where the foundation of your operating system rests.

## ✨ Key Features
*   **SATA & Hardware Integration:** Powered by native Linux tools like `findmnt`, it hooks directly into your kernel to detect and open hardware drives (such as your 240GB SATA SSD or internal NVMe) seamlessly without I/O locking or permission freezes.
*   **Dynamic Space Monitor:** Features a sleek, responsive `QProgressBar` at the bottom of each panel that calculates total free/used disk space in gigabytes (GB) in real-time.
*   **Multi-language Support (🌐 RO / EN / IT):** Full simetric internationalization. Switch instantly between Romanian, English, and Italian. All contextual menus, placeholders, and tooltips translate on the fly.
*   **Instant Search & Filter:** A lightweight, non-blocking real-time filter bar. Start typing a keyword, and it instantly hides unmatched files from your current panel.
*   **Full Action Toolbar:** Professional top-bar controls for **Move**, **New Folder**, **Delete**, and **Rename**, combined with a responsive Right-Click contextual menu.
*   **Safe System Traversal:** Implements a strict permission bypass (`os.access`) ensuring the app opens massive system roots instantly without frozen UI warnings (*Python is not responding*).
*   **Easter Egg Included:** Click on the bright red **JAR OPERATOR** title to uncover a special cultural warning about your pickles! 🥒

## 🚀 Getting Started

### Prerequisites
Make sure you have Python 3 and PyQt6 installed on your Linux machine (Ubuntu, Linux Mint, Debian, etc.):
```bash
sudo apt update
sudo apt install python3-pyqt6
```

### Installation & Running
Clone this project or navigate to your local repository directory, make the main window executable, and run it:
```bash
chmod +x main_window.py
./main_window.py
```
