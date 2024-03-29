"""
Given a list of sentences, the markov model takes note of how often it witnesses a transition from one word to another.

SOLUTION NOTE:
While using sets for the values removes some repetition, in order to really save memory the way to go would be to build
a word dictionary and make the model store dictionary indexes, so each word really appears just once and the sets
contain only integers (instead of strings as now)

"""
from collections import defaultdict
from random import choice
from typing import (Dict, List, Optional, Set)


SENTENCE_START_DELIMITER = "@@"
SENTENCE_END_DELIMITER = "||"


def build_model(sentences: List[str]) -> Dict:
    model = defaultdict(set)  # type: Dict[str, Set]

    # NOTE: explicitly removing repetitions, as `love -> love` in `Do what you love, love what you do`
    # but if input sentences have them, an alternative is to leave them as valid

    for sentence in sentences:
        words = sentence.split(" ")
        if len(words) < 2:
            raise ValueError("Sentences must be at least two words!")
        for index, word in enumerate(words):
            if index == 0:
                model[word].add(SENTENCE_START_DELIMITER)
                if words[index+1] not in model[word]:
                    model[word].add(words[index+1])
            elif index == len(words) - 1:
                model[word].add(SENTENCE_END_DELIMITER)
            else:
                if words[index+1] not in model[word]:
                    model[word].add(words[index+1])

    return model


def build_markov_sentence(model: Dict[str, Set], max_words: int) -> str:
    words = do_build_markov_sentence(current_word=None, model=model, word_count=0, max_words=max_words)
    return " ".join(words)


def do_build_markov_sentence(
    current_word: Optional[str], model: Dict[str, Set], word_count: int, max_words: int
) -> List[str]:
    # 1st word scenario: find a valid sentence start
    if current_word is None:
        current_word = choice(list(model.keys()))  # really not needing these casts but to silence the linter
        while SENTENCE_START_DELIMITER not in model[current_word]:
            current_word = choice(list(model.keys()))

        return [current_word] + do_build_markov_sentence(
            current_word=current_word, model=model, word_count=word_count + 1, max_words=max_words
        )

    is_valid_word = False
    while not is_valid_word:
        new_word = choice(list(model[current_word]))
        # we should ignore start delimiter
        if new_word != SENTENCE_START_DELIMITER:
            is_valid_word = True
        # but we don't want one-word sentences either
        if new_word == SENTENCE_END_DELIMITER and word_count == 0:
            is_valid_word = False

    # we're done
    if new_word == SENTENCE_END_DELIMITER:
        return ["."]

    if word_count + 1 < max_words:
        return [new_word] + do_build_markov_sentence(
            current_word=new_word, model=model, word_count=word_count + 1, max_words=max_words
        )

    # if still here, we're also done because we reached maximum sentence length
    return [new_word, "..."]


def _load_sentences(filename: str) -> List[str]:
    sentences = []
    with open(filename, "r") as sentences_file:
        sentence = sentences_file.readline()
        while sentence:
            sentence = sentence.replace(",", "").replace(":", "").replace(";", "").replace("\n", "").replace("\"", "")
            sentences.append(sentence)
            sentence = sentences_file.readline()
    if not sentences:
        raise ValueError("File has no sentences!")
    return sentences


if __name__ == '__main__':
    # simple example using some quotes
    filename = "markov_quotes.txt"
    max_words = 20

    # more complex example from a TED talk
    # https://www.ted.com/talks/jeremy_howard_the_wonderful_and_terrifying_implications_of_computers_that_can_learn/
    # filename = "markov_ted_talk.txt"
    # max_words = 30

    sentences = _load_sentences(filename=filename)
    model = build_model(sentences)

    # uncomment this to see the full model (in the end is a Dict)
    # print(model)

    for _ in range(10):
        markov_sentence = build_markov_sentence(model=model, max_words=max_words)
        print(markov_sentence)
