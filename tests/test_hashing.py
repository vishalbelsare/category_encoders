"""Tests for the HashingEncoder."""
from unittest import TestCase

import category_encoders as encoders
import pandas as pd
from pandas.testing import assert_frame_equal, assert_index_equal


class TestHashingEncoder(TestCase):
    """Tests for the HashingEncoder."""

    def test_must_not_reset_index(self):
        """Test that the HashingEncoder does not reset the index."""
        columns = ['column1', 'column2', 'column3', 'column4']
        df = pd.DataFrame([[i, i, i, i] for i in range(10)], columns=columns)
        df = df.iloc[2:8, :]
        target_columns = ['column1', 'column2', 'column3']

        single_process_encoder = encoders.HashingEncoder(max_process=1, cols=target_columns)
        single_process_encoder.fit(df, None)
        df_encoded_single_process = single_process_encoder.transform(df)
        assert_index_equal(df.index, df_encoded_single_process.index)
        self.assertEqual(df.shape[0],
                         pd.concat([df, df_encoded_single_process], axis=1).shape[0])

        multi_process_encoder = encoders.HashingEncoder(cols=target_columns)
        multi_process_encoder.fit(df, None)
        df_encoded_multi_process = multi_process_encoder.transform(df)
        assert_index_equal(df.index, df_encoded_multi_process.index)
        self.assertEqual(df.shape[0] , pd.concat([df, df_encoded_multi_process], axis=1).shape[0])

        assert_frame_equal(df_encoded_single_process, df_encoded_multi_process)

    def test_transform_works_with_single_row_df(self):
        """Test that the HashingEncoder works with a single row DataFrame."""
        columns = ['column1', 'column2', 'column3', 'column4']
        df = pd.DataFrame([[i, i, i, i] for i in range(10)], columns=columns)
        df = df.iloc[2:8, :]
        target_columns = ['column1', 'column2', 'column3']

        multi_process_encoder = encoders.HashingEncoder(cols=target_columns)
        multi_process_encoder.fit(df, None)
        df_encoded_multi_process = multi_process_encoder.transform(df.sample(1))

        self.assertEqual(
            multi_process_encoder.n_components + len(list(set(columns) - set(target_columns))),
            df_encoded_multi_process.shape[1]
        )

    def test_simple_example(self):
        """Test the HashingEncoder with a simple example."""
        df = pd.DataFrame(
            {
                'strings': ['aaaa', 'bbbb', 'cccc'],
                'more_strings': ['aaaa', 'dddd', 'eeee'],
            }
        )
        encoder = encoders.HashingEncoder(n_components=4, max_process=2)
        encoder.fit(df)
        expected_df = pd.DataFrame(
            {'col_0': [0, 1, 1], 'col_1': [2, 0, 1], 'col_2': [0, 1, 0], 'col_3': [0, 0, 0]}
        )
        pd.testing.assert_frame_equal(encoder.transform(df), expected_df)
