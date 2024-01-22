# BugCrowd
Solution to your "Which program should I hack in BugCrowd?".

```bash
$ python3 bugcrowd.py --help
usage: bugcrowd.py [-h] [-f] [-l] [-n] [-r] [-t TYPE] [-p PART] [-s SCOPE]

Solution to your "Which program should I hack in BugCrowd?".

options:
  -h, --help            show this help message and exit
  -f, --fresh           Generates a fresh program search and showcases recently added entries.
  -l, --latest          Display newly added Programs.
  -n, --name            Show only the Program name field.
  -r, --random          Select a random Program w/w.o. filters.
  -t TYPE, --type TYPE  Filter Programs based on Compensation Type (VDP, Bounty).
  -p PART, --part PART  Filter Programs based on Participation Status (Private/Public).
  -s SCOPE, --scope SCOPE
                        Filter Programs based on Scope rating (1-5).
```

```bash
kali@TheCaretaker:~$ python3 bugcrowd.py --type bounty --part public --scope 1 --random
Name            : Opsgenie
Program URL     : https://bugcrowd.com/Opsgenie
Min-Max Rewards : $200-$4000
```
