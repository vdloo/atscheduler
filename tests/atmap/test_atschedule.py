from unittest import TestCase
from mock import patch, Mock
import collections

from atmap import atschedule, schedule_batches, create_batches, \
    create_at_generator, check_parameters


class TestCheckParameters(TestCase):
    def test_check_parameters_excepts_when_parallel_less_than_0(self):
        with self.assertRaises(RuntimeError):
            check_parameters(parallel=-1, interval=0)

    def test_check_parameters_excepts_when_interval_is_less_than_0(self):
        with self.assertRaises(RuntimeError):
            check_parameters(parallel=0, interval=-1)

    def test_check_parameters_excepts_when_parallel_is_positive_but_interval_is_0(self):
        with self.assertRaises(RuntimeError):
            check_parameters(parallel=1, interval=0)


class TestCreateAtGenerator(TestCase):
    def test_create_at_generator_creates_iterable(self):
        ret = create_at_generator('15:00 29 Sep 2015', 10)

        self.assertIsInstance(ret, collections.Iterable)

    def test_create_at_generator_generates_iterable_that_adds_interval_after_each_load(self):
        ret = create_at_generator('15:00 29 Sep 2015', 10)

        expected_result = [
            '15:00 29 Sep 2015',
            '15:10 29 Sep 2015',
            '15:20 29 Sep 2015',
            '15:30 29 Sep 2015',
            '15:40 29 Sep 2015',
        ]

        self.assertEqual(expected_result, list(map(lambda _: ret.next(), range(5))))


@patch('atmap.create_at_generator')
@patch('atmap.batch_items')
class TestCreateBatches(TestCase):

    command = "echo {0}"
    items = [1, 2, 3, 4]
    at = '15:00'
    parallel = 5
    interval = 10
    test_args = [command, items, at, parallel, interval]

    def test_create_batches_batches_items(self, batch_items, *args):
        create_batches(*self.test_args)

        batch_items.assert_called_once_with(self.command, self.items, self.parallel)

    def test_create_batches_creates_at_generator(self, _, create_at_generator):
        create_batches(*self.test_args)

        create_at_generator.assert_called_once_with(self.at, self.interval)

    def test_create_batches_return_tuple_of_batches_and_at_generator(self, batch_items, create_at_generator):
        ret = create_batches(*self.test_args)

        self.assertEqual(ret, (batch_items.return_value, create_at_generator.return_value))


class TestScheduleBatches(TestCase):

    command = 'echo {0} {1}'
    batches = [[[1, 2]], [[3, 4]], [[5, 6]], [[7, 8]], [[9, 10]]]
    at = (x for x in range(10))
    email = 'test@example.com'
    parallel = 2
    test_args = [command, batches, at, email, parallel]

    @patch('atmap.atmap')
    def test_schedule_batches_calls_atmap_for_each_batch(self, atmap):
        schedule_batches(*self.test_args)

        self.assertEqual(len(self.batches), len(atmap.mock_calls))

    def test_schedule_batches_schedules_batches(self):
        ret = schedule_batches(*self.test_args)

        expected_result = [
                'echo "echo 1 2 | mail -s \'at command output\' test@example.com" 2>&1 | at 5',
                'echo "echo 3 4 | mail -s \'at command output\' test@example.com" 2>&1 | at 6',
                'echo "echo 5 6 | mail -s \'at command output\' test@example.com" 2>&1 | at 7',
                'echo "echo 7 8 | mail -s \'at command output\' test@example.com" 2>&1 | at 8',
                'echo "echo 9 10 | mail -s \'at command output\' test@example.com" 2>&1 | at 9'
        ]
        self.assertEqual(map(lambda x: x, ret), expected_result)


@patch('atmap.schedule_batches')
@patch('atmap.create_batches', return_value=(Mock(), Mock()))
@patch('atmap.check_parameters')
class TestAtSchedule(TestCase):

    command = 'echo {0}'
    items = [1, 2, 3]
    at = '15:00'
    test_args = [command, items, at]

    def test_atschedule_checks_parameters(self, check_parameters, *args):
        atschedule(*self.test_args, parallel=5, interval=10)

        check_parameters.assert_called_once_with(parallel=5, interval=10)

    def test_atschedule_defaults_to_parallel_is_0(self, check_parameters, *args):
        atschedule(*self.test_args, interval=10)
        
        check_parameters.assert_called_once_with(parallel=0, interval=10)

    def test_atschedule_defaults_to_interval_is_0(self, check_parameters, *args):
        atschedule(*self.test_args, parallel=5)
        
        check_parameters.assert_called_once_with(parallel=5, interval=0)

    def test_atschedule_create_batches(self, _, create_batches, *args):
        atschedule(*self.test_args, parallel=5, interval=10)

        create_batches.assert_called_once_with('echo {0}', [1, 2, 3], '15:00', 5, 10)

    def test_atschedule_schedules_batches(self, _, create_batches, schedule_batches):
        atschedule(*self.test_args, email='test@example.com', parallel=5, interval=10)
        batches, at = create_batches.return_value

        schedule_batches.assert_called_once_with(
            self.command, batches, at, 'test@example.com', 5
        )

    def test_atschedule_returns_results_of_scheduled_batches(self, _1, _2, schedule_batches):
        ret = atschedule(*self.test_args, email='test@example.com', parallel=5, interval=10)

        self.assertEqual(ret, schedule_batches.return_value)
