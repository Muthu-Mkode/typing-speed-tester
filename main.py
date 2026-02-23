"""Typing Speed Tester Application.

A GUI-based application to measure a user's typing speed (Words Per Minute)
and accuracy against a set of predefined sample texts using the Tkinter library.
"""

import tkinter as tk
import time
import random

APP_TITLE = "Typing Speed Tester"
WINDOW_SIZE = "900x600"
COLOR_BG = "#2C3E50"
COLOR_CARD = "#34495E"
COLOR_TEXT_PRIMARY = "#ECF0F1"
COLOR_TEXT_SECONDARY = "#BDC3C7"
COLOR_ACCENT = "#27AE60"
COLOR_ERROR = "#E74C3C"

FONT_HEADING = ("Helvetica", 28, "bold")
FONT_SUBHEADING = ("Helvetica", 16)
FONT_TEXT = ("Consolas", 18)
FONT_BUTTON = ("Helvetica", 14, "bold")

SAMPLE_TEXTS = [
    "The quick brown fox jumps over the lazy dog.",
    "Pack my box with five dozen liquor jugs.",
    "Jackdaws love my big sphinx of quartz.",
    "The five boxing wizards jump quickly.",
    "How vexingly quick daft zebras jump.",
    "Bright vixens jump; dozy fowl quack.",
    "Sphinx of black quartz, judge my vow.",
    "Two driven jocks help fax my big quiz.",
    "A wizard's job is to vex chumps quickly in fog.",
    "Watch Jeopardy!, Alex Trebek's fun TV quiz game."
]


class TypingSpeedApp:
    """A GUI application for testing typing speed and accuracy.

    This class handles the creation of the user interface, tracking the user's
    input speed, calculating Words Per Minute (WPM) and accuracy, and managing
    the overall state of the typing test.

    Attributes:
        root (tk.Tk): The root window of the Tkinter application.
        is_running (bool): Tracks whether a typing test is currently active.
        start_time (float): The timestamp when the user started typing.
        target_text (str): The current sample text the user needs to type.
    """

    def __init__(self, root):
        """Initializes the TypingSpeedApp with the main window and state variables.

        Args:
            root (tk.Tk): The root window of the Tkinter application.
        """
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.resizable(False, False)
        self.root.configure(bg=COLOR_BG)

        self.is_running = False
        self.start_time = 0.0
        self.target_text = ""

        self._setup_ui()
        self.reset_game()

    def _setup_ui(self):
        """Sets up the graphical user interface elements.

        Creates and arranges the main frame, labels, score displays,
        input entry field, and the reset button within the root window.
        """
        self.main_frame = tk.Frame(self.root, bg=COLOR_BG)
        self.main_frame.pack(expand=True, fill="both", padx=40, pady=40)

        self.title_label = tk.Label(
            self.main_frame,
            text="TYPING SPEED TEST",
            font=FONT_HEADING,
            bg=COLOR_BG,
            fg=COLOR_TEXT_PRIMARY
        )
        self.title_label.pack(pady=(0, 10))

        self.score_frame = tk.Frame(self.main_frame, bg=COLOR_CARD, padx=20, pady=10)
        self.score_frame.pack(pady=20, fill="x")

        self.wpm_label = tk.Label(
            self.score_frame,
            text="WPM: 0",
            font=FONT_SUBHEADING,
            bg=COLOR_CARD,
            fg=COLOR_ACCENT
        )
        self.wpm_label.pack(side="left", padx=20)

        self.accuracy_label = tk.Label(
            self.score_frame,
            text="Accuracy: 100%",
            font=FONT_SUBHEADING,
            bg=COLOR_CARD,
            fg=COLOR_ACCENT
        )
        self.accuracy_label.pack(side="right", padx=20)

        self.target_label = tk.Label(
            self.main_frame,
            text="",
            font=FONT_TEXT,
            bg=COLOR_BG,
            fg=COLOR_TEXT_SECONDARY,
            wraplength=800,
            justify="center"
        )
        self.target_label.pack(pady=30)

        self.input_entry = tk.Entry(
            self.main_frame,
            font=FONT_TEXT,
            bg=COLOR_TEXT_PRIMARY,
            fg="#2C3E50",
            relief="flat",
            justify="center"
        )
        self.input_entry.pack(pady=10, ipady=10, fill="x")

        self.input_entry.bind("<KeyPress>", self.start_timer)
        self.input_entry.bind("<KeyRelease>", self.update_stats)

        self.reset_button = tk.Button(
            self.main_frame,
            text="RESTART TEST",
            font=FONT_BUTTON,
            bg=COLOR_ACCENT,
            fg="white",
            activebackground="#2ECC71",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.reset_game
        )
        self.reset_button.pack(pady=30, ipadx=20, ipady=5)

    def start_timer(self, event):
        """Starts the tracking timer on the user's first key press.

        Args:
            event (tk.Event): The KeyPress event triggered by the user typing
                in the input field.
        """
        if not self.is_running and not self.input_entry.get():
            self.is_running = True
            self.start_time = time.time()

    def update_stats(self, event):
        """Calculates and updates the WPM and accuracy statistics based on input.

        Args:
            event (tk.Event): The KeyRelease event triggered by the user typing
                in the input field.
        """
        if not self.is_running:
            return

        typed_text = self.input_entry.get()

        elapsed_time = time.time() - self.start_time
        if elapsed_time == 0:
            elapsed_time = 0.01

        minutes = elapsed_time / 60
        wpm = (len(typed_text) / 5) / minutes

        correct_chars = 0
        for i, char in enumerate(typed_text):
            if i < len(self.target_text) and char == self.target_text[i]:
                correct_chars += 1

        accuracy = (correct_chars / len(typed_text)) * 100 if typed_text else 100

        self.wpm_label.config(text=f"WPM: {wpm:.0f}")
        self.accuracy_label.config(text=f"Accuracy: {accuracy:.0f}%")

        if typed_text != self.target_text[:len(typed_text)]:
            self.input_entry.config(fg=COLOR_ERROR)
        else:
            self.input_entry.config(fg="#2C3E50")

        if typed_text == self.target_text:
            self.is_running = False
            self.input_entry.config(state='disabled', fg=COLOR_ACCENT)

    def reset_game(self):
        """Resets the application state and UI to start a new typing test.

        This method selects a new random target text, resets the timer status,
        clears the input field, and restores the default WPM and accuracy labels.
        """
        self.is_running = False
        self.target_text = random.choice(SAMPLE_TEXTS)

        self.target_label.config(text=self.target_text)
        self.wpm_label.config(text="WPM: 0")
        self.accuracy_label.config(text="Accuracy: 100%")

        self.input_entry.config(state="normal", fg="#2C3E50")
        self.input_entry.delete(0, tk.END)
        self.input_entry.focus()


if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedApp(root)
    root.mainloop()
