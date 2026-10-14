# 🔐 Python Password Generator (CLI & GUI)

A secure, customizable, and modern Password Generator application built with Python. Features both an interactive **Terminal / CLI** version (with command-line arguments and interactive menus) and a sleek **Desktop GUI** version built with Tkinter.

---

## ✨ Features

- **Cryptographically Secure:** Powered by Python's `secrets` module for high-grade randomness.
- **Multiple Generation Modes:**
  - **Custom Passwords:** Mix uppercase, lowercase, numbers, and symbols.
  - **Memorable Passphrases:** Diceware-style passphrase generation (e.g. `Valley-Feather-Legend89-Phoenix`).
  - **PIN Codes:** Quick numeric PIN generation of any length.
- **Password Strength & Entropy Analyzer:**
  - Real-time Shannon Entropy calculation (bits).
  - Dynamic strength score (Very Weak, Weak, Moderate, Strong, Very Strong).
- **Ambiguous Character Filter:** Option to exclude easily confused characters (`1`, `l`, `I`, `0`, `O`).
- **Bulk Generation:** Generate multiple passwords at once and copy them easily.
- **Clipboard Integration:** Instant one-click copy to clipboard with visual confirmation.
- **Modern Dark GUI (Tkinter):**
  - Dark mode aesthetic (Catppuccin Mocha theme).
  - Live length & word count sliders.
  - Interactive strength gauge bar.
  - 100% standard library (zero external pip packages required).

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher installed on your system.

### How to Run

1. **Interactive CLI Version:**
   ```bash
   python passwordGenerator.py
   ```

2. **CLI with Arguments (Quick Generation):**
   ```bash
   # Generate 16-character password (default)
   python passwordGenerator.py -l 16

   # Generate 3 strong passwords of length 20
   python passwordGenerator.py -l 20 -c 3

   # Exclude ambiguous characters (1, l, I, 0, O)
   python passwordGenerator.py -l 16 --exclude-ambiguous

   # Generate memorable 4-word passphrase
   python passwordGenerator.py --passphrase -w 4

   # Generate 6-digit numeric PIN
   python passwordGenerator.py --pin 6
   ```

3. **Desktop GUI Version:**
   ```bash
   python gui_password_generator.py
   ```
   *(or run `python passwordGenerator.py --gui`)*

---

## 🛠️ Built With
- **Python 3** (Standard Library: `secrets`, `math`, `string`, `tkinter`, `argparse`)
