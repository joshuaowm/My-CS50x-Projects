# TODO
def main():
    text = input("Text: ")
    l = count_letters(text) / count_words(text) * 100
    s = count_sentences(text) / count_words(text) * 100
    cl_index = round(0.0588 * l - 0.296 * s - 15.8)
    print_grade(cl_index)


def count_letters(text):
    counter = 0
    for char in text:
        if char.isalpha():
            counter += 1
    return counter


def count_words(text):
    counter = 1
    for space in text:
        if space.isspace():
            counter += 1
    return counter


def count_sentences(text):
    counter = 0
    for punc in text:
        if punc in [".", "?", "!"]:
            counter += 1
    return counter


def print_grade(n):
    if n < 1:
        print("Before Grade 1")
    elif 1 <= n <= 15:
        print(f"Grade {n}")
    else:
        print("Grade 16+")


main()
