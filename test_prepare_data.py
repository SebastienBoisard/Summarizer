import prepare_data
import io


def test_extract_article_and_abstract():
    initial_text = "".join([
        "Chelsea are waiting on the fitness of John Terry ahead of Friday's Champions League match with Valencia.",
        '\n', 'John Terry tries out his protective mask during training for Chelsea on Tuesday.\n',
        '\n',
        '\n', '@highlight\n', '\n',
        'The central defender underwent surgery on a broken cheekbone on Sunday'])

    expected_article = "chelsea are waiting on the fitness of john terry ahead of friday 's champions league match with valencia . " \
        "john terry tries out his protective mask during training for chelsea on tuesday ."
    expected_abstract = '<s> the central defender underwent surgery on a broken cheekbone on sunday . </s>'

    story = io.BytesIO(initial_text.encode())
    article, abstract = prepare_data.extract_article_and_abstract(story)

    assert article == expected_article
    assert abstract == expected_abstract
