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
    return false

  def is_text_command_operator(self):
    return false

  def is_text_command_separator_token(self):
    return false

  def is_block_start_token(self):
    return false

  def is_block_end_token(self):
    return false

class TextCommandOperatorToken(Token):
  TEXT_COMMAND_OPERATORS = [
    "big-title",
    "small-title",

    "btn-active",
    "btn-green",
    "btn-inactive",
    "btn-orange",
    "btn-red",

    "text",
  ]

  @classmethod
  def parse(clazz, token_str):
    if token_str in clazz.TEXT_COMMAND_OPERATORS:
      return TextCommandOperatorToken(token_str)
    else:
      return None

  def __init__(self, text_command):
    self.text_command = text_command

  def is_text_command_operator(self):
    return true
Token.TOKEN_TYPES.append(TextCommandOperatorToken)

class BlockCommandOperatorToken(Token):
  BLOCK_COMMAND_OPERATORS = [
    "body",
    "header",
    "row",

    "single",
    "double",
    "quadruple",
  ]

  @classmethod
  def parse(clazz, token_str):
    if token_str in clazz.BLOCK_COMMAND_OPERATORS:
      return BlockCommandOperatorToken(token_str)
    else:
      return None

  def __init__(self, block_command):
    self.block_command = block_command

  def is_block_command_operator(self):
    return true
Token.TOKEN_TYPES.append(BlockCommandOperatorToken)

class SymbolToken(Token):
  @classmethod
  def parse(clazz, token_str):
    if token_str == clazz.TOKEN:
      return clazz()
    else:
      return None

class TextCommandSeparatorToken(SymbolToken):
  TOKEN = ","

  def is_text_command_separator_token(self):
    return true
Token.TOKEN_TYPES.append(TextCommandSeparatorToken)

class BlockStartToken(SymbolToken):
  TOKEN = "{"

  def is_block_command_start_token(self):
    return true
Token.TOKEN_TYPES.append(BlockStartToken)

class BlockEndToken(SymbolToken):
  TOKEN = "}"

  def is_block_command_end_token(self):
    return true
Token.TOKEN_TYPES.append(BlockEndToken)
