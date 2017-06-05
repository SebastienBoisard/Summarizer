import os
import urllib.request
import tarfile
import collections
from nltk.tokenize import word_tokenize
import tensorflow as tf

# List of tokens that are acceptable ways to end a sentence
END_TOKENS = ['.', '!', '?', '...', "'", "`", '"', ")",
              u'\u2019',  # single close quote
              u'\u201d',  # dm_double_close_quote
              ]

SENTENCE_START = '<s>'
SENTENCE_END = '</s>'


def print_download_progress(count, block_size, total_size):
    if count % 100 == 0:
        print("download progress {}%".format(count * block_size * 100 // total_size))


def download_file(url, filename, path, expected_bytes):
    """
    Download a file from an url, and make sure it has the right size.

    :param url: the url of the file to download
    :param filename: the name of the file on the disk
    :param path: the path to the folder that will contain the downloaded file
    :param expected_bytes: the expected size of the file to download
    """

    # Verify if the parameter `path` is a directory
    if not os.path.isdir(path):
        raise Exception('Error: expected `{}` to be a directory'.format(path))

    # Download the file from `url` and save it locally under `file_name`
    urllib.request.urlretrieve(url, path+filename, reporthook=print_download_progress)

    file_info = os.stat(path+filename)
    if file_info.st_size != expected_bytes:
        raise Exception('Error: expected `{}` to have {} bytes but got {}'.format(filename, expected_bytes, file_info.st_size))


def fix_missing_period(line):
    """Adds a period to a line that is missing a period

    :param line: a string containing the line to analyze
    :return string: the original string or a new string with an added period at the end
    """
    if "@ highlight" in line:
        return line
    if line == "":
        return line
    if line[-1] in END_TOKENS:
        return line
    return line + " ."


def extract_article_and_abstract(story_buf):
    """
    Extract the article and the abstract from the a story file, after lowercase/tokenize/fix them.

    :param story_buf: an io.BufferedReader for the current story file
    :return: a string for the article and another for the abstract that have been extracted from the story file
    """

    lines = []
    for line in story_buf:
        lines.append(line.decode("utf-8"))

    # Separate properly each word and punctuation with a tokenizer from NLTK.
    lines = [" ".join(word_tokenize(line)) for line in lines]

    # Lowercase everything
    lines = [line.lower() for line in lines]

    # Put periods on the ends of lines that are missing them (this is a problem in the dataset because many
    # image captions don't end in periods; consequently they end up in the body of the article as run-on sentences)
    lines = [fix_missing_period(line) for line in lines]

    # Separate out article and abstract sentences
    article_lines = []
    highlights = []
    next_is_highlight = False
    for idx, line in enumerate(lines):
        # print("line[{}]={}".format(idx, line))
        if line == "":
            continue  # empty line
        elif line.startswith("@ highlight"):
            next_is_highlight = True
        elif next_is_highlight:
            highlights.append(line)
        else:
            article_lines.append(line)

    # Make article into a single string
    article = ' '.join(article_lines)

    # Make abstract into a sinhle string, putting <s> and </s> tags around the sentences
    abstract = ' '.join(["{} {} {}".format(SENTENCE_START, sent, SENTENCE_END) for sent in highlights])

    return article, abstract


def get_tokens_from_article_and_abstract(article, abstract):
    # Get tokens from the article string
    article_tokens = article.split(' ')

    # Get tokens from the abstract string
    abstract_tokens = abstract.split(' ')

    # Remove start and end sentence tokens
    abstract_tokens = [t for t in abstract_tokens if t not in [SENTENCE_START, SENTENCE_END]]

    tokens = article_tokens + abstract_tokens

    # Strip tokens from leading spaces
    tokens = [t.strip() for t in tokens]

    # Remove empty tokens
    tokens = [t for t in tokens if t != ""]  # remove empty

    return tokens


def main():

    # cnn_url = "https://drive.google.com/uc?export=download&confirm=1E-H&id=0BwmD_VLjROrfTHk4NFg2SndKcjQ"
    # cnn_file_size = 158577824

    test_url = "http://commondatastorage.googleapis.com/books1000/notMNIST_small.tar.gz"
    test_file_size = 8458043
    test_filename = "test_stories.tgz"
    test_folder = "data/"

    if not os.path.isfile(test_folder+test_filename):
        download_file(test_url, test_filename, test_folder, test_file_size)

    # Open tarfile
    tar = tarfile.open(mode="r:gz", name=test_folder+test_filename)

    # Prepare to count each token in the dataset (vocab_counter['token_label']=token_count)
    vocab_counter = collections.Counter()

    output_file = test_folder+"output.bin"

    writer = tf.python_io.TFRecordWriter(output_file)

    # Iterate over every member
    for idx, tar_filename in enumerate(tar.getnames()):
        # Print contents of every file
        if not tar_filename.endswith('.story'):
            continue

        buf = tar.extractfile(tar_filename)

        if idx > 2:
            break

        article, abstract = extract_article_and_abstract(buf)
        print("article=", article)
        print("abstract=", abstract)

        # Construct the Example proto object
        example = tf.train.Example(
            # Example contains a Features proto object
            features=tf.train.Features(
                # Features contains a map of string to Feature proto objects
                feature={
                    # A Feature contains one of either a int64_list,
                    # float_list, or bytes_list
                    'article': tf.train.Feature(bytes_list=tf.train.BytesList(value=[str.encode(article)])),
                    'abstract': tf.train.Feature(bytes_list=tf.train.BytesList(value=[str.encode(abstract)])),
                }))
        # Use the proto object to serialize the example to a string
        serialized = example.SerializeToString()

        # Write the serialized object to disk
        writer.write(serialized)

        tokens = get_tokens_from_article_and_abstract(article, abstract)
        vocab_counter.update(tokens)

if __name__ == '__main__':
    main()
