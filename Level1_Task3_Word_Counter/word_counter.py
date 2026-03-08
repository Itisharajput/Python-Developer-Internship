Rajput Girl, [3/8/2026 11:48 AM]
# ============================================================
#   WORD COUNTER — Level 1, Task 3 (Basic)
#   Reads a text file and counts words, characters, lines
# ============================================================

import os

def count_words(text):
    words = text.split()
    return len(words)

def count_characters(text):
    return len(text)

def count_characters_no_spaces(text):
    return len(text.replace(" ", "").replace("\n", ""))

def count_lines(text):
    return len(text.splitlines())

def count_sentences(text):
    count = 0
    for char in text:
        if char in ['.', '!', '?']:
            count += 1
    return count

def count_word_frequency(text):
    words = text.lower().split()
    # Remove punctuation from words
    clean_words = []
    for word in words:
        clean = ""
        for char in word:
            if char.isalpha():
                clean += char
        if clean:
            clean_words.append(clean)

    frequency = {}
    for word in clean_words:
        frequency[word] = frequency.get(word, 0) + 1

    # Sort by frequency
    sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    return sorted_freq

def analyze_file(filepath):
    print("=" * 50)
    print("         WORD COUNTER & TEXT ANALYZER")
    print("=" * 50)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        print(f"\nFile: {filepath}")
        print("-" * 50)

        words      = count_words(content)
        chars      = count_characters(content)
        chars_ns   = count_characters_no_spaces(content)
        lines      = count_lines(content)
        sentences  = count_sentences(content)
        frequency  = count_word_frequency(content)

        print(f"  Total Words          : {words}")
        print(f"  Total Lines          : {lines}")
        print(f"  Total Sentences      : {sentences}")
        print(f"  Total Characters     : {chars}")
        print(f"  Characters (no space): {chars_ns}")

        if words > 0:
            avg = chars_ns / words
            print(f"  Avg Word Length      : {avg:.1f} characters")

        print(f"\n  Top 10 Most Used Words:")
        print("  " + "-" * 30)
        for i, (word, count) in enumerate(frequency[:10], 1):
            bar = "█" * count
            print(f"  {i:2}. {word:<15} {count:3} times  {bar}")

        print("\n" + "=" * 50)
        print("Analysis complete!")

    except FileNotFoundError:
        print(f"\nError: File '{filepath}' not found!")
        print("Please check the file path and try again.")
    except PermissionError:
        print(f"\nError: Permission denied to read '{filepath}'!")
    except Exception as e:
        print(f"\nUnexpected error: {e}")

def create_sample_file():
    sample = """Python is a powerful programming language.
Python is easy to learn and fun to use.
Many developers love Python for its simplicity.
Python is used in web development, data science, and AI.
Learning Python opens many career opportunities.
Python has a large and helpful community.
Python supports object oriented programming.
Python is great for beginners and experts alike.
"""
    with open("sample_text.txt", "w") as f:
        f.write(sample)
    print("Sample file 'sample_text.txt' created!")
    return "sample_text.txt"

def main():
    print("=" * 50)
    print("         WORD COUNTER — Level 1 Task 3")
    print("=" * 50)
    print("\n  1. Analyze an existing file")
    print("  2. Create sample file and analyze it")
    print("  3. Type text directly")

    choice = input("\nEnter choice (1/2/3): ").strip()

    if choice == "1":
        filepath = input("Enter file path: ").strip()
        analyze_file(filepath)

    elif choice == "2":
        filepath = create_sample_file()
        analyze_file(filepath)

Rajput Girl, [3/8/2026 11:48 AM]
elif choice == "3":
        print("\nType/paste your text below.")
        print("Press Enter twice when done:")
        lines = []
        empty_count = 0
        while empty_count < 1:
            line = input()
            if line == "":
                empty_count += 1
            else:
                empty_count = 0
                lines.append(line)
        text = "\n".join(lines)

        # Save to temp file and analyze
        with open("temp_input.txt", "w") as f:
            f.write(text)
        analyze_file("temp_input.txt")
        os.remove("temp_input.txt")

    else:
        print("Invalid choice!")

if name == "main":
    main()
