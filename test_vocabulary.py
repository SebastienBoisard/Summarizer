import unittest
from vocabulary import Vocabulary
import io


class TestVocabulary(unittest.TestCase):

    def test_load_vocab(self):
        vocab = Vocabulary()
        vocab_file_stream = io.StringIO("word 2\ntest 4")
        vocab.load_vocab_from_stream(vocab_file_stream, 10)

        self.assertEqual(2, vocab.get_vocab_size(), "Expected vocab size = {}, got {}".format(1, vocab.get_vocab_size()))


if __name__ == '__main__':
    unittest.main()
