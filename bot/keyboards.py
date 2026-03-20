from __future__ import annotations

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/today"), KeyboardButton(text="/top")],
            [KeyboardButton(text="/subscribe"), KeyboardButton(text="/unsubscribe")],
            [KeyboardButton(text="/settings"), KeyboardButton(text="/status")],
        ],
        resize_keyboard=True,
    )
