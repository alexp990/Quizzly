import tkinter as tk
import pandas as pd


def get_flashcards(csv_file: str):
    """Load flashcards from a CSV file."""
    try:
        flashcards = pd.read_csv(csv_file)
        terms = flashcards.iloc[:, 0].tolist()
        definitions = flashcards.iloc[:, 1].tolist()
        if not terms or not definitions:
            raise ValueError(
                "Flashcards file is empty or improperly formatted.")
        return terms, definitions
    except Exception as e:
        print(f"Error loading flashcards: {e}")
        return [], []


def show_flashcard():
    """Display the current flashcard term."""
    global answer_shown
    answer_shown = False  # Reset answer visibility
    if terms:
        term = terms[curr_flashcard_idx]
        question_label.config(text=term, font=("Arial", 16))
        answer_label.config(text="")
    else:
        question_label.config(
            text="No flashcards available.", font=("Arial", 16))
        answer_label.config(text="")


def show_or_hide_answer():
    """Reveal or hide the answer to the current flashcard."""
    global answer_shown
    if terms:
        answer_shown = not answer_shown
        if answer_shown:
            definition = definitions[curr_flashcard_idx]
            answer_label.config(text=definition, font=("Arial", 14))
        else:
            answer_label.config(text="")
    else:
        answer_label.config(text="No flashcards available to reveal.")


def change_flashcard(action: str):
    """Move to the next or previous flashcard."""
    global curr_flashcard_idx
    if terms:
        if action == "fwd":
            curr_flashcard_idx = (curr_flashcard_idx + 1) % len(terms)
        elif action == "bwd":
            curr_flashcard_idx = (curr_flashcard_idx - 1) % len(terms)
        show_flashcard()
    else:
        question_label.config(text="No flashcards to navigate.")


# Load flashcards from file
flashcards_path = "test_flashcards.csv"
terms, definitions = get_flashcards(flashcards_path)
curr_flashcard_idx = 0
answer_shown = False

# Create GUI
root = tk.Tk()
root.title("Flashcards App")

question_label = tk.Label(root, text="", wraplength=400, justify="center")
question_label.pack(pady=20)

answer_label = tk.Label(root, text="", wraplength=400,
                        justify="center", fg="blue")
answer_label.pack(pady=10)

reveal_button = tk.Button(root, text="Show/Hide Answer",
                          font=("Arial", 14), command=show_or_hide_answer)
reveal_button.pack(pady=5)

next_button = tk.Button(root, text="Next Flashcard",
                        font=("Arial", 14), command=lambda: change_flashcard("fwd"))
next_button.pack(pady=5)

prev_button = tk.Button(root, text="Previous Flashcard",
                        font=("Arial", 14), command=lambda: change_flashcard("bwd"))
prev_button.pack(pady=5)

# Start with the first flashcard
show_flashcard()

root.mainloop()
