class InvertedIndex:
    def __init__(self):
        self.index = {}  # Initializes an empty dictionary to store the inverted index

    def add_document(self, document_id, document):
        terms = document.split()  # Split the document string into a list of words (terms)
        for position, term in enumerate(terms):  # Enumerate provides a counter (position) and the value (term)
            if term not in self.index:
                self.index[term] = {}  # If term not in index, initialize a new dictionary for this term
            if document_id not in self.index[term]:
                self.index[term][document_id] = []  # If document ID not in term's dictionary, initialize a new list
            self.index[term][document_id].append(position)  # Append the position of the term in the document

    def search(self, query):
        terms = query.split()  # Split the query into individual terms
        results = None  # Initialize results to None, to store the intersection of document IDs
        for term in terms:
            if term in self.index:  # Check if the term is in the index
                if results is None:
                    results = set(self.index[term].keys())  # Initialize results with set of document IDs for the first term
                else:
                    results.intersection_update(self.index[term].keys())  # Intersect current results with new set of document IDs

        if results is None:
            return []  # If no results found for any term, return empty list

        search_results = []
        for document_id in results:  # Iterate over each document ID found in results
            positions = [self.index[term][document_id] for term in terms if document_id in self.index[term]]  # Gather all term positions in each document
            search_results.append((document_id, positions))  # Append a tuple of document ID and list of positions to search_results

        return search_results  # Return the list of tuples (document IDs with positions of terms)

# Example usage:
index = InvertedIndex()
index.add_document(1, 'apple banana apple')  # Add a document with ID 1 and text
index.add_document(2, 'banana cherry')  # Add a document with ID 2 and text
index.add_document(3, 'apple cherry')  # Add a document with ID 3 and text

print('Documents added to the inverted index:')
print(index.index)  # Print the entire inverted index

query = "apple banana"
search_results = index.search(query)  # Perform a search for the query "apple banana"
print('Search results for query:', query)
print(search_results)  # Print the search results
