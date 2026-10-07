"""
Typing Speed Test
-----------------
A simple desktop app built with tkinter that measures
typing speed (WPM) and accuracy.

Run:  python typing_speed_test.py
"""

import random
import time
import tkinter as tk

SENTENCES = [
    "The quick brown fox jumps over the lazy dog near the river bank.",
    "Practice makes perfect, so keep typing every day to improve your speed.",
    "Python is a powerful language that is easy to read and fun to learn.",
    "A journey of a thousand miles begins with a single step forward.",
    "Good programmers write code that humans can understand and maintain.",
    "Consistency is more important than speed when you are learning to type.",
    "Every expert was once a beginner who refused to give up on learning.",
]

TIME_LIMIT = 60  # seconds


class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("700x450")
        self.root.resizable(False, False)

        self.target = ""
        self.start_time = None
        self.running = False
        self.finished = False

        self.build_ui()
        self.reset()

    # ---------- UI ----------
    def build_ui(self):
        tk.Label(
            self.root, text="Typing Speed Test", font=("Arial", 22, "bold")
        ).pack(pady=(15, 5))

        tk.Label(
            self.root,
            text="Start typing the text below. The timer begins with your first key.",
            font=("Arial", 10),
            fg="gray",
        ).pack()

        # Text to type (read-only, colored as you type)
        self.text_box = tk.Text(
            self.root,
            height=4,
            width=60,
            font=("Courier", 15),
            wrap="word",
            padx=10,
            pady=10,
            relief="solid",
            borderwidth=1,
        )
        self.text_box.pack(pady=15)
        self.text_box.tag_config("correct", foreground="green")
        self.text_box.tag_config("wrong", foreground="white", background="red")

        # Typing area
        self.entry = tk.Entry(self.root, width=55, font=("Courier", 15))
        self.entry.pack(pady=5)
        self.entry.bind("<KeyRelease>", self.on_key)

        # Live stats
        self.timer_label = tk.Label(
            self.root, text=f"Time left: {TIME_LIMIT}s", font=("Arial", 13)
        )
        self.timer_label.pack(pady=(15, 5))

        self.result_label = tk.Label(
            self.root, text="", font=("Arial", 15, "bold"), fg="#1a5fb4"
        )
        self.result_label.pack(pady=5)

        tk.Button(
            self.root,
            text="Restart",
            font=("Arial", 12),
            width=12,
            command=self.reset,
        ).pack(pady=10)

    # ---------- Game logic ----------
    def reset(self):
        """Pick a new sentence and clear everything."""
        self.target = random.choice(SENTENCES)
        self.start_time = None
        self.running = False
        self.finished = False

        self.text_box.config(state="normal")
        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", self.target)
        self.text_box.config(state="disabled")

        self.entry.config(state="normal")
        self.entry.delete(0, "end")
        self.entry.focus()

        self.timer_label.config(text=f"Time left: {TIME_LIMIT}s")
        self.result_label.config(text="")

    def on_key(self, event):
        if self.finished:
            return

        typed = self.entry.get()
        if not typed:
            return

        # Start the timer on the first keystroke
        if not self.running:
            self.running = True
            self.start_time = time.time()
            self.update_timer()

        self.highlight(typed)

        # Finished if the whole sentence has been typed
        if len(typed) >= len(self.target):
            self.finish()

    def highlight(self, typed):
        """Color each typed character green (correct) or red (wrong)."""
        self.text_box.config(state="normal")
        self.text_box.tag_remove("correct", "1.0", "end")
        self.text_box.tag_remove("wrong", "1.0", "end")

        for i, ch in enumerate(typed[: len(self.target)]):
            tag = "correct" if ch == self.target[i] else "wrong"
            self.text_box.tag_add(tag, f"1.{i}", f"1.{i + 1}")

        self.text_box.config(state="disabled")

    def update_timer(self):
        if not self.running or self.finished:
            return

        remaining = TIME_LIMIT - int(time.time() - self.start_time)
        if remaining <= 0:
            self.timer_label.config(text="Time left: 0s")
            self.finish()
            return

        self.timer_label.config(text=f"Time left: {remaining}s")
        self.root.after(200, self.update_timer)

    def finish(self):
        self.finished = True
        self.running = False
        self.entry.config(state="disabled")

        typed = self.entry.get()
        elapsed = min(time.time() - self.start_time, TIME_LIMIT)
        minutes = max(elapsed / 60, 1 / 60)  # avoid dividing by zero

        correct = sum(
            1 for i, ch in enumerate(typed[: len(self.target)]) if ch == self.target[i]
        )

        # Standard formula: 1 "word" = 5 characters
        wpm = (correct / 5) / minutes
        accuracy = (correct / len(typed) * 100) if typed else 0

        self.result_label.config(
            text=f"Speed: {wpm:.1f} WPM   |   Accuracy: {accuracy:.1f}%"
        )


if __name__ == "__main__":
    root = tk.Tk()
    TypingSpeedTest(root)
    root.mainloop()