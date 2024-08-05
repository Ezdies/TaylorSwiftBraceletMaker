import pandas as pd
import re
from collections import Counter

def remove_parentheses_and_brackets(text):
    return re.sub(r"\[.*?\]|\(.*?\)", "", text).strip()

def can_form(word, letter_counts):
    word_counter = Counter(word)
    for letter, count in word_counter.items():
        if letter_counts[letter] < count:
            return False
    return True

def update_counts(word, letter_counts, increment=False):
    word_counter = Counter(word)
    for letter, count in word_counter.items():
        if increment:
            letter_counts[letter] += count
        else:
            letter_counts[letter] -= count
    return letter_counts

def find_all_combinations(items, letter_counts, current_combination, results):
    found = False

    for i, item in enumerate(items):
        cleaned_item = item.replace(' ', '').replace('\'', '').replace('!','')
        if can_form(cleaned_item, letter_counts):
            found = True
            current_combination.append(item)
            updated_counts = update_counts(cleaned_item, letter_counts)
            find_all_combinations(items[:i] + items[i+1:], updated_counts, current_combination, results)
            current_combination.pop()
            update_counts(cleaned_item, letter_counts, increment=True)

    if not found and current_combination:
        results.add(tuple(sorted(current_combination)))

# Sample data
df = pd.read_csv('./songs.csv')


# Clean the DataFrame
df = df.apply(lambda x: x.str.upper().apply(remove_parentheses_and_brackets))

# Drop duplicate rows based on 'Title', 'Album', and 'Lyrics' columns
df = df.drop_duplicates()

# Combine titles and albums into a single list
items = df['Title'].tolist() + df['Album'].drop_duplicates().tolist()

available_words = ["Grlpwr", "Dream", "Family", "Smile", "Happy", "Love"]
available_letters = [letter for word in available_words for letter in word.upper()]

# Count the frequency of each letter in available letters
original_letter_counts = Counter(available_letters)

# Print out initial data for debugging
print(f"Items: {items}")
print(f"Original Letter Counts: {original_letter_counts}")

# Find all valid combinations
results = set()

# Try starting combinations from any item
find_all_combinations(items, original_letter_counts.copy(), [], results)

# Output the possible combinations to verify the contents
for idx, combination in enumerate(results):
    print(f"Combination {idx+1}:")
    print(" Items:", combination)
    print()

print(f"Total valid combinations: {len(results)}")
