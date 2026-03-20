from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.keyboards import main_keyboard

router = Router()


HELP_TEXT = (
    "Команды:\n"
    "/start - начать\n"
    "/help - помощь\n"
    "/subscribe - подписаться\n"
    "/unsubscribe - отписаться\n"
    "/settings - настройки\n"
    "/today - дневная сводка\n"
    "/top - вечерняя топ-сводка\n"
    "/status - статус подписки"
)


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    await message.answer("Добро пожаловать! Бот спортивных сводок готов.", reply_markup=main_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(HELP_TEXT)


@router.message(Command("subscribe"))
async def cmd_subscribe(message: Message) -> None:
    await message.answer("Вы подписаны на ежедневные сводки.")


@router.message(Command("unsubscribe"))
async def cmd_unsubscribe(message: Message) -> None:
    await message.answer("Вы отписаны от ежедневных сводок.")


@router.message(Command("settings"))
async def cmd_settings(message: Message) -> None:
    await message.answer("Настройки: timezone, sports, leagues, odds range, confidence threshold.")


@router.message(Command("today"))
async def cmd_today(message: Message) -> None:
    await message.answer("Запрос принят. Формирую дневную сводку.")


@router.message(Command("top"))
async def cmd_top(message: Message) -> None:
    await message.answer("Запрос принят. Формирую вечернюю топ-сводку.")


@router.message(Command("status"))
async def cmd_status(message: Message) -> None:
    await message.answer("Статус: активная подписка.")


@router.message(F.text)
async def fallback(message: Message) -> None:
    await message.answer("Используйте /help для списка доступных команд.")
