import sys
from eng.logging import info, error

from eng.generator import generate
from eng.scaffolder import new


invalid = "Invalid action."
valid_actions = {'generate': generate, 'new': new}


def cli(options):
    if not options:
        error(invalid)
        return

    action = options[0]

    for k in valid_actions:
        if action == k or action == k[0]:
            valid_actions[k](options[1:])
            return
    error(invalid)


def main():
    cli(sys.argv[1:])
    info("Done.")
