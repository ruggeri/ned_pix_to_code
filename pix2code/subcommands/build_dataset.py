import argparse

def configure_parser(build_dataset_parser):
  build_dataset_parser.add_argument(
    "--limit", type=int, help = "limits number of source files used to build dataset"
  )

  build_dataset_parser.add_argument(
    "data_dir_path", help = "path to directory of gui/png source files"
  )
  build_dataset_parser.add_argument(
    "outfile_path", help = "path to write compressed npz file out to"
  )

from .. import dataset

def main(args):
  d = dataset.load_datafiles(args.data_dir_path, limit = args.limit)
  dataset.save_dataset(args.outfile_path, d)
