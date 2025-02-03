"""
Given a list of sentences, the markov model takes note of how often it witnesses a transition from one word to another.

Implementation:
- Uses a symbol dictionary to save memory (only one instance of each word)
- Only words seen as sentence starts are used to start a sentence
- Does not take into account weights for sentence starts
- Takes into account weights for transitions and for sentence ends

"""
from collections import defaultdict
from random import choice, sample
from typing import (Dict, List, Set)


SENTENCE_END_DELIMITER = "."


class MarkovModel:

    def __init__(self):
        self.dictionary: Dict[int, str] = {}
        self.transitions : Dict[int, Dict[int, int]] = {}
        self.sentence_start_words: Set[int] = set()

    def debug_model(self):
        print("Symbols Dictionary:", self.dictionary)
        print("Start words:", self.sentence_start_words)
        print("Transitions:", self.transitions)

    def build_model(self, sentences: List[str]):
        sentence_end_index = self._get_word_index(SENTENCE_END_DELIMITER)

        for sentence in sentences:
            sentence_words = sentence.lower().split(" ")
            if len(sentence_words) < 2:
                raise ValueError("Sentences must be at least two words")
            # we want to stop at the second to last word, as we always compare i with i+1
            for index in range(len(sentence_words) - 1):
                word_index = self._get_word_index(sentence_words[index])

                if index == 0:
                    self.sentence_start_words.add(word_index)

                next_word_index = self._get_word_index(sentence_words[index+1])

                self._add_transition(word_index, next_word_index)

                # last word in sentence
                if index == len(sentence_words) - 2:
                    self._add_transition(next_word_index, sentence_end_index)

    def build_markov_sentence(self, max_words: int) -> str:
        # Note that we don't take into account weights for picking the starting word
        first_word_index = choice(list(self.sentence_start_words))
        first_word = self.dictionary[first_word_index]

        words = [first_word] + self._do_build_markov_sentence(current_word_index=first_word_index, word_count=1, max_words=max_words)

        words[0] = words[0].capitalize()
        return " ".join(words[:-1]) + words[-1]

    def _do_build_markov_sentence(self, current_word_index: int, word_count: int, max_words: int) -> List[str]:
        # surpassed max words
        if word_count > max_words:
            return [SENTENCE_END_DELIMITER]

        potential_next_words = self.transitions[current_word_index]

        new_word_index = sample(list(potential_next_words.keys()), 1)[0]
        new_word = self.dictionary[new_word_index]

        # chosen to end the sentence
        if new_word == SENTENCE_END_DELIMITER:
            return [new_word]

        return [new_word] + self._do_build_markov_sentence(
            current_word_index=new_word_index, word_count=word_count + 1, max_words=max_words
        )

    def _get_word_index(self, word: str) -> int:
        word_index = len(self.dictionary)
        if word not in self.dictionary.values():
            self.dictionary[word_index] = word
        else:
            word_index = [k for k, v in self.dictionary.items() if v == word][0]

        return word_index

    def _add_transition(self, current: int, next: int):
        if current not in self.transitions:
            self.transitions[current] = defaultdict(int)
        self.transitions[current][next] += 1


def load_sentences(filename: str) -> List[str]:
    sentences = []
    with open(filename, "r", encoding="utf8") as sentences_file:
        sentence = sentences_file.readline()
        while sentence:
            # TODO: regex to only leave alphanumeric characters and spaces
            sentence = sentence.replace(",", "").replace(":", "").replace(";", "").replace("\n", "").replace("\"", "")
            sentences.append(sentence)
            sentence = sentences_file.readline()
    if not sentences:
        raise ValueError("File has no sentences!")
    return sentences


if __name__ == '__main__':
    markov_model = MarkovModel()

    input_file = "markov_quotes.txt"
    markov_model.build_model(load_sentences(input_file))

    # markov_model.debug_model()

    max_sentence_words = 20
    num_sentences = 10

    for _ in range(num_sentences):
        print(markov_model.build_markov_sentence(max_sentence_words))
