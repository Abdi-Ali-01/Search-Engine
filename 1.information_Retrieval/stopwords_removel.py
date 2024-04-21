import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Ensure stopwords are downloaded from the NLTK library
nltk.download('stopwords')

# Example sentence for demonstrating the removal of stopwords
original_text = "This is an example sentence demonstrating the removal of stopwords."

# Tokenize the text, i.e., split the sentence into individual words
tokens = word_tokenize(original_text)

# Load stopwords, a set of commonly used words that may be omitted in some contexts
stop_words = set(stopwords.words('english'))

# Remove stopwords from the tokenized text
filtered_words = [word for word in tokens if word not in stop_words]

# Convert the list of filtered words back into a single string
filtered_text = ' '.join(filtered_words)

# Print the original text and the text after stopwords have been removed
print("Original text:", original_text)
print("After removal of stopwords:", filtered_text)
