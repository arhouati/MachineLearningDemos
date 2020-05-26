import numpy as np
import pandas as pd
import nltk

nltk.download('punkt')  # one time execution
from nltk.tokenize import sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import os

dirpath = os.getcwd()
slash = "\\"  # use '/' for mac or linux
path = dirpath + slash

# Read Data from csv
df = pd.read_csv(path + 'data' + slash + 'tennis_articles_v4.csv')

# split text into sentences
sentences = []
for s in df['article_text']:
    sentences.append(sent_tokenize(s))

# flatten list
sentences = [y for x in sentences for y in x]

# Extract word vectors
# get 400,000 different word vectors from pre-trained "Wikipedia 2014 + Gigaword 5 GloVe vectors"
# available here http://nlp.stanford.edu/data/glove.6B.zip
word_embeddings = {}
f = open(path + 'models' + slash + 'glove.6B.100d.txt', encoding='utf-8')
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    word_embeddings[word] = coefs
f.close()

# Text Preprocessing
# remove punctuations, numbers and special characters
clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")
# make alphabets lowercase
clean_sentences = [s.lower() for s in clean_sentences]

# Get rid of the stopwords
nltk.download('stopwords')

from nltk.corpus import stopwords

stop_words = stopwords.words('english')


# function to remove stopwords
def remove_stopwords(sen):
    sen_new = " ".join([i for i in sen if i not in stop_words])
    return sen_new


# remove stopwords from the sentences
clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]

# Extract word vectors
word_embeddings = {}
f = open(path + 'models' + slash + 'glove.6B.100d.txt', encoding='utf-8')
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    word_embeddings[word] = coefs
f.close()

sentence_vectors = []
for i in clean_sentences:
    if len(i) != 0:
        v = sum([word_embeddings.get(w, np.zeros((100,))) for w in
                 i.split()]) / (len(i.split()) + 0.001)
    else:
        v = np.zeros((100,))
    sentence_vectors.append(v)

# Similarity Matrix Preparation

# Initi the similarity matrix
sim_mat = np.zeros([len(sentences), len(sentences)])

# use Cosine Similarity to compute the similarity between a pair of sentences.
# initialize the matrix with cosine similarity scores.
for i in range(len(sentences)):
    for j in range(len(sentences)):
        if i != j:
            sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1, 100), sentence_vectors[j].reshape(1, 100))[
                0, 0]

# Applying PageRank Algorithm
nx_graph = nx.from_numpy_matrix(sim_mat)
scores = nx.pagerank(nx_graph)

# Summary Extraction
ranked_sentences = sorted(((scores[i], s) for i, s in
                           enumerate(sentences)), reverse=True)
# Extract top 10 sentences as the summary
for i in range(1):
    print(ranked_sentences[i][1])
