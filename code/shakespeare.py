import csv
import os
import re

INPUT_DIR = os.path.join("data", "shakespeare")
STOPWORDS_PATH = os.path.join(INPUT_DIR, "stopwords.txt")
SHAKESPEARE_PATH = os.path.join(INPUT_DIR, "shakespeare.txt")
OUTPUT_DIR = "artifacts"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "shakespeare_report.csv")

NUM_LINES_TO_SKIP = 246
LAST_LINE_START = "End of this Etext"


def load_stopwords():
    """Load the stopwords from the file and return a set of the cleaned stopwords."""

    stopwords = set()

    with open(STOPWORDS_PATH, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip().lower()
            stopwords.add(re.sub(r'[^a-z]', '', line))

    return stopwords


def load_shakespeare_lines():
    "Loads every line in the dataset that was written by Shakespeare as a list of strings."

    shakespeare_lines = []

    with open(SHAKESPEARE_PATH, 'r', encoding='utf-8') as file:
        for _ in range(NUM_LINES_TO_SKIP):
            next(file)
        
        for line in file:
            if line.startswith(LAST_LINE_START):
                break
            line = line.strip()
            if not (line.startswith('<<') and line.endswith('>>')):
                shakespeare_lines.append(line)
    return shakespeare_lines


def get_shakespeare_words(shakespeare_lines):
    """Takes the lines and makes a list of lowercase words."""
    words = []
    for line in shakespeare_lines:
        clean_line = re.sub(r'[^a-z\s]', '', line.lower())
        words.extend(clean_line.split())
    return words


def count_words(words, stopwords):
    """Counts the words that are not stopwords.
    returns a dictionary with words as keys and values."""
    word_counts = {}
    for word in words:
        if word and word not in stopwords:
            word_counts[word] = word_counts.get(word, 0) + 1
    return word_counts


def sort_word_counts(word_counts):
    """Takes a dictionary or word counts.
    Returns a list of (word, count) tuples that are sorted by count in descending order."""

    sorted_word_counts = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)

    return sorted_word_counts


def write_word_counts(sorted_word_counts, path):
    """Takes a list of (word, count) tuples and writes them to a CSV."""

    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['word', 'count'])
        writer.writerows(sorted_word_counts)


if __name__ == "__main__":

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Loading stopwords...")
    stopwords = load_stopwords()
    print(f"Loaded {len(stopwords)} stopwords.")

    print("Loading Shakespeare lines...")
    shakespeare_lines = load_shakespeare_lines()
    print(f"Loaded {len(shakespeare_lines)} lines from Shakespeare.")

    print("Processing words...")
    shakespeare_words = get_shakespeare_words(shakespeare_lines)
    print(f"Processed {len(shakespeare_words)} words.")

    print("Counting words...")
    word_counts = count_words(shakespeare_words, stopwords)
    print(f"Counted {len(word_counts)} unique words.")

    print("Sorting word counts...")
    word_counts_sorted = sort_word_counts(word_counts)
    print("Word counts sorted.")

    print("Writing word counts to CSV...")
    write_word_counts(word_counts_sorted, OUTPUT_PATH)
    print(f"CSV file written to {OUTPUT_PATH}.")