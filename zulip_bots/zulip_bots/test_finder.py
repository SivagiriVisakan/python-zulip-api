from zulip_bots import finder
import unittest
from unittest import TestCase

from unittest import mock
from unittest.mock import patch


class FinderTestCase(TestCase):

    def test_resolve_bot_path_for_custom_bot(self):

        with patch('os.path.isfile', return_value=True), \
                patch('os.path.abspath', return_value='path/to/custom_handler.py'):

            custom_bot_handlers = ['custom_handler', 'custom_handler.py']
            for custom_bot_handler in custom_bot_handlers:
                expected_bot_path_and_name = ('path/to/custom_handler.py', 'custom_handler')
                bot_path_and_name = finder.resolve_bot_path(custom_bot_handler)
                self.assertEqual(bot_path_and_name, expected_bot_path_and_name)
