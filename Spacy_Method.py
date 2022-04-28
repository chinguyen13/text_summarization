import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


def read_file(file_name):
    file = open(file_name, "r", encoding="utf8")
    text = file.read()
    text = text.replace("\n", " ")

    # spacy.cli.download("en")
    nlp = spacy.load("en_core_web_sm")

    doc = nlp(text)
    return doc


def build_word_frequency(doc):
    word_frequencies = {}
    stopwords = list(STOP_WORDS)
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

    max_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency

    sentence_scores = build_sentence_scores(doc, word_frequencies)

    return sentence_scores


def build_sentence_scores(doc, word_frequencies):
    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text]
                else:
                    sentence_scores[sent] += word_frequencies[word.text]
    return sentence_scores


def build_summary(file_name, words=500):
    doc = read_file(file_name)

    sentence_scores = build_word_frequency(doc)
    number_of_word = 0
    for i in range(1, 80):
        summary = nlargest(i, sentence_scores, key=sentence_scores.get)
        number_of_word += len(summary[-1].text.split())
        if number_of_word >= words:
            break

    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)

    print(number_of_word)
    print("Summarize Text: \n" + summary)


build_summary("news.txt", 500)
