from vocabulary import Vocabulary
import io


def test_load_vocab():
    vocab = Vocabulary()
    vocab_file_stream = io.StringIO("word 2\ntest 4")
    vocab.load_vocab_from_stream(vocab_file_stream, 10)

    assert vocab.get_vocab_size() == 2
