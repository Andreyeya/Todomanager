import asyncio
import logging

import tortoise
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from config_reader import config
from database import init_db
from models import Task

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("📝 ToDo Manager - бот для управления задачами\n\n"
                         "Доступные команды:\n"
                         "/add [текст] - добавить задачу\n"
                         "/list - список задач\n"
                         "/done [ID] - отметить как выполненное\n"
                         "/delete [ID] - удалить задачу\n"
                         "/help - помощь")


@dp.message(Command("help"))
async def cmd_answer(message: types.Message):
    await message.answer("📝 ToDo Manager - бот для управления задачами\n\n"
                         "Доступные команды:\n"
                         "/add [текст] - добавить задачу\n"
                         "/list - список задач\n"
                         "/done [ID] - отметить как выполненное\n"
                         "/delete [ID] - удалить задачу\n"
                         "/help - помощь")


@dp.message(Command("add"))
async def cmd_add(message: types.Message):
    task_text = message.text[5:].strip()
    if not task_text:
        return await message.answer("❌ Укажите текст задачи после /add")

    task = await Task.create(
        user_id=message.from_user.id,
        text=str(task_text)
    )
    await message.answer(f'✅ Задача добавлена: "{task_text}" (ID: {task.id})')


@dp.message(Command("list"))
async def cmd_list(message: types.Message):
    tasks = await Task.filter(
        user_id=message.from_user.id
    ).order_by("is_completed", "-created_at")

    if not tasks:
        return await message.answer("📭 Список задач пуст")

    result = ["📝 Ваши задачи:"]
    for task in tasks:
        status = "✔️" if task.is_completed else "◻️"
        result.append(f"{status} {task.text} (ID: {task.id})")

    await message.answer("\n".join(result))


@dp.message(Command("done"))
async def cmd_done(message: types.Message):
    try:
        task_id = int(message.text[6:].strip())
    except ValueError:
        return await message.answer("❌ Укажите ID задачи после /done")

    task = await Task.filter(
        id=task_id,
        user_id=message.from_user.id
    ).first()

    if not task:
        return await message.answer("❌ Задача не найдена")

    task.is_completed = True
    await task.save()
    await message.answer(f'✔️ Задача "{task.text}" выполнена!')


@dp.message(Command("delete"))
async def cmd_delete(message: types.Message):
    try:
        task_id = int(message.text[8:].strip())
    except ValueError:
        return await message.answer("❌ Укажите ID задачи после /delete")

    task = await Task.filter(
        id=task_id,
        user_id=message.from_user.id
    ).first()

    if not task:
        return await message.answer("❌ Задача не найдена")

    await task.delete()
    await message.answer(f'🗑️ Задача "{task.text}" удалена!')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    tortoise.run_async(init_db())
    asyncio.run(main())
