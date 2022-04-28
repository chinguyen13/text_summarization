from string import punctuation
from nltk.corpus import stopwords


def clean_data(file_name):
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

    return text


def get_sentences(text):
    sentences = text.split(".")
    sentences.pop()
    sentences = [sent.strip() for sent in sentences]

    return sentences


def get_word_freg(text, sentences):
    # take stopwords
    stop_words = stopwords.words('english')

    word_freq = {}
    for word in text.split():
        if word not in stop_words:
            if word not in word_freq:
                word_freq[word] = 1
            else:
                word_freq[word] += 1

    word_freq_in_sents = {}
    for word in word_freq.keys():
        word_freq_in_sents[word] = word_freq[word]/len(sentences)

    return word_freq_in_sents


def get_centroid_scores(word_freq_in_sents):
    threshold = 0.05
    centroid_scores = {}
    for word in word_freq_in_sents.keys():
        if word_freq_in_sents[word] > threshold:
            centroid_scores[word] = word_freq_in_sents[word]
        else:
            centroid_scores[word] = 0

    return centroid_scores


def get_sent_score(centroid_scores, sentences):
    sent_scores = []
    count = 0

    for sent in sentences:
        sent_scores.append(0)
        for word in sent.split():
            if word in centroid_scores:
                sent_scores[count] += centroid_scores[word]
        count += 1

    return sent_scores


def get_summary(file_name):

    text = clean_data(file_name)

    sentences = get_sentences(text)

    for special_char in punctuation:
        text = text.replace(special_char, "")

    word_freq = get_word_freg(text, sentences)

    centroid_scores = get_centroid_scores(word_freq)

    sent_scores = get_sent_score(centroid_scores, sentences)

    summary_list = []
    for i in range(len(sentences)):
        if sent_scores[i] >= 1.6:
            summary_list.append(sentences[i])

    final_summary = ". ".join(summary_list)
    final_summary += "."

    print(final_summary)


get_summary("machine_learning.txt")
