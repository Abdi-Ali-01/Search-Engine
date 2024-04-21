import nltk                            # Import the nltk library
from nltk.stem import PorterStemmer    # Import the PorterStemmer class from nltk.stem module

stemmer = PorterStemmer()              # Create an instance of the PorterStemmer class

words = ['jumps', 'jumped', 'jumping'] # Define a list of words to be stemmed

# Apply stemming to each word in the list using a list comprehension
stemmed_words = [stemmer.stem(word) for word in words]

# Loop through each word and its stemmed version and print them
for i in range(len(words)):
    print(words[i], "->", stemmed_words[i])
