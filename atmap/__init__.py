from re import findall
from json import dumps
from dateutil import parser
from datetime import timedelta
from itertools import chain

def format_at_commands(commands, at):
    return map(lambda command: "echo %s | at %s" % (dumps(command), at), commands)

def format_email_output_commands(commands, email):
    return map(lambda command: "(%s) | mail -s 'at command output' %s" % 
            (command, email), commands)

def count_arguments(command):
    return len(findall(r"\{\d+\}", command))

def pair_items(items, amount):
    return zip(*[iter(items)]*amount)

def format_command(command, items):
    count = count_arguments(command)
    paired_arguments_list = pair_items(items, count)
    return map(lambda paired_args: command.format(*paired_args), paired_arguments_list)

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
            yield dt.strftime('%H:%M%p %d %b %Y')
            dt = dt + timedelta(minutes=interval)
    return at_generator(dt, interval)

def batch_items(items, amount=0):
    batches = pair_items(items, amount) if amount else [items]
    left = len(items) % amount if amount else 0
    if left:
        batches.append(items[-left:])
    return batches

def create_batches(items, at, parallel, interval):
    batches = batch_items(items, parallel)
    at_generator = create_at_generator(at, interval)
    return batches, at_generator

def schedule_batches(command, batches, at, email, parallel):
    return chain(*map(lambda sub_items: atmap(command, sub_items, at.next(), email=email), batches))

def atschedule(command, items, at, email=None, parallel=0, interval=0):
    check_parameters(parallel=parallel, interval=interval)
    batches, at = create_batches(items, at, parallel, interval)
    return schedule_batches(command, batches, at, email, parallel)
