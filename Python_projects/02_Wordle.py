import random
import string

# Function to generate a random 5-letter word
def generate_word():
    return ''.join(random.choices(string.ascii_lowercase, k=5))

# Generate 600 words
words = [generate_word() for _ in range(600)]

# Join the words into a single text
text = '\n'.join(words)

# Save to a .txt file
file_path = "02_Wordle.txt"
with open(file_path, "w") as file:
    file.write(text)

print(f"File saved as {file_path}")