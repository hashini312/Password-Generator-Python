import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import string
import math
# Common wordlist for Diceware-style passphrase generation
MEMORABLE_WORDS = [
    "amber", "anchor", "apple", "beacon", "breeze", "bridge", "cactus", "castle",
    "cedar", "cloud", "clover", "comet", "coral", "crystal", "delta", "desert",
    "dolphin", "dragon", "eagle", "echo", "ember", "falcon", "feather", "flame",
    "forest", "fossil", "galaxy", "garden", "glacier", "granite", "harbor", "haven",
    "island", "jasper", "jungle", "lagoon", "lantern", "legend", "lotus", "meadow",
    "meteor", "moon", "nebula", "nexus", "oasis", "ocean", "orbit", "peak",
    "pebble", "phoenix", "planet", "prism", "quartz", "radar", "rainbow", "raven",
    "reef", "ridge", "river", "ruby", "sable", "sailor", "sapphire", "shadow",
    "shield", "sierra", "silver", "solar", "spark", "sphinx", "spirit", "star",
    "storm", "summit", "sunset", "thunder", "tiger", "timber", "titan", "topaz",
    "tower", "trail", "valley", "vapor", "velvet", "venture", "vessel", "vortex",
    "whisper", "willow", "winter", "wizard", "zenith", "zephyr"
]

AMBIGUOUS_CHARS = "il1Lo0O"

def calculate_entropy(password: str) -> float:
    """Calculate the information entropy (in bits) of a password."""
    if not password:
        return 0.0

    pool_size = 0
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)
    has_space = " " in password

    if has_lower:
        pool_size += 26
    if has_upper:
        pool_size += 26
    if has_digit:
        pool_size += 10
    if has_symbol:
        pool_size += 32
    if has_space:
        pool_size += 1

    if pool_size == 0:
        pool_size = len(set(password))

    entropy = len(password) * math.log2(pool_size)
    return round(entropy, 2)

def evaluate_strength(password: str) -> dict:
    """Evaluate password strength based on entropy and character variety."""
    entropy = calculate_entropy(password)

    if entropy < 28:
        level = "Very Weak"
        score = 1
    elif entropy < 36:
        level = "Weak"
        score = 2
    elif entropy < 60:
        level = "Moderate"
        score = 3
    elif entropy < 85:
        level = "Strong"
        color = "lightgreen"
        score = 4
    else:
        level = "Very Strong"
        color = "green"
        score = 5

    return {
        "entropy": entropy,
        "level": level,
        "score": score
    }

def generate_password(
    length: int = 16,
    use_upper: bool = True,
    use_lower: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
    exclude_ambiguous: bool = False,
    custom_symbols: str = None
) -> str:
    """Generate a cryptographically secure random password."""
    char_pool = ""
    guaranteed = []

    upper_chars = string.ascii_uppercase
    lower_chars = string.ascii_lowercase
    digit_chars = string.digits
    symbol_chars = custom_symbols if custom_symbols is not None else "!@#$%^&*()_+-=[]{}|;:,.<>?"

    if exclude_ambiguous:
        upper_chars = "".join(c for c in upper_chars if c not in AMBIGUOUS_CHARS)
        lower_chars = "".join(c for c in lower_chars if c not in AMBIGUOUS_CHARS)
        digit_chars = "".join(c for c in digit_chars if c not in AMBIGUOUS_CHARS)
        symbol_chars = "".join(c for c in symbol_chars if c not in AMBIGUOUS_CHARS)

    if use_upper and upper_chars:
        char_pool += upper_chars
        guaranteed.append(secrets.choice(upper_chars))
    if use_lower and lower_chars:
        char_pool += lower_chars
        guaranteed.append(secrets.choice(lower_chars))
    if use_digits and digit_chars:
        char_pool += digit_chars
        guaranteed.append(secrets.choice(digit_chars))
    if use_symbols and symbol_chars:
        char_pool += symbol_chars
        guaranteed.append(secrets.choice(symbol_chars))

    if not char_pool:
        raise ValueError("At least one character set must be selected.")

    if length < len(guaranteed):
        length = len(guaranteed)

    remaining_length = length - len(guaranteed)
    password_chars = guaranteed + [secrets.choice(char_pool) for _ in range(remaining_length)]

    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)

