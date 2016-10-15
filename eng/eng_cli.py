import sys
from eng.cli import cli
from eng.logging import info

def main():
  cli(sys.argv[1:])
  info("Done.")

