from re import findall
from json import dumps

def format_at_commands(commands, at):
    return map(lambda command: "echo %s | at %s" % (dumps(command), at), commands)

def format_email_output_commands(commands, email):
    return map(lambda command: "(%s) | mail -s 'at command output' %s" % 
            (command, email), commands)

def count_arguments(command):
    return len(findall(r"\{\d+\}", command))

def pair_arguments(items, amount):
    return zip(*[iter(items)]*amount)

def format_command(command, items):
    count = count_arguments(command)
    paired_arguments_list = pair_arguments(items, count)
    return map(lambda paired_args: command.format(*paired_args), paired_arguments_list)

def atmap(command, items, at, email=None):
    commands = format_command(command, items)
    if email:
        commands = format_email_output_commands(commands, email)
    return format_at_commands(commands, at)
