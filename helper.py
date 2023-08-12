import spacy, re, os
import wikipedia, openai
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest
from dotenv import load_dotenv

load_dotenv()

INIT, SUCCESS = range(2)
OPENAI_KEY = os.environ.get("OPENAI_KEY")

nlp = spacy.load("en_core_web_sm")
openai.api_key = OPENAI_KEY


def calculate_weight(character_length):
    max_token = 4096
    tokens = (character_length // 4) + 1

    return max_token / tokens


def extractive_summary(input_text):
    keywords = []
    stopwords = list(STOP_WORDS)
    pos_tag = ["PROPN", "ADJ", "NOUN", "VERB"]

    doc = nlp(input_text)

    for token in doc:
        if token.text in stopwords or token.text in punctuation:
            continue

        if token.pos_ in pos_tag:
            keywords.append(token.text)

    # Tag Frequencies with Words
    freq_word = Counter(keywords)
    max_freq = freq_word.most_common(1)[0][1]

    # Normalize Frequencies
    for word in freq_word.keys():
        freq_word[word] = freq_word[word] / max_freq

    sent_strength = {}

    for sent in doc.sents:
        for word in sent:
            if word.text in freq_word.keys():
                if sent in sent_strength.keys():
                    sent_strength[sent] += freq_word[word.text]

                else:
                    sent_strength[sent] = freq_word[word.text]

    total_characters = sum(len(sent.text) for sent in doc.sents)
    weight = calculate_weight(total_characters)

    summary_length = int(len(sent_strength) * weight)
    summarized_sentences = nlargest(
        summary_length, sent_strength, key=sent_strength.get
    )

    sumarized_text = " ".join(w.text for w in summarized_sentences)

    return sumarized_text


def abstractive_summary(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k", messages=[{"role": "user", "content": prompt}]
    )

    summary = response["choices"][0]["message"]["content"]

    return SUCCESS, summary


def handle_input(query):
    urls = re.findall(r"https?://\S+|www\.\S+", query)

    if len(urls) != 1:
        # Restarts Flow
        return (
            INIT,
            "It seems like I can't find a valid url in your response. Please provide just one wikipedia url!",
        )

    url = urls[0]

    regex = r"https?://(?:en\.m\.wikipedia\.org|en\.wikipedia\.org)/wiki/\S+"

    is_not_wikipedia = re.match(regex, url) is None

    if is_not_wikipedia:
        # Restarts Flow
        return (
            INIT,
            "It seems like I can't find a valid wikipedia url in your response. Note that we only support wikipedia urls!",
        )

    title = " ".join(url.split("/")[-1].split("_"))
    wikisearch = wikipedia.page(title)
    input_text = wikisearch.content

    summarized_text = extractive_summary(input_text)

    prompt = "I want you to act as a wiki summarizer. I will provide a title, as well as an excerpt of the text gotten through extractive summary techniques. Your job is now to provide a comprehensive summary, one that is easy to follow, and understand."

    prompt += f"\n\n {title}"

    prompt += f"\n\n {summarized_text}"

    return abstractive_summary(prompt)
