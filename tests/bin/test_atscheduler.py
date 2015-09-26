from unittest import TestCase
from mock import patch

from bin.atscheduler import main

@patch('bin.atscheduler.atmap')
@patch('bin.atscheduler.get_args_from_stdin')
@patch('bin.atscheduler.get_args')
class TestAtscheduler(TestCase):
    def test_main_calls_atmap(self, get_args, _, atmap):
        args = get_args.return_value

        main()

        atmap.assert_called_once_with(args.command, args.items, args.at, args.email)

    def test_main_reads_from_stdin_if_stdin_marker_is_specified(self, get_args, get_from_stdin, atmap):
        args = get_args.return_value
        args.items = ['-']

        main()

        get_from_stdin.assert_called_once_with()
        atmap.assert_called_once_with(args.command, get_from_stdin.return_value, args.at, args.email)

