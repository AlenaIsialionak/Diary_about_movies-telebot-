# from aiogram import Bot, Dispatcher, types, executor
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import StatesGroup, State
# import functionals_for_databasa

# import asyncio

# from aiogram import Bot, Dispatcher, types
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import StatesGroup, State

# from aiogram import Bot, Dispatcher, types
# from aiogram.fsm.storage.memory import MemoryStorage


import asyncio
import logging
import sys
from os import getenv

# from aiogram import Bot, Dispatcher, html, types
# from aiogram.client.default import DefaultBotProperties
# from aiogram.enums import ParseMode
# from aiogram.filters import CommandStart
# from aiogram.types import Message
#
#
#
# # TOKEN = open("TOKEN.txt", 'r').read()
#
#
# with open("TOKEN.txt", 'r') as f:
#     TOKEN = f.read().strip()

# All handlers should be attached to the Router (or Dispatcher)

# dp = Dispatcher()



# @dp.message(CommandStart())
# async def command_start_handler(message: Message) -> None:
#     """
#     This handler receives messages with `/start` command
#     """
#     # Most event objects have aliases for API methods that can be called in events' context
#     # For example if you want to answer to incoming message you can use `message.answer(...)` alias
#     # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
#     # method automatically or call API method directly via
#     # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
#     await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
# @dp.message()
# async def echo_handler(message: Message) -> None:
#     try:
#         # Send a copy of the received message
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         # But not all the types is supported to be copied so need to handle it
#         await message.answer("Nice try!")


# @dp.message_handler(commands=["start"])
# async def command_start_handler(message: Message):
#     user_name = message.from_user.first_name
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     btn1 = types.InlineKeyboardButton("Add a new watched film", callback_data="add_film")
#     btn2 = types.InlineKeyboardButton("Get a list of the watched films", callback_data="get_watched_films")
#     markup.add(btn1, btn2)
#
#     await message.answer(f"Hello, {user_name}. \nHow can I help you?", reply_markup=markup)
#
#
# async def main() -> None:
#     # Initialize Bot instance with default bot properties which will be passed to all API calls
#     bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
#
#     # And the run events dispatching
#     await dp.start_polling(bot)
#
#
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())

