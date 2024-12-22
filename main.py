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


def switch_to_review_mode():
    global terms, definitions, curr_flashcard_idx, review_mode
    """Allows user to review the cards they got wrong"""
    terms = incorrect_terms
    definitions = incorrect_definitions
    curr_flashcard_idx = 0
    show_flashcard()
    review_mode = True
    print("review mode")


def switch_to_normal_mode():
    global terms, definitions, curr_flashcard_idx
    """Switches back to normal mode with all loaded flashcards"""
    terms, definitions = get_flashcards(flashcards_path)
    curr_flashcard_idx = 0
    show_flashcard()
    print("normal mode")


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


def add_flashcard_to_incorrect_list(flashcard_idx: int):
    """Adds flashcard to list of incorrect flashcards"""
    global incorrect_terms
    global incorrect_definitions
    if terms[flashcard_idx] not in incorrect_terms:
        incorrect_terms.append(terms[flashcard_idx])

    if definitions[flashcard_idx] not in incorrect_definitions:
        incorrect_definitions.append(definitions[flashcard_idx])
    print(incorrect_terms, incorrect_definitions)


def mark_correct_and_continue():
    """Remove the current flashcard from the incorrect list and navigate."""
    if review_mode:
        global curr_flashcard_idx, incorrect_terms, incorrect_definitions
        incorrect_terms.remove(terms[curr_flashcard_idx])
        incorrect_definitions.remove(definitions[curr_flashcard_idx])

        # If the incorrect list is empty, switch back to normal mode
        if not incorrect_terms:
            switch_to_normal_mode()
            curr_flashcard_idx = 0
            show_flashcard()
    if terms[curr_flashcard_idx] not in incorrect_terms or review_mode:
        change_flashcard("fwd")


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

review_mode_button = tk.Button(root, text="Review mode",
                               font=("Arial", 10), command=switch_to_review_mode)
review_mode_button.pack(pady=5)

normal_mode_button = tk.Button(root, text="Normal Mode",
                               font=("Arial", 10), command=switch_to_normal_mode)
normal_mode_button.pack(pady=5)

# Keybinds for checking
root.bind("1", lambda event: add_flashcard_to_incorrect_list(
    curr_flashcard_idx))  # *1: incorrect
root.bind("2", lambda event: mark_correct_and_continue())  # *2: incorrect

# Start with the first flashcard
show_flashcard()
incorrect_terms = []
incorrect_definitions = []
review_mode = False

root.mainloop()
