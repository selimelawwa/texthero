import pandas as pd
from texthero import preprocessing

from . import PandasTestCase

import unittest
import string


class TestPreprocessing(PandasTestCase):
    """
    Remove digits.
    """
    def test_remove_digits_only_block(self):
        s = pd.Series("remove block of digits 1234 h1n1")
        s_true = pd.Series("remove block of digits  h1n1")
        self.assertEqual(preprocessing.remove_digits(s), s_true)

    def test_remove_digits_block(self):
        s = pd.Series("remove block of digits 1234 h1n1")
        s_true = pd.Series("remove block of digits  hn")
        self.assertEqual(preprocessing.remove_digits(s, only_blocks=False),
                         s_true)

    def test_remove_digits_brackets(self):
        s = pd.Series("Digits in bracket (123 $) needs to be cleaned out")
        s_true = pd.Series("Digits in bracket ( $) needs to be cleaned out")
        self.assertEqual(preprocessing.remove_digits(s), s_true)

    def test_remove_digits_start(self):
        s = pd.Series("123 starting digits needs to be cleaned out")
        s_true = pd.Series(" starting digits needs to be cleaned out")
        self.assertEqual(preprocessing.remove_digits(s), s_true)

    def test_remove_digits_end(self):
        s = pd.Series("end digits needs to be cleaned out 123")
        s_true = pd.Series("end digits needs to be cleaned out ")
        self.assertEqual(preprocessing.remove_digits(s), s_true)

    def test_remove_digits_phone(self):
        s = pd.Series("+41 1234 5678")
        s_true = pd.Series("+  ")
        self.assertEqual(preprocessing.remove_digits(s), s_true)

    def test_remove_digits_punctuation(self):
        s = pd.Series(string.punctuation)
        s_true = pd.Series(string.punctuation)
        self.assertEqual(preprocessing.remove_digits(s), s_true)

    """
    Remove punctuation.
    """

    def test_remove_punctation(self):
        s = pd.Series("Remove all! punctuation!! ()")
        s_true = pd.Series(
            "Remove all  punctuation   ")    # TODO maybe just remove space?
        self.assertEqual(preprocessing.remove_punctuation(s), s_true)

    """
    Remove diacritics.
    """

    def test_remove_diactitics(self):
        s = pd.Series("hèllo")
        s_true = pd.Series("hello")
        self.assertEqual(preprocessing.remove_diacritics(s), s_true)

    """
    Remove whitespace.
    """

    def test_remove_whitespace(self):
        s = pd.Series("hello   world  hello        world ")
        s_true = pd.Series("hello world hello world")
        self.assertEqual(preprocessing.remove_whitespace(s), s_true)

    """
    Text pipeline.
    """

    def test_pipeline_stopwords(self):
        s = pd.Series("E-I-E-I-O\nAnd on")
        s_true = pd.Series("e-i-e-i-o\n ")
        pipeline = [preprocessing.lowercase, preprocessing.remove_stopwords]
        self.assertEqual(preprocessing.clean(s, pipeline=pipeline), s_true)