# bot = Bot(TOKEN)
# storage = MemoryStorage()
# dp = Dispatcher(bot, storage=storage)
# GENRES = {}
#
# class StepForm(StatesGroup):
#     name_movie = State()
#     year_genre = State()
#     add_to_db = State()
#     genre = State()
#     like_dislike = State()
#     get_list_of_5 = State()
#     keywords = State()
#     sort_by_keywords = State()
#
#
# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     user_name = message.from_user.first_name
#     markup = types.InlineKeyboardMarkup(row_width=1)
#     btn1 = types.InlineKeyboardButton("Add a new watched film", callback_data="add_film")
#     btn2 = types.InlineKeyboardButton("Get a list of the watched films", callback_data="get_watched_films")
#     btn3 = types.InlineKeyboardButton("Get the ability to sort ", callback_data="sort")
#     markup.add(btn1, btn2, btn3)
#     await message.answer(f"Hello, {user_name}. \nHow can I help you?", reply_markup=markup)
#
#
# @dp.callback_query_handler()
# async def option_callback(callback: types.CallbackQuery):
#     if callback.data == "add_film":
#         await bot.send_message(callback.message.chat.id, "What movie do you want to add?")
#         await StepForm.name_movie.set()
#     if callback.data == "sort":
#         genres = functionals_for_databasa.get_genre_in_db(callback.message.chat.id)
#         markup1 = types.InlineKeyboardMarkup(row_width=1)
#         for genre in genres:
#             markup1.add(types.InlineKeyboardButton(f"{genre[0]}", callback_data=genre[0]))
#         await StepForm.genre.set()
#         await callback.message.answer("Please, choose the genre of the movies, what you wont to sort by", reply_markup=markup1)
#     if callback.data == "get_watched_films":
#         markup2 = types.InlineKeyboardMarkup(row_width=1)
#         btn1 = types.InlineKeyboardButton("5 recently watched movies", callback_data="5 recently")
#         btn2 = types.InlineKeyboardButton("5 the most liked movies", callback_data="5 the most likes")
#         btn3 = types.InlineKeyboardButton("find movies by keywords", callback_data="by_keywords")
#         markup2.add(btn1, btn2, btn3)
#         await callback.message.answer("what a list of movies do you want to get?", reply_markup=markup2)
#         await StepForm.get_list_of_5.set()
#
#
# @dp.callback_query_handler(state=StepForm.get_list_of_5)
# async def get_watched_films(callback: types.CallbackQuery, state: FSMContext):
#     user_id = callback.message.chat.id
#     match callback.data:
#         case "5 recently":
#             list_of_5 = functionals_for_databasa.get_list_of_5_movies(user_id)
#             recently_sp = "\n".join([mov[0] for mov in list_of_5])
#             await callback.message.answer(f'{recently_sp}')
#         case "5 the most likes":
#             list_of_5 = functionals_for_databasa.get_list_of_favorite_5_movies(user_id, 1)
#             favorite_sp = "\n".join([mov[0] for mov in list_of_5])
#             await callback.message.answer(f'{favorite_sp}')
#
#         case "by_keywords":
#             await bot.send_message(callback.message.chat.id, """please enter the words separated by a space\n"""
#                                                              """for which you want to find the movie""")
#             await StepForm.sort_by_keywords.set()
#
#
# @dp.message_handler(content_types=['text'], state=StepForm.sort_by_keywords)
# async def sort_film_by_keywords(message: types.Message, state: FSMContext):
#     keywords = message.text
#     list_keywords = keywords.split(' ')
#     list_of_movies = set()
#     for word in list_keywords:
#         movies = functionals_for_databasa.get_movie_by_keywords(word)
#         for movie in movies:
#             list_of_movies.add(movie[0])
#     res = '\n'.join([movie for movie in list_of_movies])
#     await message.answer(f"{res}")
#
#
#
#
# @dp.callback_query_handler(state=StepForm.genre)
# async def get_list_by_genre(callback: types.CallbackQuery, state: FSMContext):
#     genre = callback.data
#     res = functionals_for_databasa.sort_movie(genre, callback.message.chat.id)
#     await callback.message.answer(f"{res}")
#     await state.finish()
#
#
# @dp.message_handler(state=StepForm.name_movie)
# async def input_name(message: types.Message, state: FSMContext):
#     name = message.text
#     async with state.proxy() as data:
#         data['name_movie'] = name
#     markup1 = types.InlineKeyboardMarkup(row_width=2)
#     btn1 = types.InlineKeyboardButton("Yes", callback_data="yes")
#     btn2 = types.InlineKeyboardButton("No", callback_data="no")
#     markup1.add(btn1, btn2)
#     await message.answer(f'Do you want to add the release year and the genre of the movie?', reply_markup=markup1)
#
#
# @dp.callback_query_handler(state=StepForm.name_movie)
# async def add_information_about_film(callback: types.CallbackQuery, state: FSMContext):
#     if callback.data == "yes":
#         await bot.send_message(callback.message.chat.id, "What is the release year and genre of the movie?\n"
#                                                          "Please, enter the information separated by a space")
#         await StepForm.next()
#     if callback.data == "no":
#         data = await state.get_data()
#         name_movie, user_id = data.get("name_movie"), callback.message.chat.id
#         if functionals_for_databasa.add_movie_to_db(user_id, name_movie):
#                 await callback.message.answer(f"""The movie has been added""")
#
#
# @dp.message_handler(state=StepForm.year_genre)
# async def input_year(message: types.Message, state: FSMContext):
#     year_genre = message.text
#     try:
#         year_, genre = year_genre.split(" ")
#         year = int(year_)
#         if 2025 > year > 1800:
#             await StepForm.next()
#             await state.update_data(year=year, genre=genre)
#             data = await state.get_data()
#             inf = (data["name_movie"], str(data["year"]), data["genre"])
#             markup = types.InlineKeyboardMarkup(row_width=2)
#             btn1 = types.InlineKeyboardButton("Yes", callback_data="yes")
#             btn2 = types.InlineKeyboardButton("No", callback_data="no")
#             markup.add(btn1, btn2)
#             await message.answer(f"is this information about the film correct: {' '.join([a for a in inf])}",
#                                  reply_markup=markup)
#         else:
#             raise ValueError
#     except ValueError:
#         await bot.send_message(message.chat.id, "You entered the wrong values. Try to enter again")
#
#
# @dp.callback_query_handler(state=StepForm.add_to_db)
# async def user_check_inf(callback: types.CallbackQuery, state: FSMContext):
#     if callback.data == "yes":
#         data = await state.get_data()
#         name, year, genre = (data["name_movie"], data["year"], data["genre"])
#         id_movie = functionals_for_databasa.add_movie_to_db(callback.message.chat.id, name, year, genre)
#         if id_movie:
#             markup = types.InlineKeyboardMarkup(row_width=3)
#             btn1 = types.InlineKeyboardButton("yes", callback_data="yes")
#             btn2 = types.InlineKeyboardButton("no", callback_data="no")
#             btn3 = types.InlineKeyboardButton("neutral", callback_data="neutral")
#             markup.add(btn1, btn2, btn3)
#             await callback.message.answer(f"The movie has been added!\n"
#                                           f"Did you like this movie? {id_movie}", reply_markup=markup)
#             await state.finish()
#             await StepForm.like_dislike.set()
#             async with state.proxy() as data:
#                 data['id_movie'] = id_movie
#
#     if callback.data == "no":
#         await StepForm.year_genre.set()
#
#
# @dp.callback_query_handler(state=StepForm.like_dislike)
# async def callback_likes_dislikes(callback: types.CallbackQuery, state: FSMContext):
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     btn1 = types.InlineKeyboardButton("Yes", callback_data="yes")
#     btn2 = types.InlineKeyboardButton("No", callback_data="no")
#     markup.add(btn1, btn2)
#     data = await state.get_data()
#     id_movie = data.get("id_movie")
#     if callback.data == "yes":
#         if functionals_for_databasa.add_like_to_db(id_movie, 1):
#             await bot.send_message(callback.message.chat.id, f"Added like!\n"
#             f"Do you want to add keywords for a future movie search?", reply_markup=markup)
#
#     elif callback.data == "no":
#         if functionals_for_databasa.add_like_to_db(id_movie, -1):
#             await bot.send_message(callback.message.chat.id, "Added dislike\n"
#             f"Do you want to add keywords for a future movie search?", reply_markup=markup)
#     elif callback.data == "neutral":
#         if functionals_for_databasa.add_like_to_db(id_movie, 0):
#             await bot.send_message(callback.message.chat.id, f"Added\n"
#             f"Do you want to add keywords for a future movie search?", reply_markup=markup)
#     else:
#         await bot.send_message(callback.message.chat.id, "Sorry, something went wrong.")
#     await StepForm.keywords.set()
#
#
# @dp.callback_query_handler(state=StepForm.keywords)
# async def add_keywords(callback: types.CallbackQuery, state: FSMContext):
#     match callback.data:
#         case "yes":
#             await bot.send_message(callback.message.chat.id, "Please, enter the words separated by a space")
#         case "no":
#             await state.finish()
#
#
# @dp.message_handler(content_types=['text'], state=StepForm.keywords)
# async def get_words_from_user(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     id_movie = data.get("id_movie")
#     keywords = message.text
#     list_keywords = keywords.split(' ')
#     for word in list_keywords:
#         await message.answer(f'{word}')
#         id_keywords = functionals_for_databasa.check_add_word(word)
#         if id_keywords:
#             functionals_for_databasa.add_to_movies_keywords(id_movie, id_keywords)
#             await message.answer('ok')
#         await state.finish()
#

