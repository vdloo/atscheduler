from unittest import TestCase
from mock import patch

from bin.atscheduler import main

@patch('bin.atscheduler.atschedule')
@patch('bin.atscheduler.get_args_from_stdin')
@patch('bin.atscheduler.get_args')
class TestAtscheduler(TestCase):
    def test_main_calls_atschedule(self, get_args, _, atschedule):
        args = get_args.return_value

        main()

        atschedule.assert_called_once_with(args.command, args.items, args.at, args.email, parallel=args.j, interval=args.i)

    def test_main_reads_from_stdin_if_stdin_marker_is_specified(self, get_args, get_from_stdin, atschedule):
        args = get_args.return_value
        args.items = ['-']

        main()

        get_from_stdin.assert_called_once_with()
        atschedule.assert_called_once_with(args.command, get_from_stdin.return_value, args.at, args.email, parallel=args.j, interval=args.i)

