# Linux Jar File Manager 🫙

A unique, lightweight, and modular file manager built for Linux using **Python 3** and **PyQt6**. It features a creative visual metaphor where your personal files float at the top of the jar, while the heavy core operating system sits at the bottom.

## 🫙 The Metaphor

Unlike traditional twin-panel file managers, **Linux Jar File Manager** organizes your storage into two distinct vertical layers:

* **UPPER LAYER:** Your Home directory (`~`), where your everyday user files and scripts float safely.
* **LOWER LAYER:** The System Root (`/`), where the foundation of your operating system rests.

## ✨ Key Features

* **SATA & Hardware Integration:** Powered by native Linux tools like `findmnt`, it hooks directly into your kernel to detect and open hardware drives (such as your 240GB SATA SSD or internal NVMe) seamlessly without I/O locking or permission freezes.
* **Dynamic Space Monitor:** Features a sleek, responsive `QProgressBar` at the bottom of each panel that calculates total free/used disk space in gigabytes (GB) in real-time.
* **Multi-language Support (🌐 RO / EN / IT):** Full simetric internationalization. Switch instantly between Romanian, English, and Italian. All contextual menus, placeholders, and tooltips translate on the fly.
* **Instant Search & Filter:** A lightweight, non-blocking real-time filter bar. Start typing a keyword, and it instantly hides unmatched files from your current panel.
* **Full Action Toolbar:** Professional top-bar controls for **Move**, **New Folder**, **Delete**, and **Rename**, combined with a responsive Right-Click contextual menu.
* **Safe System Traversal:** Implements a strict permission bypass (`os.access`) ensuring the app opens massive system roots instantly without frozen UI warnings (Python is not responding).
* **Easter Egg Included:** Click on the bright red JAR OPERATOR title to uncover a special cultural warning about your pickles! 🥒
* **Smart Bookmarks & Favorites (⭐ v1.8.0):** Quick dropdown navigation menu located right next to fixed system paths. Save your favorite workspace folders dynamically with smart empty/filled star toggles (⭐/☆) and persistent JSON synchronization.
* **Secret Camouflage Mode (🎭 v1.9.0):** Hit **`F2`** to instantly hide your entire development workspace and file listings behind an innocent, fully internationalized dashboard showing traditional pickle recipes from Cecina! Press **`F2`** again to drop the disguise and return safely to your files.

## 📦 How to Install (.deb Package)

To install the official compiled package directly on any Debian/Ubuntu-based distribution (including elementary OS), follow these steps:

1. Download the latest `.deb` package file from this repository.
2. Open your terminal in the download directory and run:
   ```bash
   sudo dpkg -i linux-jar-file-manager_1.9.0_amd64.deb
   ```
3. Launch the application from your desktop applications menu or simply type `jar` in any terminal window!

## 📋 Prerequisites

Make sure you have Python 3 and PyQt6 installed on your Linux machine (Ubuntu, Linux Mint, Debian, etc.):

```bash
sudo apt update
sudo apt install python3-pyqt6
```

## 🚀 Installation & Running

Clone this project or navigate to your local repository directory, make the main window executable, and run it:

```bash
chmod +x main_window.py
./main_window.py
```

## 📦 How to Install (.deb Package)

To install the official compiled package directly on any Debian/Ubuntu-based distribution (including elementary OS), follow these steps:

1. Download the latest `.deb` package file from this repository.
2. Open your terminal in the download directory and run:
   ```bash
   sudo dpkg -i linux-jar-file-manager_1.9.0_amd64.deb
   ```
3. Launch the application from your desktop applications menu or simply type `jar` in any terminal window!
