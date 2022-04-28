import math


def get_paragraphs(file_name):
    with open(file_name, "r", encoding="utf8") as file:
        text = file.read()

    paragraphs = text.split("\n\n")

    return paragraphs


def get_sentences(file_name):
    with open(file_name, "r", encoding="utf8") as file:
        text = file.read()

    text = text.replace("\n", " ")
    tags = []
    for i in range(len(text)):
        if text[i] == "[":
            begin = i
        if text[i] == "]":
            end = i
            tags.append(text[begin:end+1])

    for tag in tags:
        text = text.replace(tag, "")

    text = text.replace("(", "")
    text = text.replace(")", "")

    sentences = text.split(".")
    sentences.pop()
    sentences = [sent.strip() for sent in sentences]

    return sentences


# IDF Score
def calculate_idf(word, paragraphs):
    word_count = 1
    count = len(paragraphs)
    for paragraph in paragraphs:
        if word in paragraph.split():
            word_count += 1

    idf = count / word_count

    return math.log(idf, 10)


# Centroid Score
def calculate_centroid(sentences, paragraphs):

    # Compute tf X idf score for each word
    TFIDF = {}
    for sent in sentences:
        words = sent.split()
        for word in words:
            if word not in TFIDF:
                TFIDF[word] = calculate_idf(word, paragraphs)
            else:
                TFIDF[word] += calculate_idf(word, paragraphs)

    # Centroid of Cluster
    # get words that are above the threshold

    centroid = {}
    threshold = 1.4
    for word in TFIDF:
        if(TFIDF[word] > threshold):
            centroid[word] = TFIDF[word]
        else:
            centroid[word] = 0

    # Sentence score
    sentence_score = []
    counter = 0
    for sent in sentences:
        sentence_score.append(0)
        for word in sent.split():
            sentence_score[counter] += centroid[word]

        counter = counter+1

    return sentence_score


paragraphs = get_paragraphs("machine_learning.txt")

sentences = get_sentences("machine_learning.txt")

sentence_score = calculate_centroid(sentences, paragraphs)


# get summarized
summary = ""
for i in range(len(sentences)):
    if(sentence_score[i] > 15):
        summary += sentences[i] + ". "

print(summary)
