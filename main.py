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

def find_combinations(titles, albums, letter_counts, current_titles, current_albums, results):
    if not titles and not albums:
        results.append((list(current_titles), list(current_albums)))
        return

    if not titles:
        for j, album in enumerate(albums):
            cleaned_album = album.replace(' ', '')
            if can_form(cleaned_album, letter_counts):
                current_albums.append(album)
                updated_counts = update_counts(cleaned_album, letter_counts)
                find_combinations([], albums[:j] + albums[j+1:], updated_counts, current_titles, current_albums, results)
                current_albums.pop()
                update_counts(cleaned_album, letter_counts, increment=True)
        return

    if not albums:
        for i, title in enumerate(titles):
            cleaned_title = title.replace(' ', '')
            if can_form(cleaned_title, letter_counts):
                current_titles.append(title)
                updated_counts = update_counts(cleaned_title, letter_counts)
                find_combinations(titles[:i] + titles[i+1:], [], updated_counts, current_titles, current_albums, results)
                current_titles.pop()
                update_counts(cleaned_title, letter_counts, increment=True)
        return

    for i, title in enumerate(titles):
        cleaned_title = title.replace(' ', '')
        if can_form(cleaned_title, letter_counts):
            current_titles.append(title)
            updated_counts = update_counts(cleaned_title, letter_counts)
            find_combinations(titles[:i] + titles[i+1:], albums, updated_counts, current_titles, current_albums, results)
            current_titles.pop()
            update_counts(cleaned_title, letter_counts, increment=True)

    for j, album in enumerate(albums):
        cleaned_album = album.replace(' ', '')
        if can_form(cleaned_album, letter_counts):
            current_albums.append(album)
            updated_counts = update_counts(cleaned_album, letter_counts)
            find_combinations(titles, albums[:j] + albums[j+1:], updated_counts, current_titles, current_albums, results)
            current_albums.pop()
            update_counts(cleaned_album, letter_counts, increment=True)

# Read the CSV file into a DataFrame
df = pd.read_csv('./songs.csv')

df = df.apply(lambda x: x.str.upper().apply(remove_parentheses_and_brackets))

# Drop duplicate rows based on 'Title', 'Album', and 'Lyrics' columns
df = df.drop_duplicates()

# Separate the columns into arrays (lists)
titles = df['Title'].drop_duplicates().tolist()
albums = df['Album'].drop_duplicates().tolist()
lyrics = df['Lyrics'].drop_duplicates().tolist()

available_words = ["Grlpwr", "Dream", "Family", "Smile", "Happy", "Love"]
available_letters = [letter for word in available_words for letter in word.upper()]

# Count the frequency of each letter in available letters
original_letter_counts = Counter(available_letters)

# Print out initial data for debugging
print(f"Titles: {titles}")
print(f"Albums: {albums}")
print(f"Original Letter Counts: {original_letter_counts}")

# Find all valid combinations
results = []
find_combinations(titles, albums, original_letter_counts.copy(), [], [], results)

# Output the possible combinations to verify the contents
for idx, (comb_titles, comb_albums) in enumerate(results):
    print(f"Combination {idx+1}:")
    print(" Titles:", comb_titles)
    print(" Albums:", comb_albums)
    print()

print(f"Total valid combinations: {len(results)}")

# Debugging prints to see if titles or albums can be formed individually
for title in titles:
    cleaned_title = title.replace(' ', '')
    if can_form(cleaned_title, original_letter_counts):
        print(f"Title '{title}' can be formed with the available letters")

for album in albums:
    cleaned_album = album.replace(' ', '')
    if can_form(cleaned_album, original_letter_counts):
        print(f"Album '{album}' can be formed with the available letters")
