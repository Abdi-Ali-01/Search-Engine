import nltk
nltk.download('punkt')  # Download the 'punkt' tokenizer models for tokenization

from nltk.stem import WordNetLemmatizer  # Import the WordNetLemmatizer for lemmatization

# Tokenization
sentence = "the bats were hanging by their feet"  # Define a sentence to be processed
tokenized_word = nltk.word_tokenize(sentence)  # Tokenize the sentence into individual words

print(f"Tokenized sentence {tokenized_word}")  # Print the list of tokenized words

lemmatizer = WordNetLemmatizer()  # Create an instance of WordNetLemmatizer
lemmatized_words = [lemmatizer.lemmatize(word) for word in tokenized_word]  # Lemmatize each word in the tokenized list

print(f"Lemmatized words = {lemmatized_words}")  # Print the list of lemmatized words
