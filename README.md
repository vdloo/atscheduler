![License](https://img.shields.io/github/license/vdloo/atscheduler.svg)


atscheduler
===========

atscheduler is a simple command line tool that helps with generating [at](http://linux.die.net/man/1/at) jobs.

Examples
--------

Generating the commands to schedule executing ```echo "this is job 1"``` and 
```echo "This is job 2"``` on 20:00 today.
```bash
$ atscheduler --at 20:00 'echo "this is job {0}"' 1 2
echo "echo \"this is job 1\"" | at 20:00
echo "echo \"this is job 2\"" | at 20:00
```

A simple command with two arguments for two items
```bash
$ ./bin/atscheduler.py 'echo "this is job {0} {1}"' 1 2 3 4 --at "20:00"
echo "echo \"this is job 1 2\"" | at 20:00
echo "echo \"this is job 3 4\"" | at 20:00
```

STDIN is fine too
```bash
$ echo '1 2 3 4 5 6' | atscheduler --at "9:30 PM Tue" 'echo "this is job {2} {1} {0}"' - 
echo "echo \"this is job 3 2 1\"" | at 9:30 PM Tue
echo "echo \"this is job 6 5 4\"" | at 9:30 PM Tue
```

Send the output somewhere by redirecting it to mail
```bash
$ python bin/atscheduler --email example@example.com --at 20:00 'echo "this is job {0}"' 1 2
echo "(echo \"this is job 1\") | mail -s 'at command output' example@example.com" | at 20:00
echo "(echo \"this is job 2\") | mail -s 'at command output' example@example.com" | at 20:00
```

To actually schedule the job, simply pipe it to sh (but it's a good idea to always inspect the output first!)
```bash
$ atscheduler --at 20:00 "beep -f {0}" 400 500 600 | sh
```

Installation
------------
```bash
$ git clone git@github.com:vdloo/atscheduler.git && cd atscheduler
```

*Installation into a virtualenv*
```bash
$ mkvirtualenv atscheduler
$ pip install -e .  --upgrade
```

*System wide installation (not recommended)*
```bash
# python setup.py install --record installed_files.txt
```

To uninstall
```bash
# tr '\n' '\0' < installed_files.txt | xargs -0 rm -f --
```

Development
-----------
```bash
$ git clone git@github.com:vdloo/atscheduler.git && cd atscheduler
$ mkvirtualenv atscheduler
$ workon atscheduler
$ pip install -r requirements/development.txt 
```
