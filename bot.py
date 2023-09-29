import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F, html
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.filters.command import Command, CommandObject
from config_reader import config
from datetime import datetime
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
#Объект бота
# Для записей с типом Secret* необходимо
# вызывать метод get_secret_value(),
# чтобы получить настоящее содержимое вместо '*******'
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
#Диспетчер
dp = Dispatcher()

#Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")
#Хэндлер на команду /test1
@dp.message(Command("test1"))
async def cmd_test1(message: types.Message):
    await message.answer("Test 1")

@dp.message(Command("test"))
async def cmd_test(message: types.Message):
    await message.answer("Hello, <i>world</i>!", parse_mode="HTML") #курсив для "world" для HTML
    await message.answer("Hello, *world*\!", parse_mode="MarkdownV2") #жирный шрифт для "world" для markdownV2

@dp.message(Command("answer"))
async def cmd_answer(message: types.Message):
    await message.answer("Это простой ответ")
@dp.message(Command("reply"))
async def cmd_reply(message: types.Message):
    await message.reply('Это ответ с ""ответом"')

@dp.message(Command("dice"))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")
@dp.message(Command("add_to_list"))
async def cmd_add_to_list(message: types.Message, mylist: list[int]):
    mylist.append(7)
    await message.answer("Добавлено число 7")

@dp.message(Command("show_list"))
async def cmd_show_list(message: types.Message, mylist: list[int]):
    await message.answer(f"Ваш список: {mylist}")

@dp.message(Command("name"))
async def cmd_name(message: types.Message, command: CommandObject): #тк используется встроенный фильтр Command, нужно добавить в хэндлер аргуемнт command c ипом
    if command.args: #с типом CommandObjetct
        await message.answer(f"Привет, {html.bold(html.quote(command.args))}!", parse_mode="HTML") #методы bold и quote для экранирования и форматирования
    else:
        await message.answer("Укажите, пожалуйста, свое имя после команды /name.")

#Сохранение форматирования
"""@dp.message(F.text)
async def echo_with_time(message: types.Message):
    # Получаем текущее время в часовом поясе ПК
    time_now = datetime.now().strftime('%H:%M')
    #Создаем подчеркнутый текст создания сообщения
    added_text = html.underline(f"Создано в {time_now}")
    # Отправляем полученное ботом сообщение с созданным временем
    await message.answer(f"{message.html_text}\n {added_text}", parse_mode="HTML")
"""

@dp.message(F.text)
async def extract_data(message: types.Message):
    data = {
        "url": "<N/A>",
        "email": "<N/A>",
        "code": "<N/A>"
    }
    entities = message.entities or []
    for item in entities:
        if item.type in data.keys():
            # Неправильно
            # data[item.type] = message.text[item.offset : item.offset+item.length]
            # Правильно
            data[item.type] = item.extract_from(message.text)

    await message.reply(
        "Вот что я нашёл:\n"
        f"URL: {html.quote(data['url'])}\n"
        f"E-mail: {html.quote(data['email'])}\n"
        f"Пароль: {html.quote(data['code'])}"
    )

#Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot, mylist = [1, 2, 3])

if __name__ == '__main__':
    asyncio.run(main())


