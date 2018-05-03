class Token:
  TOKEN_TYPES = []

  @classmethod
  def parse(clazz, str):
    for token_type in clazz.TOKEN_TYPES:
      token = token_type.parse(str)
      if token:
        return token
    raise f"Failed to parse token: ${str}"

  def is_block_command_operator(self):
    return False

  def is_text_command_operator(self):
    return False

  def is_text_command_separator_token(self):
    return False

  def is_block_start_token(self):
    return False

  def is_block_end_token(self):
    return False

class TextCommandOperatorToken(Token):
  TEXT_COMMAND_OPERATORS = {
    "big-title": None,
    "small-title": None,

    "btn-active": None,
    "btn-green": None,
    "btn-inactive": None,
    "btn-orange": None,
    "btn-red": None,

    "text": None,
  }

  @classmethod
  def parse(clazz, token_str):
    if token_str not in clazz.TEXT_COMMAND_OPERATORS:
      return None

    if clazz.TEXT_COMMAND_OPERATORS[token_str] is None:
      clazz.TEXT_COMMAND_OPERATORS[token_str] = clazz(token_str)

    return clazz.TEXT_COMMAND_OPERATORS[token_str]

  def __init__(self, text_command):
    self.text_command = text_command

  def is_text_command_operator(self):
    return True

Token.TOKEN_TYPES.append(TextCommandOperatorToken)

class BlockCommandOperatorToken(Token):
  BLOCK_COMMAND_OPERATORS = {
    "body": None,
    "header": None,
    "row": None,

    "single": None,
    "double": None,
    "quadruple": None,
  }

  @classmethod
  def parse(clazz, token_str):
    if token_str not in clazz.BLOCK_COMMAND_OPERATORS:
      return None

    if clazz.BLOCK_COMMAND_OPERATORS[token_str] is None:
      clazz.BLOCK_COMMAND_OPERATORS[token_str] = clazz(token_str)

    return clazz.BLOCK_COMMAND_OPERATORS[token_str]

  def __init__(self, block_command):
    self.block_command = block_command

  def is_block_command_operator(self):
    return True

  def __str__(self):
    return f"<token: {self.block_command}>"

Token.TOKEN_TYPES.append(BlockCommandOperatorToken)

class SymbolToken(Token):
  TOKEN = None
  SINGLETON = None

  @classmethod
  def parse(clazz, token_str):
    if not token_str == clazz.TOKEN:
      return None

    if clazz.SINGLETON is None:
      clazz.SINGLETON = clazz()

    return clazz.SINGLETON

class TextCommandSeparatorToken(SymbolToken):
  TOKEN = ","

  def is_text_command_separator_token(self):
    return True

Token.TOKEN_TYPES.append(TextCommandSeparatorToken)

class BlockStartToken(SymbolToken):
  TOKEN = "{"

  def is_block_start_token(self):
    return True

  def __str__(self):
    return "<token: {>"

Token.TOKEN_TYPES.append(BlockStartToken)

class BlockEndToken(SymbolToken):
  TOKEN = "}"

  def is_block_end_token(self):
    return True

  def __str__(self):
    return "<token: }>"

Token.TOKEN_TYPES.append(BlockEndToken)
