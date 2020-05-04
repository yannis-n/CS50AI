import nltk
import sys
import os
import string
from nltk.corpus import stopwords
from math import log

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()

    path =  os.path.dirname(os.path.abspath(__file__)) + os.sep + directory

    file_names = [f for f in os.listdir(path) if f.endswith("txt")]
    for file in file_names:
        file_path = os.path.join(path, file)
        with open(file_path, encoding="utf8") as f:
            files[file] = f.read()
    return files

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    stop_words = set(stopwords.words('english'))
    words = nltk.word_tokenize(document)
    words = list(map(lambda x:x.lower(), words))
    for word in words.copy():

        if word in string.punctuation:
            words.remove(word)
        if word in stop_words:
            words.remove(word)
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    word_set = set()
    word_idfs = dict()
    total_documents = len(documents)

    for file in documents:
        word_set.update(set(documents[file]))

    for word in word_set:
        f = sum(word in documents[file] for file in documents)
        # num = 0
        # for file in documents:
        #     if word in documents[file]:
        #         num += 1
        word_idfs[word] = log(total_documents / f)
    return word_idfs



def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    files_tfidf = [file for file in files]
    tfidf = list()
    for file in files:
        tfidf_sum = 0
        for word in query:
            tfidf_sum += files[file].count(word) * idfs[word]
        tfidf.append(tfidf_sum)
    files_tfidf = [files for tdidf,files in sorted(zip(tfidf, files_tfidf), reverse = True)]
    return files_tfidf[:n]

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # sentences_idfs = [sentence for sentence in sentences]
    mwm = list()
    for sentence in sentences:
        idf_sum = 0
        density = 0
        for word in query:
            if word in sentences[sentence]:
                density += sentences[sentence].count(word)
                idf_sum += idfs[word]
        mwm.append([sentence, idf_sum, density/len(sentences[sentence])])

    mwm_sorted = sorted(mwm, key=lambda x: (x[1], x[2]), reverse = True)
    sentences = [row[0] for row in mwm_sorted]
    return sentences[:n]


if __name__ == "__main__":
    main()
