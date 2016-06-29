from re import findall
from json import dumps
from dateutil import parser
from datetime import timedelta
from itertools import chain

def format_at_commands(commands, at):
    return map(lambda command: "echo %s 2>&1 | at %s" % (dumps(command), at), commands)

def format_email_output_commands(commands, email):
    return map(lambda command: "(%s) | mail -s 'at command output' %s" % 
            (command, email), commands)

def count_arguments(command):
    with_index = len(set(findall(r"\{\d+\}", command)))
    no_index = len(findall(r"\{\}", command))
    return with_index + no_index

def group_n_elements(elements, n=1):
    groups = map(list, zip(*[iter(elements)]*n))
    left = len(elements) % n if n else False
    if left:
        groups.append(elements[-left:])
    return groups

def group_items(command, items):
    count = count_arguments(command)
    return group_n_elements(items, count)

def format_command(command, items):
    try:
        return map(lambda grouped_args: command.format(*grouped_args), items)
    except IndexError:
        raise RuntimeError("Invalid amount of arguments for the command provided")

def atmap(command, items, at, email=None):
    commands = format_command(command, items)
    if email:
        commands = format_email_output_commands(commands, email)
    return format_at_commands(commands, at)

def check_parameters(*args, **kwargs):
    if kwargs['parallel'] < 0:
        raise RuntimeError("can't have a negative amount of parallel jobs!")
    if kwargs['interval'] < 0:
        raise RuntimeError("can't have a negative interval time!")
    if kwargs['parallel'] > 0 and kwargs['interval'] == 0:
        raise RuntimeError("a limited amount of workers requires an interval greater than 0!")

def create_at_generator(at, interval):
    dt = parser.parse(at)
    def at_generator(dt, interval):
        while True:
            yield dt.strftime('%H:%M %d %b %Y')
            dt = dt + timedelta(minutes=interval)
    return at_generator(dt, interval)

def batch_items(command, items, amount=0):
    argument_lists = group_items(command, items)
    batches = group_n_elements(argument_lists, amount) if amount else [argument_lists]
    return batches

def create_batches(command, items, at, parallel, interval):
    batches = batch_items(command, items, parallel)
    at_generator = create_at_generator(at, interval)
    return batches, at_generator

def schedule_batches(command, batches, at, email, parallel):
    return chain(*map(lambda batch: atmap(command, batch, at.next(), email=email), batches))

def atschedule(command, items, at, email=None, parallel=0, interval=0):
    check_parameters(parallel=parallel, interval=interval)
    batches, at = create_batches(command, items, at, parallel, interval)
    return schedule_batches(command, batches, at, email, parallel)
