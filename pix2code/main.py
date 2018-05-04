import argparse
import sys

def main():
  parser = argparse.ArgumentParser(description = "pix2code")
  subparsers = parser.add_subparsers(dest = "subcommand", metavar = "subcommand")

  subcommands = {}

  from .subcommands import compile
  compile.configure_parser(
    subparsers.add_parser("compile", help = "compiles a .gui file")
  )
  subcommands["compile"] = compile.main

  from .subcommands import build_dataset
  build_dataset.configure_parser(
    subparsers.add_parser("build-dataset", help = "builds a compressed dataset")
  )
  subcommands["build-dataset"] = build_dataset.main

  # TODO: train
  subparsers.add_parser("train", help = "trains a model on a dataset")

  # TODO: predict
  subparsers.add_parser("predict", help = "generates gui code from an image")

  args = parser.parse_args()

  if args.subcommand == None:
    parser.print_help()
  else:
    subcommands[args.subcommand](args)
