import logging

UNKNOWN_TOKEN = '<UNK>'


class Vocabulary(object):
    """Vocabulary class for mapping words and ids."""

    def __init__(self):
        self._word_to_id = {}
        self._id_to_word = {}
        self._vocab_size = 0

    def load_vocab(self, vocab_file, vocab_max_size):
        with open(vocab_file, 'r') as vocab_f:
            self.load_vocab_from_stream(vocab_f, vocab_max_size)

    def load_vocab_from_stream(self, vocab_stream, vocab_max_size):
        for line in vocab_stream:
            pieces = line.split()
            if len(pieces) != 2:
                logging.warning('Wrong line format: %', line)
                continue
            if pieces[0] in self._word_to_id:
                logging.warning('Duplicated word: %', pieces[0])
                continue
            self._word_to_id[pieces[0]] = self._vocab_size
            self._id_to_word[self._vocab_size] = pieces[0]
            self._vocab_size += 1

        if self._vocab_size > vocab_max_size:
            logging.warning('Too many words in vocab file, loaded only % words', vocab_max_size)

    def get_word_id(self, word):
        if word not in self._word_to_id:
            return self._word_to_id[UNKNOWN_TOKEN]
        return self._word_to_id[word]

    def get_word(self, word_id):
        if word_id not in self._id_to_word:
            raise ValueError('Vocab with id % not found', word_id)
        return self._id_to_word[word_id]

    def get_vocab_size(self):
        return self._vocab_size
