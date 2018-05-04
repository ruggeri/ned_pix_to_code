import numpy as np
import os
from PIL import Image
from typing import List

from . import config
from .compiler import mytoken
from .compiler import tokenizer

EMPTY_TOKEN = "EMPTY"
STOP_TOKEN = "STOP"

SPECIAL_TOKENS = [EMPTY_TOKEN, STOP_TOKEN]
ALL_TOKENS = SPECIAL_TOKENS + mytoken.Token.all()

TOKEN_TO_ID = {
  token: idx for idx, token in enumerate(ALL_TOKENS)
}
ID_TO_TOKEN = {
  idx: token for token, idx in TOKEN_TO_ID.items()
}
NUM_TOKENS = len(ALL_TOKENS)

def token_to_one_hot(token):
  token_idx = TOKEN_TO_ID[token]
  result = np.zeros(NUM_TOKENS, np.bool)
  result[token_idx] = True
  return result

def one_hot_to_token(one_hot):
  token_idx = np.argmax(one_hot)
  return ID_TO_TOKEN[token_idx]

def load_gui_datafile(fpath):
  tokens = tokenizer.tokenize_file(fpath)

  X = []
  y = []

  window = np.tile(
    token_to_one_hot(EMPTY_TOKEN),
    (config.TOKENS_WINDOW, 1)
  )

  for token in tokens:
    token_one_hot = token_to_one_hot(token)

    X.append(window)
    y.append(token_one_hot)

    window = np.roll(window, -1, axis = 0)
    window[config.TOKENS_WINDOW-1, :] = token_one_hot

  X, y = np.array(X), np.array(y)

  return (X, y)

def load_png_datafile(fpath):
  img = Image.open(fpath)
  img = img.resize((config.IMAGE_SIZE, config.IMAGE_SIZE), Image.BICUBIC)
  img_data = np.asarray(img)
  return img_data

def one_hot_window_to_tokens(window):
  tokens = []
  for one_hot in window:
    token = one_hot_to_token(one_hot)
    tokens.append(token)
  return tokens

def load_datafiles(data_dir_path, limit = None):
  datahashes = set()
  for fname in os.listdir(data_dir_path):
    if fname.endswith(".gui"):
      datahashes.add(fname.rsplit(".", 1)[0])
    elif fname.endswith(".png"):
      datahashes.add(fname.rsplit(".", 1)[0])
    else:
      print(f"Ignorning unrecognized file: {fname}")
  datahashes = list(datahashes)
  datahashes.sort()

  dataset = {}

  if limit is not None:
    print(f"Limiting dataset size to {limit}.")
    datahashes = datahashes[:limit]

  for datahash in datahashes:
    print(datahash)
    gui_filepath = os.path.join(data_dir_path, f"{datahash}.gui")
    png_filepath = os.path.join(data_dir_path, f"{datahash}.png")

    gui_X, y = load_gui_datafile(gui_filepath)
    png_X = load_png_datafile(png_filepath)

    dataset[datahash] = { "gui": gui_X, "png": png_X, "y": y }

  return dataset

def save_dataset(data_file_path, dataset):
  np.savez_compressed(data_file_path, dataset = dataset)

def load_compressed_dataset(data_file_path):
  npz_data = np.load(data_file_path)
  # We use `()` because we saved a single dict object.
  dataset = npz_data["dataset"][()]
  return dataset
