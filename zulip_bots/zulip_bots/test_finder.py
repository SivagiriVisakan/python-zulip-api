from zulip_bots import finder
import unittest
from unittest import TestCase
from typing import Text
from unittest import mock
from unittest.mock import patch


class FinderTestCase(TestCase):
    def setUp(self) -> None:
        self.original_current_dir = finder.current_dir
        finder.current_dir = 'api-repo/zulip_bots/zulip_bots'

    def test_resolve_bot_path_for_custom_bot(self) -> None:

        with patch('os.path.isfile', return_value=True), \
                patch('os.path.abspath', return_value='path/to/custom_handler.py'):

            custom_bot_handlers = ['custom_handler', 'custom_handler.py']
            for custom_bot_handler in custom_bot_handlers:
                expected_bot_path_and_name = ('path/to/custom_handler.py', 'custom_handler')
                bot_path_and_name = finder.resolve_bot_path(custom_bot_handler)
                self.assertEqual(bot_path_and_name, expected_bot_path_and_name)

    def test_resolve_bot_path_for_existing_bot(self) -> None:

        def abspath_side_effect(path: Text) -> Text:
            return 'absolute/path/to/'+path

        with patch('os.path.isfile', return_value=False), \
                patch('os.path.dirname'), \
                patch('os.path.abspath', side_effect=abspath_side_effect):

            expected_existing_bot_path_and_name = ('absolute/path/to/api-repo/zulip_bots/zulip_bots/bots/helloworld/helloworld.py',
                                                   'helloworld')
            existing_bot_path_and_name = finder.resolve_bot_path('helloworld')
            self.assertEqual(existing_bot_path_and_name, expected_existing_bot_path_and_name)

    def tearDown(self) -> None:
        finder.current_dir = self.original_current_dir
