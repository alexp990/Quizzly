from customtkinter import *
import pandas as pd
import time

# //Review mode/normal mode deletion of items index out of range


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
        question_label.configure(text=term, font=("Arial", 16))
        answer_label.configure(text="")
    else:
        question_label.configure(
            text="No flashcards available.", font=("Arial", 16))
        answer_label.configure(text="")


def show_or_hide_answer():
    """Reveal or hide the answer to the current flashcard."""
    global answer_shown
    if terms:
        answer_shown = not answer_shown
        if answer_shown:
            definition = definitions[curr_flashcard_idx]
            answer_label.configure(text=definition, font=("Arial", 14))
            if write_mode:
                user_entry = str(answer_entry.get()).strip().lower()
                if user_entry == definition.strip().lower():
                    print("Correct!")
                    answer_entry.configure(text_color="#4ceb34")
                else:
                    print("Wrong!")
                    answer_entry.configure(text_color="red")
                    add_flashcard_to_incorrect_list(curr_flashcard_idx)
        else:
            answer_label.configure(text="")
    else:
        answer_label.configure(text="No flashcards available to reveal.")


def switch_to_review_mode():
    global terms, definitions, curr_flashcard_idx, review_mode
    """Allows user to review the cards they got wrong"""
    terms = incorrect_terms
    definitions = incorrect_definitions
    curr_flashcard_idx = 0
    show_flashcard()
    if write_mode:
        answer_entry.configure(text_color="yellow")
    review_mode = True
    print("review mode")


def switch_to_normal_mode():
    global terms, definitions, curr_flashcard_idx
    """Switches back to normal mode with all loaded flashcards"""
    terms, definitions = get_flashcards(flashcards_path)
    curr_flashcard_idx = 0
    if write_mode:
        answer_entry.configure(text_color="yellow")
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
        answer_entry.delete(0, "end")
        answer_entry.configure(text_color="yellow")
        show_flashcard()
    else:
        question_label.configure(text="No flashcards to navigate.")


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
    if not write_mode:
        global curr_flashcard_idx, incorrect_terms, incorrect_definitions
        if review_mode and curr_flashcard_idx < len(terms):
            term_to_remove = terms[curr_flashcard_idx]
            definition_to_remove = definitions[curr_flashcard_idx]

            if term_to_remove in incorrect_terms:
                incorrect_terms.remove(term_to_remove)
            if definition_to_remove in incorrect_definitions:
                incorrect_definitions.remove(definition_to_remove)

            # Check if review list is empty
            if not incorrect_terms:
                switch_to_normal_mode()
                return

        # Navigate to the next flashcard
        change_flashcard("fwd")


def switch_modes():
    global normal_mode, write_mode
    normal_mode = not normal_mode
    write_mode = not write_mode
    if normal_mode:
        switch_modes_button.configure(text="Switch to Write Mode")
    else:
        switch_modes_button.configure(text="Switch to Normal Mode")


# Load flashcards from file
flashcards_path = "C:/Users/Alex/Documents/GitHub/Quizzly/test_flashcards.csv"
terms, definitions = get_flashcards(flashcards_path)
curr_flashcard_idx = 0
answer_shown = False
normal_mode = True
write_mode = False

# Create GUI
root = CTk()
root.title("Flashcard App")
root.geometry("600x400")

# Flashcard Frame
flashcard_frame = CTkFrame(root)
flashcard_frame.pack(pady=20, padx=20, fill="x")

# Question Label Frame
question_frame = CTkFrame(
    flashcard_frame, fg_color="#4c75b0", corner_radius=10)
question_frame.pack(pady=3, padx=10, fill="x")
question_label = CTkLabel(question_frame, text="",
                          wraplength=500, font=("Arial", 16), anchor="center")
question_label.pack(pady=3, padx=10)

# Answer Label Frame
answer_frame = CTkFrame(flashcard_frame, fg_color="#4c75b0",
                        corner_radius=10)
answer_frame.pack(pady=3, padx=10, fill="x")
answer_label = CTkLabel(answer_frame, text="", wraplength=500, font=(
    "Arial", 16, "italic"), text_color="blue", anchor="center")
answer_label.pack(pady=3, padx=10)

# Answer Text Entry
answer_entry = CTkEntry(root, fg_color="#4c75b0",
                        corner_radius=10, text_color="yellow")
answer_entry.pack(pady=2, padx=30, fill="x")

# Switch to write mode
switch_modes_button = CTkButton(
    root, text="Switch to write mode", font=("Arial", 14), command=switch_modes)
switch_modes_button.pack(pady=20, padx=10)

# Navigation Buttons Frame
nav_frame = CTkFrame(root)
nav_frame.pack(pady=(10, 0))

prev_button = CTkButton(nav_frame, text="Previous", font=(
    "Arial", 14), command=lambda: change_flashcard("bwd"))
prev_button.grid(row=0, column=0, padx=10, pady=3)

next_button = CTkButton(nav_frame, text="Next", font=(
    "Arial", 14), command=lambda: change_flashcard("fwd"))
next_button.grid(row=0, column=1, padx=10, pady=3)

# Reveal Answer Button
reveal_button = CTkButton(root, text="Show/Hide Answer",
                          font=("Arial", 14), command=show_or_hide_answer)
reveal_button.pack(pady=20)

# Mode Buttons Frame
mode_frame = CTkFrame(root)
mode_frame.pack(pady=(10, 20))

review_mode_button = CTkButton(mode_frame, text="Review Mode", font=(
    "Arial", 12), command=switch_to_review_mode)
review_mode_button.grid(row=0, column=0, padx=10, pady=3)

normal_mode_button = CTkButton(mode_frame, text="Normal Mode", font=(
    "Arial", 12), command=switch_to_normal_mode)
normal_mode_button.grid(row=0, column=1, padx=10, pady=3)


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
