import argparse
import sys

from .subcommands import compile

def main():
  parser = argparse.ArgumentParser(description = "pix2code")
  subparsers = parser.add_subparsers(dest = "command_name")

  compile.configure_parser(subparsers.add_parser("compile"))

  args = parser.parse_args()

  if args.command_name == "compile":
    compile.main(args)
