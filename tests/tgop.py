import getopt
import sys

args = '--a=def --b=124 --d -x ok'.split()
optlist, args = getopt.getopt(args, 'x:', [
    'a=', 'b=', 'd'])

print(optlist, args)
