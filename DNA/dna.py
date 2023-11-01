import csv
import sys


def main():
    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # TODO: Read database file into a variable
    database = []
    with open(sys.argv[1]) as data:
        data_r = csv.DictReader(data)
        for row in data_r:
            database.append(row)

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as dna_file:
        dna = " ".join(char.rstrip() for char in dna_file)
        # Above function is for read and copy the txt file into a variable without including any systems symbol ([], '', \n)

    # TODO: Find longest match of each STR in DNA sequence
    # Copying all the subsequences from the database file (exclude the 'name')
    subsequences = []
    with open(sys.argv[1]) as data:
        reader = csv.DictReader(data)
        for element in reader.fieldnames:
            if element != "name":
                subsequences.append(element)

    # Using list comprehension to create a tuple contains a subsequence and its longest match in the dna sequence.
    list_of_subsequences = [(subsequence, str(longest_match(dna, subsequence)))for subsequence in subsequences]

    # TODO: Check database for matching profiles
    for row in database:
        # The all function takes an iterable and returns True if all elements in the iterable are True, and False if at least one element is False
        if all(row[key] == value for key, value in list_of_subsequences):
            print(row["name"])
            sys.exit(0)
    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):
        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:
            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run

main()
