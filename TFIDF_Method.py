import math


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

    sentences = text.split(". ")

    return sentences


# create sentence info
def get_doc(sentences):
    doc_info = []
    i = 0
    for sent in sentences:
        i += 1
        count = len(sent.split())
        temp = {"doc_id": i, "doc_length": count}
        doc_info.append(temp)

    return doc_info


# create word frequency
def create_freq_dict(sentences):
    i = 0
    freq_dict_list = []
    for sent in sentences:
        i += 1
        freq_dict = {}
        words = sent.split()
        for word in words:
            word = word.lower()
            if word not in freq_dict:
                freq_dict[word] = 1
            else:
                freq_dict[word] += 1
            temp = {"doc_id": i, "freq_dict": freq_dict}
        freq_dict_list.append(temp)

    return freq_dict_list


# get TF scores (score of each word in sentence)
def computeTF(doc_info, freq_dict_list):
    TF_scores = []
    for tempDict in freq_dict_list:
        _id = tempDict["doc_id"]
        for k in tempDict['freq_dict']:
            temp = {"doc_id": _id,
                    "TF_scores": tempDict["freq_dict"][k]/doc_info[_id-1]["doc_length"],
                    "key": k}

            TF_scores.append(temp)

    return TF_scores


# get IDF scores (score of each word in whole article)
def computeIDF(doc_info, freq_dict_list):
    IDF_scores = []
    i = 0
    for tempDict in freq_dict_list:
        i += 1
        for k in tempDict["freq_dict"]:
            count = sum([k in tempDict["freq_dict"] for tempDict in freq_dict_list])
            temp = {"doc_id": i, "IDF_scores": math.log(len(doc_info)/count,10), "key": k}
            IDF_scores.append(temp)

    return IDF_scores


# compute TF IDF (score TF*IDF)
def computeTFIDF(TF_scores, IDF_scores):
    TFIDF_scores = []
    for idf in IDF_scores:
        for tf in TF_scores:
            if idf['key'] == tf['key'] and idf['doc_id'] == tf['doc_id']:
                temp = {"doc_id": idf["doc_id"],
                        "TFIDF_scores": idf["IDF_scores"]*tf["TF_scores"],
                        "key": tf["key"]}
        TFIDF_scores.append(temp)

    return TFIDF_scores


# get sentence score (plus all TFIDF score of word in sentence)
def get_sent_score(TFIDF_scores, sentences, doc_info):
    sentence_info = []
    for doc in doc_info:
        sent_score = 0
        for i in range(len(TFIDF_scores)):
            temp_dict = TFIDF_scores[i]
            if doc["doc_id"] == temp_dict["doc_id"]:
                sent_score += temp_dict["TFIDF_scores"]
        temp = {"doc_id": doc["doc_id"],
                "sent_score": sent_score,
                "sentence": sentences[doc["doc_id"] - 1]}

        sentence_info.append(temp)

    return sentence_info


# get summary
def get_summary(sentence_info):
    _sum = 0
    summary = []
    array = []

    for temp_dict in sentence_info:
        _sum += temp_dict["sent_score"]

    average = _sum/len(sentence_info)

    for temp_dict in sentence_info:
        array.append(temp_dict["sent_score"])

    for sent in sentence_info:
        if sent["sent_score"] >= average:
            summary.append(sent["sentence"])

    summary = ". ".join(summary)

    return summary


sentences = get_sentences("machine_learning.txt")

doc_info = get_doc(sentences)

freq_dict_list = create_freq_dict(sentences)

TF_scores = computeTF(doc_info, freq_dict_list)
IDF_scores = computeIDF(doc_info, freq_dict_list)
TFIDF_scores = computeTFIDF(TF_scores, IDF_scores)

sent_scores = get_sent_score(TFIDF_scores, sentences, doc_info)

summary = get_summary(sent_scores)
print(summary)
