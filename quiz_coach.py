# reads libraries in the current directory
import glob
import json
import random
import textwrap


def read_questions_from_library(library):
    with open(library, "r") as file:
        questions = json.load(file)
    return questions


def select_library():
    libraries = glob.glob("*.json")
    print("\nSelect a library:\n")
    for i in range(len(libraries)):
        print(f"{i+1}) {libraries[i]}")
    print()
    library = input("> ")
    return libraries[int(library) - 1]


def main():
    print()
    print("--------- Welcome to Quiz Coach! ---------\n")
    library = select_library()

    while True:
        print()
        print("Select an option:")
        print()
        print(f"  1. Select a new library [{library}]")
        print("  2. Start a new quiz")
        print()
        print("  Q. Exit")
        print()
        option = input("> ")

        if option == "1":
            library = select_library()
        elif option == "2":
            print()
            print("Starting a new quiz...")
            print()
            make_quiz(library)
        elif option.upper() == "Q":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")
            print()
            continue


def select_question_number(frequencies):
    question_numbers = [
        i_question for i_question, freq in enumerate(frequencies) for f in range(freq)
    ]
    return random.choice(question_numbers)


def grade_question(i_question, question):

    #
    print("-" * 70)
    print()
    print(f"Question {i_question + 1}")
    print()

    #
    question_text = question["question"].split("\n\n")
    paragraph = textwrap.fill(question_text[0], width=70)
    print(paragraph)

    if len(question_text) > 1:
        paragraph = textwrap.fill(question_text[1], width=70)
        print()
        print(paragraph)

    print()

    #
    choices = question["choices"]
    correct_answers = question["answer"]
    indexes = list(range(len(choices)))

    if len(choices) > 2:
        random.shuffle(indexes)

    choices = [choices[i] for i in indexes]
    correct_answers = [indexes.index(ans) for ans in correct_answers]

    for i_choice, choice in enumerate(choices):
        choice_text = textwrap.fill(
            choice, width=67, initial_indent="", subsequent_indent="   "
        )
        print(f"{i_choice + 1}. {choice_text}")
        print()

    answer = input("> ")
    answer = answer.split()
    answer = set(int(ans) - 1 for ans in answer)

    is_correct = True

    if len(answer) != len(correct_answers):
        is_correct = False

    if is_correct:
        for ans in answer:
            if ans not in correct_answers:
                is_correct = False
                break

    if is_correct:
        print()
        print("Correct!")
        print("\n")
        return True

    print()
    print("Incorrect.")
    print()
    if len(correct_answers) > 1:
        print("The correct answers are:")
        print()
        for ans in correct_answers:
            text = textwrap.fill(
                choices[ans], width=67, initial_indent="", subsequent_indent="   "
            )
            print(f"{ans+1}. {text}")

    else:
        print("The correct answer is:")
        print()
        text = textwrap.fill(
            choices[correct_answers[0]],
            width=67,
            initial_indent="",
            subsequent_indent="   ",
        )
        print(f"{correct_answers[0]+1}. {text}")

    print()
    return False


def recalculate_frequencies(frequencies, selected_question, is_correct):
    if is_correct:
        frequencies[selected_question] = max(1, frequencies[selected_question] - 1)
    else:
        frequencies[selected_question] += 5
    return frequencies


def make_quiz(library):

    questions = read_questions_from_library(library)
    n_questions = len(questions)
    frequencies = [5] * n_questions

    repeat = True
    n_correct = 0

    while repeat:

        for i_question in range(20):

            selected_question = select_question_number(frequencies)
            is_correct = grade_question(i_question, questions[selected_question])
            frequencies = recalculate_frequencies(
                frequencies, selected_question, is_correct
            )

            if is_correct:
                n_correct += 1

        print("-" * 70)
        print()
        print("Quiz complete.")
        print()
        print("Your score is:", int(float(n_correct) / 20.0 * 100), "%\n")
        answer = input("Do you a new round of questions? (y/n) > ")
        print()

        if answer.lower() == "n":
            repeat = False
        else:
            n_correct = 0


if __name__ == "__main__":

    main()
