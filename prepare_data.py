import os
import urllib.request


def print_download_progress(count, block_size, total_size):
    if count % 100 == 0:
        print("download progress {}%".format(count * block_size * 100 // total_size))


def download_file(url, filename, expected_bytes):
    """
    Download a file from an url, and make sure it has the right size.

    :param url: the url of the file to download
    :param filename: the name of the file on the disk
    :param expected_bytes: the expected size of the file to download
    """

    # Download the file from `url` and save it locally under `file_name`
    urllib.request.urlretrieve(url, filename, reporthook=print_download_progress)

    file_info = os.stat(filename)
    if file_info.st_size != expected_bytes:
        raise Exception('Error: expected `{}` to have {} bytes but got {}'.format(filename, expected_bytes, file_info.st_size))


def main():

    # cnn_url = "https://drive.google.com/uc?export=download&id=0BwmD_VLjROrfTHk4NFg2SndKcjQ"
    # cnn_file_size = 158577824

    test_url = "http://commondatastorage.googleapis.com/books1000/notMNIST_small.tar.gz"
    test_file_size = 8458043

    download_file(test_url, "test_file.tgz", test_file_size)


if __name__ == '__main__':
    main()
