from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx


def read_file(file_name):
    file = open(file_name, "r", encoding="utf8")
    filedata = file.read()

    filedata = filedata.replace("\n\n", " ")

    news = filedata.split(". ")
    sentences = []

    for sentence in news:
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop()
    return sentences


def sentence_similarity(sentence1, sentence2, stopwords=None):
    if stopwords is None:
        stopwords = []

    sentence1 = [word.lower() for word in sentence1]
    sentence2 = [word.lower() for word in sentence2]

    all_words = list(set(sentence1 + sentence2))

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    for word in sentence1:
        if word in stopwords:
            continue
        vector1[all_words.index(word)] += 1

    for word in sentence2:
        if word in stopwords:
            continue
        vector2[all_words.index(word)] += 1

    return 1 - cosine_distance(vector1, vector2)


def build_similarity_matrix(sentences, stop_words):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:
                continue
        similarity_matrix[idx1][idx2] = sentence_similarity(
                sentences[idx1], sentences[idx2], stop_words)
    return similarity_matrix


def generate_summary(file_name, words=500):
    stop_words = stopwords.words('english')
    summarize_text = []

    # Step 1 - Read text anc split it
    sentences = read_file(file_name)

    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

    # Step 3 - Rank sentences in similarity martix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)

    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i], s)
                             for i, s in enumerate(sentences)),
                             reverse=True)

    # print("Indexes of top ranked_sentence order are ", ranked_sentence)
    number_of_word = 0
    for i in range(80):
        summarize_text.append(" ".join(ranked_sentence[i][1]))
        number_of_word += len(summarize_text[i].split())
        if number_of_word >= words:
            break

    print(number_of_word)
    # Step 5 - Offcourse, output the summarize texr
    print("Summarize Text: \n", ". ".join(summarize_text) + ".")


# let's begin
generate_summary("news.txt", 500)
