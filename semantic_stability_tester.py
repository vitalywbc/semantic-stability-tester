"""
Semantic Stability Tester

This project checks whether repeated answers for each question are stable.
"""

import tkinter


def read_answers_from_file(file_name):
    """Read answers from a text file and group them by question ID."""

    answers_by_question = {}

    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line == "":
                continue

            parts = line.split(",", 1)

            if len(parts) != 2:
                print("Skipping line because it is not in question_id,answer format:", line)
                continue

            question_id = parts[0].strip()
            answer = parts[1].strip()

            if question_id not in answers_by_question:
                answers_by_question[question_id] = []

            answers_by_question[question_id].append(answer)

    return answers_by_question


def count_answers(answers):
    """Count how many times each answer appears."""

    answer_counts = {}

    for answer in answers:
        if answer not in answer_counts:
            answer_counts[answer] = 0

        answer_counts[answer] = answer_counts[answer] + 1

    return answer_counts


def find_most_common_answer_count(answer_counts):
    """Find the biggest answer count."""

    most_common_count = 0

    for answer in answer_counts:
        count = answer_counts[answer]

        if count > most_common_count:
            most_common_count = count

    return most_common_count


def calculate_question_sci_scores(answers_by_question):
    """Calculate an SCI score for every question group."""

    sci_by_question = {}

    for question_id in answers_by_question:
        answers = answers_by_question[question_id]
        answer_counts = count_answers(answers)
        most_common_count = find_most_common_answer_count(answer_counts)
        total_answers = len(answers)

        question_sci = (most_common_count / total_answers) * 100
        sci_by_question[question_id] = question_sci

    return sci_by_question


def calculate_overall_sci(sci_by_question):
    """Calculate the overall SCI score."""

    total_groups = len(sci_by_question)

    if total_groups == 0:
        return 0

    total_sci = 0

    for question_id in sci_by_question:
        total_sci = total_sci + sci_by_question[question_id]

    overall_sci = total_sci / total_groups
    return overall_sci


def print_most_unstable_groups(answers_by_question, sci_by_question):
    """Print the three lowest SCI question groups."""

    remaining_scores = {}

    for question_id in sci_by_question:
        remaining_scores[question_id] = sci_by_question[question_id]

    print("Most unstable question groups:")

    groups_printed = 0

    while groups_printed < 3 and len(remaining_scores) > 0:
        lowest_question_id = ""
        lowest_score = 101

        for question_id in remaining_scores:
            score = remaining_scores[question_id]

            if score < lowest_score:
                lowest_score = score
                lowest_question_id = question_id

        print(
            "-",
            lowest_question_id,
            "SCI:",
            round(lowest_score, 2),
            "%",
            "answers:",
            answers_by_question[lowest_question_id],
        )

        del remaining_scores[lowest_question_id]
        groups_printed = groups_printed + 1


def draw_heatmap(sci_by_question):
    """Draw a simple heatmap using tkinter canvas."""

    square_size = 40
    gap = 8
    squares_per_row = 5

    total_groups = len(sci_by_question)

    canvas_width = squares_per_row * (square_size + gap) + gap
    number_of_rows = (total_groups + squares_per_row - 1) // squares_per_row
    canvas_height = number_of_rows * (square_size + gap) + 140

    window = tkinter.Tk()
    window.title("Semantic Stability Tester Heatmap")

    canvas = tkinter.Canvas(window, width=canvas_width, height=canvas_height, bg="white")
    canvas.pack()

    canvas.create_text(
        canvas_width / 2,
        20,
        text="Semantic Stability Heatmap",
        font=("Arial", 16, "bold"),
    )

    canvas.create_rectangle(12, 42, 32, 62, fill="green", outline="")
    canvas.create_text(102, 52, text="SCI 80 or above", font=("Arial", 11))

    canvas.create_rectangle(12, 68, 32, 88, fill="orange", outline="")
    canvas.create_text(112, 78, text="SCI 50 to 79", font=("Arial", 11))

    canvas.create_rectangle(12, 94, 32, 114, fill="red", outline="")
    canvas.create_text(98, 104, text="SCI below 50", font=("Arial", 11))

    index = 0

    for question_id in sci_by_question:
        row = index // squares_per_row
        column = index % squares_per_row

        x1 = gap + column * (square_size + gap)
        y1 = 135 + row * (square_size + gap)
        x2 = x1 + square_size
        y2 = y1 + square_size

        question_sci = sci_by_question[question_id]

        if question_sci >= 80:
            color = "green"
        elif question_sci >= 50:
            color = "orange"
        else:
            color = "red"

        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
        canvas.create_text(
            x1 + square_size / 2,
            y1 + square_size / 2,
            text=question_id,
            fill="white",
            font=("Arial", 10, "bold"),
        )

        index = index + 1

    window.mainloop()


def main():
    """Run the program."""

    print("Semantic Stability Tester")
    print("-------------------------")
    print("This program checks whether answers are stable for each question ID.")
    print()

    file_name = input("Enter the data file name, or press Enter for sample_answers.txt: ")

    if file_name == "":
        file_name = "sample_answers.txt"

    answers_by_question = read_answers_from_file(file_name)

    if len(answers_by_question) == 0:
        print("No valid answer data was found.")
        return

    sci_by_question = calculate_question_sci_scores(answers_by_question)
    overall_sci = calculate_overall_sci(sci_by_question)

    print()
    print("Results")
    print("-------")

    for question_id in sci_by_question:
        print(question_id, "SCI:", round(sci_by_question[question_id], 2), "%")

    print()
    print("Overall SCI score:", round(overall_sci, 2), "%")
    print()

    print_most_unstable_groups(answers_by_question, sci_by_question)

    print()
    print("Opening heatmap window...")
    draw_heatmap(sci_by_question)


main()
