import unittest
import prepare_data
import io


class TestPrepareData(unittest.TestCase):

    def test_extract_article_and_abstract(self):
        initial_text = "".join([
            "Chelsea are waiting on the fitness of John Terry ahead of Wednesday's Champions League match with Valencia.",
            '\n', 'John Terry tries out his protective mask during training for Chelsea on Tuesday.\n',
            '\n',
            '\n', '@highlight\n', '\n',
            'The central defender underwent surgery on a broken cheekbone on Sunday'])

        expected_article = "chelsea are waiting on the fitness of john terry ahead of wednesday 's champions league match with valencia . " \
            "john terry tries out his protective mask during training for chelsea on tuesday ."
        expected_abstract = '<s> the central defender underwent surgery on a broken cheekbone on sunday . </s>'

        story = io.BytesIO(initial_text.encode())
        article, abstract = prepare_data.extract_article_and_abstract(story)

        self.assertEqual(expected_article, article, "Expected `{}`, got `{}`".format(expected_article, article))
        self.assertEqual(expected_abstract, abstract, "Expected `{}`, got `{}`".format(expected_abstract, abstract))


if __name__ == '__main__':
    unittest.main()