# if __name__ == "__main__":
#     executor.start_polling(dp)

# from aiogram import Bot, Dispatcher, types
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.fsm.state import State, StatesGroup

#


import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
import os
import uuid

from aiogram import Router
import traceback

import functionals_for_databasa

import logging
import sys
from os import getenv


with open("TOKEN.txt", 'r') as f:
    TOKEN = f.read().strip()

USER_PHOTO_DIR = "user_photos"
os.makedirs(USER_PHOTO_DIR, exist_ok=True)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()



@dp.message(CommandStart())
async def start_command(message: types.Message):
    logging.info(f"User {message.from_user.id} started the bot")
    await message.reply("Привет! Отправь мне изображение для обработки.")


@router.message(F.photo)
async def handle_photo(message: types.Message):
    try:
        user_id = message.from_user.id
        photo_id = message.photo[-1].file_id
        photo_file = await bot.get_file(photo_id)

        unique_filename = f"user_photo_{uuid.uuid4()}.jpg"
        photo_path = os.path.join(USER_PHOTO_DIR, unique_filename)

        if not os.path.exists(USER_PHOTO_DIR):
            os.makedirs(USER_PHOTO_DIR)

        await bot.download_file(photo_file.file_path, destination=photo_path)

        logging.info(f"Image saved for user {user_id} to {photo_path}")

        await message.reply("Изображение получено и сохранено!")

    except Exception as e:
        logging.error(f"Error processing photo from user {message.from_user.id}: {str(e)}")
        logging.error(traceback.format_exc())
        await message.reply("Извините, произошла ошибка при обработке вашего изображения.")