def generate_passphrase(
    word_count: int = 4,
    separator: str = "-",
    capitalize: bool = True,
    include_number: bool = True
) -> str:
    """Generate a memorable Diceware-style passphrase."""
    chosen_words = [secrets.choice(MEMORABLE_WORDS) for _ in range(word_count)]
    if capitalize:
        chosen_words = [w.capitalize() for w in chosen_words]

    if include_number:
        insert_idx = secrets.randbelow(word_count)
        num_str = str(secrets.randbelow(90) + 10)
        chosen_words[insert_idx] = f"{chosen_words[insert_idx]}{num_str}"

    return separator.join(chosen_words)


class ModernPasswordGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Modern Password Generator")
        self.root.geometry("480x680")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        # Color Palette (Catppuccin Mocha)
        self.colors = {
            "bg": "#1e1e2e",
            "card": "#2a2b3d",
            "card_border": "#3b3d54",
            "text": "#cdd6f4",
            "subtext": "#a6adc8",
            "primary": "#89b4fa",
            "primary_hover": "#b4befe",
            "secondary": "#313244",
            "success": "#a6e3a1",
            "warning": "#fab387",
            "danger": "#f38ba8",
            "accent": "#cba6f7"
        }

        self.mode_var = tk.StringVar(value="password")  # "password" or "passphrase"
        self.length_var = tk.IntVar(value=16)
        self.words_var = tk.IntVar(value=4)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.no_ambig_var = tk.BooleanVar(value=False)
        self.add_number_var = tk.BooleanVar(value=True)
        self.history = []

        self._setup_ui()
        self.generate()

    def _setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors["bg"])
        header_frame.pack(fill="x", padx=24, pady=(20, 10))

        title_label = tk.Label(
            header_frame,
            text="\U0001F510 Password Generator",
            font=("Segoe UI", 18, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        )
        title_label.pack(anchor="w")

        subtitle_label = tk.Label(
            header_frame,
            text="Generate strong, cryptographically secure passwords & passphrases",
            font=("Segoe UI", 9),
            bg=self.colors["bg"],
            fg=self.colors["subtext"]
        )
        subtitle_label.pack(anchor="w", pady=(2, 0))

        # Result Card Frame
        result_card = tk.Frame(
            self.root,
            bg=self.colors["card"],
            highlightbackground=self.colors["card_border"],
            highlightthickness=1,
            bd=0
        )
        result_card.pack(fill="x", padx=24, pady=10)

        # Result display entry
        self.result_entry = tk.Entry(
            result_card,
            font=("Consolas", 14, "bold"),
            bg=self.colors["secondary"],
            fg=self.colors["primary"],
            bd=0,
            justify="center",
            insertbackground=self.colors["text"]
        )
        self.result_entry.pack(fill="x", padx=16, pady=(16, 10), ipady=8)

        # Strength Bar & Info
        strength_frame = tk.Frame(result_card, bg=self.colors["card"])
        strength_frame.pack(fill="x", padx=16, pady=(0, 10))

        self.strength_canvas = tk.Canvas(
            strength_frame,
            height=8,
            bg=self.colors["secondary"],
            highlightthickness=0,
            bd=0
        )
        self.strength_canvas.pack(fill="x", pady=(0, 6))

        info_row = tk.Frame(strength_frame, bg=self.colors["card"])
        info_row.pack(fill="x")

        self.strength_label = tk.Label(
            info_row,
            text="Strength: Strong",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors["card"],
            fg=self.colors["success"]
        )
        self.strength_label.pack(side="left")

        self.entropy_label = tk.Label(
            info_row,
            text="Entropy: 85 bits",
            font=("Segoe UI", 9),
            bg=self.colors["card"],
            fg=self.colors["subtext"]
        )
        self.entropy_label.pack(side="right")

        # Copy & Refresh Quick Action Buttons
        btn_row = tk.Frame(result_card, bg=self.colors["card"])
        btn_row.pack(fill="x", padx=16, pady=(0, 14))

        self.copy_btn = tk.Button(
            btn_row,
            text="\U0001F4CB Copy to Clipboard",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors["primary"],
            fg="#11111b",
            activebackground=self.colors["primary_hover"],
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.copy_to_clipboard
        )
        self.copy_btn.pack(side="left", expand=True, fill="x", padx=(0, 6), ipady=6)

        regen_btn = tk.Button(
            btn_row,
            text="\U0001F504 Regenerate",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors["secondary"],
            fg=self.colors["text"],
            activebackground=self.colors["card_border"],
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.generate
        )
        regen_btn.pack(side="right", expand=True, fill="x", padx=(6, 0), ipady=6)

        # Mode Selection Tabs (Password vs Passphrase)
        mode_frame = tk.Frame(self.root, bg=self.colors["bg"])
        mode_frame.pack(fill="x", padx=24, pady=(6, 8))

        self.btn_pwd_mode = tk.Button(
            mode_frame,
            text="Standard Password",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda: self.set_mode("password")
        )
        self.btn_pwd_mode.pack(side="left", expand=True, fill="x", padx=(0, 4), ipady=5)

        self.btn_phrase_mode = tk.Button(
            mode_frame,
            text="Memorable Passphrase",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda: self.set_mode("passphrase")
        )
        self.btn_phrase_mode.pack(side="right", expand=True, fill="x", padx=(4, 0), ipady=5)

        # Settings Card
        self.settings_card = tk.Frame(
            self.root,
            bg=self.colors["card"],
            highlightbackground=self.colors["card_border"],
            highlightthickness=1,
            bd=0
        )
        self.settings_card.pack(fill="both", expand=True, padx=24, pady=(4, 16))

        self.build_settings_widgets()
        self.update_mode_buttons()

    def set_mode(self, mode):
        self.mode_var.set(mode)
        self.update_mode_buttons()
        self.build_settings_widgets()
        self.generate()

    def update_mode_buttons(self):
        is_pwd = self.mode_var.get() == "password"
        self.btn_pwd_mode.configure(
            bg=self.colors["primary"] if is_pwd else self.colors["secondary"],
            fg="#11111b" if is_pwd else self.colors["text"]
        )
        self.btn_phrase_mode.configure(
            bg=self.colors["primary"] if not is_pwd else self.colors["secondary"],
            fg="#11111b" if not is_pwd else self.colors["text"]
        )

    def build_settings_widgets(self):
        for widget in self.settings_card.winfo_children():
            widget.destroy()

        if self.mode_var.get() == "password":
            # Slider row
            slider_header = tk.Frame(self.settings_card, bg=self.colors["card"])
            slider_header.pack(fill="x", padx=16, pady=(12, 4))

            tk.Label(
                slider_header,
                text="Password Length",
                font=("Segoe UI", 10, "bold"),
                bg=self.colors["card"],
                fg=self.colors["text"]
            ).pack(side="left")

            self.len_display = tk.Label(
                slider_header,
                text=str(self.length_var.get()),
                font=("Segoe UI", 10, "bold"),
                bg=self.colors["secondary"],
                fg=self.colors["primary"],
                padx=8,
                pady=1
            )
            self.len_display.pack(side="right")

            slider = ttk.Scale(
                self.settings_card,
                from_=6,
                to=48,
                variable=self.length_var,
                orient="horizontal",
                command=self.on_length_change
            )
            slider.pack(fill="x", padx=16, pady=(0, 12))

            # Options Checkboxes
            options = [
                ("Include Uppercase (A-Z)", self.upper_var),
                ("Include Lowercase (a-z)", self.lower_var),
                ("Include Numbers (0-9)", self.digits_var),
                ("Include Symbols (!@#$...)", self.symbols_var),
                ("Exclude Ambiguous (1, l, I, 0, O)", self.no_ambig_var)
            ]

            for text, var in options:
                cb = tk.Checkbutton(
                    self.settings_card,
                    text=text,
                    variable=var,
                    font=("Segoe UI", 10),
                    bg=self.colors["card"],
                    fg=self.colors["text"],
                    selectcolor=self.colors["secondary"],
                    activebackground=self.colors["card"],
                    activeforeground=self.colors["text"],
                    bd=0,
                    command=self.generate
                )
                cb.pack(anchor="w", padx=16, pady=3)

        else:
            # Passphrase Options
            words_header = tk.Frame(self.settings_card, bg=self.colors["card"])
            words_header.pack(fill="x", padx=16, pady=(12, 4))

            tk.Label(
                words_header,
                text="Number of Words",
                font=("Segoe UI", 10, "bold"),
                bg=self.colors["card"],
                fg=self.colors["text"]
            ).pack(side="left")

            self.words_display = tk.Label(
                words_header,
                text=str(self.words_var.get()),
                font=("Segoe UI", 10, "bold"),
                bg=self.colors["secondary"],
                fg=self.colors["primary"],
                padx=8,
                pady=1
            )
            self.words_display.pack(side="right")

            slider = ttk.Scale(
                self.settings_card,
                from_=3,
                to=8,
                variable=self.words_var,
                orient="horizontal",
                command=self.on_words_change
            )
            slider.pack(fill="x", padx=16, pady=(0, 16))

            cb_num = tk.Checkbutton(
                self.settings_card,
                text="Append Random 2-digit Number",
                variable=self.add_number_var,
                font=("Segoe UI", 10),
                bg=self.colors["card"],
                fg=self.colors["text"],
                selectcolor=self.colors["secondary"],
                activebackground=self.colors["card"],
                activeforeground=self.colors["text"],
                bd=0,
                command=self.generate
            )
            cb_num.pack(anchor="w", padx=16, pady=4)

        # Bulk Generation Link
        bulk_btn = tk.Button(
            self.settings_card,
            text="\U0001F4D1 Generate Multiple / View History",
            font=("Segoe UI", 9),
            bg=self.colors["card"],
            fg=self.colors["accent"],
            activebackground=self.colors["card"],
            activeforeground=self.colors["primary"],
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.show_bulk_dialog
        )
        bulk_btn.pack(side="bottom", pady=12)

    def on_length_change(self, val):
        length = int(float(val))
        self.length_var.set(length)
        if hasattr(self, 'len_display'):
            self.len_display.config(text=str(length))
        self.generate()

    def on_words_change(self, val):
        words = int(float(val))
        self.words_var.set(words)
        if hasattr(self, 'words_display'):
            self.words_display.config(text=str(words))
        self.generate()

    def generate(self):
        try:
            if self.mode_var.get() == "password":
                if not (self.upper_var.get() or self.lower_var.get() or self.digits_var.get() or self.symbols_var.get()):
                    self.lower_var.set(True)  # default back to lowercase if all deselected

                pwd = generate_password(
                    length=self.length_var.get(),
                    use_upper=self.upper_var.get(),
                    use_lower=self.lower_var.get(),
                    use_digits=self.digits_var.get(),
                    use_symbols=self.symbols_var.get(),
                    exclude_ambiguous=self.no_ambig_var.get()
                )
            else:
                pwd = generate_passphrase(
                    word_count=self.words_var.get(),
                    separator="-",
                    capitalize=True,
                    include_number=self.add_number_var.get()
                )

            self.result_entry.delete(0, tk.END)
            self.result_entry.insert(0, pwd)
            self.copy_btn.config(text="\U0001F4CB Copy to Clipboard", bg=self.colors["primary"])

            if pwd not in self.history:
                self.history.insert(0, pwd)
                if len(self.history) > 20:
                    self.history.pop()

            self.update_strength(pwd)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_strength(self, pwd):
        metrics = evaluate_strength(pwd)
        score = metrics["score"]
        entropy = metrics["entropy"]
        level = metrics["level"]

        bar_colors = {
            1: self.colors["danger"],
            2: self.colors["warning"],
            3: "#f9e2af",  # Yellow
            4: self.colors["success"],
            5: "#94e2d5"   # Teal / Strongest
        }

        active_color = bar_colors.get(score, self.colors["primary"])
        self.strength_label.config(text=f"Strength: {level}", fg=active_color)
        self.entropy_label.config(text=f"Entropy: {entropy} bits")

        self.strength_canvas.delete("all")
        width = self.strength_canvas.winfo_width()
        if width <= 1:
            width = 430
        fill_width = int(width * (score / 5.0))
        self.strength_canvas.create_rectangle(0, 0, fill_width, 8, fill=active_color, width=0)

    def copy_to_clipboard(self):
        text = self.result_entry.get()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.root.update()
            self.copy_btn.config(text="\U00002705 Copied!", bg=self.colors["success"])

    def show_bulk_dialog(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("Generate Multiple Passwords")
        dlg.geometry("420x450")
        dlg.configure(bg=self.colors["bg"])
        dlg.transient(self.root)

        tk.Label(
            dlg,
            text="Generate Multiple Passwords",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        ).pack(anchor="w", padx=16, pady=(16, 8))

        top_bar = tk.Frame(dlg, bg=self.colors["bg"])
        top_bar.pack(fill="x", padx=16, pady=4)

        tk.Label(top_bar, text="Count:", font=("Segoe UI", 10), bg=self.colors["bg"], fg=self.colors["text"]).pack(side="left")
        count_var = tk.IntVar(value=5)
        count_spin = tk.Spinbox(top_bar, from_=1, to=50, width=5, textvariable=count_var, font=("Segoe UI", 10))
        count_spin.pack(side="left", padx=8)

        text_box = tk.Text(
            dlg,
            font=("Consolas", 10),
            bg=self.colors["card"],
            fg=self.colors["text"],
            bd=0,
            padx=10,
            pady=10
        )
        text_box.pack(fill="both", expand=True, padx=16, pady=10)

        def generate_bulk():
            text_box.delete("1.0", tk.END)
            count = count_var.get()
            passwords = []
            for _ in range(count):
                if self.mode_var.get() == "password":
                    p = generate_password(
                        length=self.length_var.get(),
                        use_upper=self.upper_var.get(),
                        use_lower=self.lower_var.get(),
                        use_digits=self.digits_var.get(),
                        use_symbols=self.symbols_var.get(),
                        exclude_ambiguous=self.no_ambig_var.get()
                    )
                else:
                    p = generate_passphrase(
                        word_count=self.words_var.get(),
                        separator="-",
                        capitalize=True,
                        include_number=self.add_number_var.get()
                    )
                passwords.append(p)
            text_box.insert(tk.END, "\n".join(passwords))

        gen_btn = tk.Button(
            top_bar,
            text="Generate",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors["primary"],
            fg="#11111b",
            relief="flat",
            bd=0,
            command=generate_bulk
        )
        gen_btn.pack(side="left", padx=8)

        def copy_all():
            content = text_box.get("1.0", tk.END).strip()
            if content:
                self.root.clipboard_clear()
                self.root.clipboard_append(content)
                self.root.update()
                copy_all_btn.config(text="\U00002705 Copied All!", bg=self.colors["success"])

        copy_all_btn = tk.Button(
            dlg,
            text="\U0001F4CB Copy All",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors["secondary"],
            fg=self.colors["text"],
            relief="flat",
            bd=0,
            command=copy_all
        )
        copy_all_btn.pack(fill="x", padx=16, pady=(0, 16), ipady=6)

        generate_bulk()

def launch_gui():
    root = tk.Tk()
    app = ModernPasswordGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    launch_gui()
