"""
The lightbot library provides interface to facilitate dealing with telegram-api in Python.
Just 'from lightbot import bot'.
"""

from ._lightbot import Core
from ._lightbot import InlineKeyboard, ReplyKeyboard
from ._text_handler import TextHandler
from ._callback_handler import CallbackHandler
from ._file_handler import FileHandler
from ._location_handler import LocationHandler

__version__ = "0.1.0"

__all__ = ["bot"]


bot = Core(
    text_handler=TextHandler(),
    location_handler=LocationHandler(),
    file_handler=FileHandler(),
    callback_handler=CallbackHandler(),
)
