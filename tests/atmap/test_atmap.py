from unittest import TestCase
from mock import patch

from atmap import atmap, format_command, pair_items, count_arguments, format_email_output_commands, format_at_commands

class TesFormatAtCommands(TestCase):
    commands = ['echo 1', 'echo "2"']

    def test_format_at_commands_formats_commands(self):
        ret = format_at_commands(self.commands, '15:00')

        expected_formatted_commands = [
                'echo "echo 1" | at 15:00',
                'echo "echo \\"2\\"" | at 15:00'
        ]

        self.assertEqual(ret, expected_formatted_commands)

class TestFormatEmailOutputCommands(TestCase):
    commands = ['echo 1', 'echo 2']

    def test_format_email_output_commands_formats_commands(self):
        ret = format_email_output_commands(self.commands, 'test@example.com')

        expected_formatted_commands = [
                "(echo 1) | mail -s 'at command output' test@example.com",
                "(echo 2) | mail -s 'at command output' test@example.com"
        ]

        self.assertEqual(ret, expected_formatted_commands)

class TestCountArguments(TestCase):
    def test_count_arguments_counts_arguments(self):
        ret1 = count_arguments('echo {0}')
        ret2 = count_arguments('echo {0} {1}')

        self.assertEqual(ret1, 1)
        self.assertEqual(ret2, 2)

class TestPairItems(TestCase):
    def test_pair_items_pairs_arguments(self):
        ret1 = pair_items([1, 2, 3, 4], 2)
        ret2 = pair_items([1, 2, 3, 4], 4)

        self.assertEqual(ret1, [(1, 2), (3, 4)])
        self.assertEqual(ret2, [(1, 2, 3, 4)])

class TestFormatCommand(TestCase):
    @patch('atmap.count_arguments')
    def test_format_command_counts_arguments(self, c_args):
        format_command('echo {1}', [1, 2, 3])

        c_args.assert_called_once_with('echo {1}')

    @patch('atmap.pair_items')
    def test_format_command_pairs_arguments(self, p_args):
        ret = format_command('echo {0} {1}', [1, 2, 3, 4])

        p_args.assert_called_once_with([1, 2, 3, 4], 2)

    def test_format_command_formats_command_in_right_order(self):
        ret = format_command('echo {3} {1} {2} {0}', [1, 2, 3, 4])
        
        self.assertEqual(ret, ['echo 4 2 3 1'])

    def test_format_command_with_pairs(self):
        ret = format_command('echo {0}', [1, 2, 3, 4])

        self.assertEqual(ret, ['echo 1', 'echo 2', 'echo 3', 'echo 4'])

@patch('atmap.format_at_commands')
@patch('atmap.format_email_output_commands')
@patch('atmap.format_command')
class TestAtMap(TestCase):
    command = "echo %%s"
    items = [1, 2, 3]

    def test_atmap_formats_command(self, f_command, *args):
        atmap(self.command, self.items, '15:00')

        f_command.assert_called_once_with(self.command, self.items)

    def test_atmap_formats_email_output_commands_if_email_is_specified(self, f_command, f_email, _):
        atmap(self.command, self.items, '15:00', 'test@example.com')

        f_email.assert_called_once_with(f_command.return_value, 'test@example.com')

    def test_atmap_does_not_format_email_output_commands_if_no_email_is_specified(self, f_command, f_email, _):
        atmap(self.command, self.items, '15:00')

        self.assertEqual(0, len(f_email.mock_calls))

    def test_atmap_formats_at_commands(self, f_command, _, f_at_command):
        ret = atmap(self.command, self.items, '15:00')

	f_at_command.assert_called_once_with(f_command.return_value, '15:00')
	self.assertEqual(ret, f_at_command.return_value)

    def test_atmap_formats_at_commands_using_formatted_email_commands_if_email_is_specified(self, _, f_email, f_at_command):
        ret = atmap(self.command, self.items, '15:00', 'test@example.com')

	f_at_command.assert_called_once_with(f_email.return_value, '15:00')
	self.assertEqual(ret, f_at_command.return_value)
