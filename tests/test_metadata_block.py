# pylint: disable=R0201
from unittest.mock import Mock
import pytest
from manimlib.imports import *
from algomanim.metadata_block import MetadataBlock


mock_actpair1 = Mock()
mock_actpair2 = Mock()


def get_empty_metablock():
    return MetadataBlock('empty', [], 0, 0)

def get_test_metablock():
    return MetadataBlock('test', [mock_actpair1, mock_actpair2], 2, 10)


class TestMetadataBlock:

    def test_start_index_with_empty_action_pairs_throws_error(self):
        metablock = get_empty_metablock()
        with pytest.raises(Exception):
            metablock.start_index()

    def test_start_index_with_action_pairs_returns_first_index(self):
        metablock = get_test_metablock()
        mock_actpair1.reset_mock()
        mock_actpair2.reset_mock()

        metablock.start_index()

        mock_actpair1.get_index.assert_called_once()
        mock_actpair2.get_index.assert_not_called()

    def test_end_index_with_empty_action_pairs_throws_error(self):
        metablock = get_empty_metablock()
        with pytest.raises(Exception):
            metablock.end_index()

    def test_end_index_with_action_pairs_returns_last_index(self):
        metablock = get_test_metablock()
        mock_actpair1.reset_mock()
        mock_actpair2.reset_mock()

        metablock.end_index()

        mock_actpair2.get_index.assert_called_once()
        mock_actpair1.get_index.assert_not_called()

    def test_start_position_returns_normalised_start_time(self):
        metablock = get_test_metablock()
        assert metablock.start_position() == 2 * 1000

    def test_end_position_returns_normalised_end_time(self):
        metablock = get_test_metablock()
        assert metablock.end_position() == (2 + 10) * 1000
