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

def one_hot(idx):
  result = np.zeros(NUM_TOKENS)
  result[idx] = 1
  return result

def load_gui_datafile(fpath):
  tokens = tokenizer.tokenize_file(fpath)

  X = []
  y = []

  window = np.tile(
    one_hot(TOKEN_TO_ID[EMPTY_TOKEN]),
    (config.TOKENS_WINDOW, 1)
  )

  for token in tokens:
    token_idx = TOKEN_TO_ID[token]
    token_one_hot = one_hot(token_idx)

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
  for one_hot_token in window:
    token = ID_TO_TOKEN[np.argmax(one_hot_token)]
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

    dataset[datahash] = (gui_X, png_X, y)

  return dataset