async def main():
    dp.include_router(router)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())




# class StepForm(StatesGroup):
#     name_movie = State()
#     genre = State()
#     get_list_of_5 = State()
#
# @dp.message(CommandStart())
# async def command_start_handler(message: Message, state: FSMContext):
#     user_name = message.from_user.first_name
#     names_button = ["Add a new watched film", "Get a list of the watched films" ]
#     cal_d = ["add_film", "get_watched_films" ]
#
#     builder = InlineKeyboardBuilder()
#
#     for index in range(2):
#         builder.button(text=names_button[index], callback_data=cal_d[index])
#
#     await message.answer(f"Hello, {user_name}. \nHow can I help you?", reply_markup=builder.as_markup())
#
#
# @dp.callback_query()
# async def option_callback(callback: types.CallbackQuery, state: FSMContext):
#     if callback.data == "add_film":
#         await bot.send_message(callback.message.chat.id, "What movie do you want to add?")
#         await state.set_state(StepForm.name_movie)
#
#     elif callback.data == "sort":
#         genres = functionals_for_databasa.get_genre_in_db(callback.message.chat.id)
#         builder = InlineKeyboardBuilder()
#         for genre in genres:
#             builder.button(text=f"{genre[0]}", callback_data=genre[0])
#
#         await state.set_state(StepForm.genre)
#         await callback.message.answer("Please, choose the genre of the movies, what you want to sort by", reply_markup=builder.as_markup())
#
#
#     elif callback.data == "get_watched_films":
#         names_button = ["5 recently watched movies", "5 the most liked movies", "find movies by keywords"]
#         cal_d = ["5 recently", "5 the most likes", "by_keywords"]
#
#         builder = InlineKeyboardBuilder()
#         for index in range(3):
#             builder.button(text=names_button[index], callback_data=cal_d[index])
#
#         await callback.message.answer("what a list of movies do you want to get?", reply_markup=builder.as_markup())
#         await state.set_state(StepForm.get_list_of_5)

# @dp.message(state=MyStates.WAITING_FOR_NAME)
# async def process_name(message: types.Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await message.reply("What is your age?")
#     await state.set_state(MyStates.WAITING_FOR_AGE)
#
#
# @dp.message(state=MyStates.WAITING_FOR_AGE)
# async def process_age(message: types.Message, state: FSMContext):
#     age = message.text
#     await state.update_data(age=age)
#     data = await state.get_data()
#     name = data["name"]
#     await state.clear()
#     await message.answer(f"Hello {name}, your age is {age}")



