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
echo "echo \"this is job 1\"" 2>&1 | at 20:00 29 Sep 2015
echo "echo \"this is job 2\"" 2>&1 | at 20:00 29 Sep 2015
```

A simple command with two arguments for two items
```bash
$ ./bin/atscheduler.py 'echo "this is job {0} {1}"' 1 2 3 4 --at "20:00"
echo "echo \"this is job 1 2\"" 2>&1 | at 20:00 29 Sep 2015
echo "echo \"this is job 3 4\"" 2>&1 | at 20:00 29 Sep 2015
```

Run only a limited amount of jobs simultaneously and specify an interval in minutes
This example schedules batches of 2 at the same time with a delay of 5 minutes.
```bash 
$ ./bin/atscheduler --at '21:33' -j 2 -i 5 'echo {0}' 1 2 3 4
echo "echo 1" 2>&1 | at 21:33 29 Sep 2015
echo "echo 2" 2>&1 | at 21:33 29 Sep 2015
echo "echo 3" 2>&1 | at 21:38 29 Sep 2015
echo "echo 4" 2>&1 | at 21:38 29 Sep 2015
```

STDIN is fine too
```bash
$ echo '1 2 3 4 5 6' 2>&1 | atscheduler --at "9:30 PM Tue" 'echo "this is job {2} {1} {0}"' - 
echo "echo \"this is job 3 2 1\"" 2>&1 | at 21:30 29 Sep 2015
echo "echo \"this is job 6 5 4\"" 2>&1 | at 21:30 29 Sep 2015
```

Send the output somewhere by redirecting it to mail
```bash
$ python bin/atscheduler --email example@example.com --at 20:00 'echo "this is job {0}"' 1 2
echo "(echo \"this is job 1\") 2>&1 | mail -s 'at command output' example@example.com" 2>&1 | at 20:00 29 Sep 2015
echo "(echo \"this is job 2\") 2>&1 | mail -s 'at command output' example@example.com" 2>&1 | at 20:00 29 Sep 2015
```

To actually schedule the job, simply pipe it to sh (but it's a good idea to always inspect the output first!)
```bash
$ atscheduler --at 20:00 "beep -f {0}" 400 500 600 2>&1 | sh
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
# tr '\n' '\0' < installed_files.txt 2>&1 | xargs -0 rm -f --
```

Development
-----------
```bash
$ git clone git@github.com:vdloo/atscheduler.git && cd atscheduler
$ mkvirtualenv atscheduler
$ workon atscheduler
$ pip install -r requirements/development.txt 
```
