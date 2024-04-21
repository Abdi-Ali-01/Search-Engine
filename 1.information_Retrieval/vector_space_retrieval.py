import math

# Corpus with documents as text
corpus = {
    'doc1': 'the quick brown fox',
    'doc2': 'jumped over the lazy dog',
    'doc3': 'the quick brown fox jumped over the lazy dog',
    'doc4': 'the lazy dog slept'
}

# Tokenize a document into words
def tokenize(doc):
    return doc.split()

# Calculate TF-IDF for a term in a document
def tfidf(term, doc):
    tf = doc.count(term) / len(tokenize(doc))
    idf = math.log(len(corpus) / sum(1 for d in corpus.values() if term in tokenize(d)))
    return tf * idf

# Create a TF-IDF vector for a document
def tfidf_vector(doc):
    vector = {}
    for term in set(tokenize(doc)):
        vector[term] = tfidf(term, doc)
    return vector

# Dictionary to store TF-IDF vectors for all documents
vectors = {}
for doc_id, doc in corpus.items():
    vectors[doc_id] = tfidf_vector(doc)

# Calculate cosine similarity between two vectors
def cosine_similarity(vec1, vec2):
    dot_product = sum(vec1.get(term, 0) * vec2.get(term, 0) for term in set(vec1) | set(vec2))
    norm1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
    norm2 = math.sqrt(sum(val ** 2 for val in vec2.values()))
    if norm1 * norm2 == 0:
        return 0  # prevent division by zero
    return dot_product / (norm1 * norm2)

# Retrieve documents similar to a query based on cosine similarity
def vector_space_retrieval(query):
    query_vec = tfidf_vector(query)
    results = []
    for doc_id, doc_vec in vectors.items():
        score = cosine_similarity(query_vec, doc_vec)
        results.append((doc_id, score))
    results.sort(key=lambda x: x[1], reverse=True)
    return results

# Example usage
query = "quick brown dog"
results = vector_space_retrieval(query)
print(f'Results for query: "{query}":')
for doc_id, score in results:
    print(f"{doc_id} \t {score:.4f}")
