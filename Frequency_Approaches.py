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

        return text


def get_word_scores(text, stop_words):
    word_freq = {}
    for word in text.split():
        if word.lower() not in stop_words:
            if word not in word_freq:
                word_freq[word] = 1
            else:
                word_freq[word] += 1

    word_scores = word_scores_process(word_freq)

    return word_scores


def word_scores_process(word_freq):
    word_scores = {}
    for word in word_freq.keys():
        if word not in word_scores:
            word_scores[word] = word_freq[word]/len(word_freq)

    return word_scores


def get_best_sent(sentences, word_scores):
    sent_scores = {}
    for sent in sentences:
        word_count = 0
        for word in sent.split():
            if word in word_scores.keys():
                word_count += 1
                if sent not in sent_scores:
                    sent_scores[sent] = word_scores[word]
                else:
                    sent_scores[sent] += word_scores[word]
        sent_scores[sent] = sent_scores[sent]/word_count

    best_sent = max(sent_scores, key=sent_scores.get)

    return best_sent


def update_word_scores(best_sent, word_scores):
    for word in best_sent.split():
        if word in word_scores.keys():
            word_scores[word] = word_scores[word]*word_scores[word]

    return word_scores


def get_summary(file_name, number_of_words):
    # get text and sentences
    text = clean_data(file_name)
    sentences = text.split(".")
    sentences.pop()
    sentences = [sent.strip() for sent in sentences]

    # remove punctuation and get words
    for special_char in punctuation:
        text = text.replace(special_char, "")

    # take stopwords
    stop_words = stopwords.words('english')

    # get word scores
    word_scores = get_word_scores(text, stop_words)

    # get sents based on number of sentences
    final_summary = []
    word_count = 0
    for i in range(len(sentences)):
        best_sent = get_best_sent(sentences, word_scores)

        final_summary.append(best_sent)
        
        word_count += len(best_sent.split())
        if word_count >= number_of_words:
            break
        word_scores = update_word_scores(best_sent, word_scores)

    # get summary

    summary = ". ".join(final_summary)
    summary += "."
    print("Summarized Text: \n" + summary)


get_summary("machine_learning.txt", 500)
