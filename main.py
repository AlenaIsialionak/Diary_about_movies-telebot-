from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import functionals_for_databasa

TOKEN = open("TOKEN.txt", 'r').read()



bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
GENRES = {}

class StepForm(StatesGroup):
    name_movie = State()
    year_genre = State()
    add_to_db = State()
    genre = State()
    like_dislike = State()
    get_list_of_5 = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_name = message.from_user.first_name
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("Add a new watched film", callback_data="add_film")
    btn2 = types.InlineKeyboardButton("Get a list of the watched films", callback_data="get_watched_films")
    btn3 = types.InlineKeyboardButton("Get the ability to sort ", callback_data="sort")
    markup.add(btn1, btn2, btn3)
    await message.answer(f"Hello, {user_name}. \nHow can I help you?", reply_markup=markup)


@dp.callback_query_handler()
async def option_callback(callback: types.CallbackQuery):
    if callback.data == "add_film":
        await bot.send_message(callback.message.chat.id, "What movie do you want to add?")
        await StepForm.name_movie.set()
    if callback.data == "sort":
        genres = functionals_for_databasa.get_genre_in_db(callback.message.chat.id)
        markup1 = types.InlineKeyboardMarkup(row_width=1)
        for genre in genres:
            markup1.add(types.InlineKeyboardButton(f"{genre[0]}", callback_data=genre[0]))
        await StepForm.genre.set()
        await callback.message.answer("Please, choose the genre of the movies, what you wont to sort by", reply_markup=markup1)
    if callback.data == "get_watched_films":
        markup2 = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("5 recently watched movies", callback_data="5 recently")
        btn2 = types.InlineKeyboardButton("5 the most liked movies", callback_data="5 the most likes")
        btn3 = types.InlineKeyboardButton("find movies by keywords", callback_data="by_keywords")
        markup2.add(btn1, btn2, btn3)
        await callback.message.answer("what a list of movies do you want to get?", reply_markup=markup2)
        await StepForm.get_list_of_5.set()


@dp.callback_query_handler(state=StepForm.get_list_of_5)
async def get_watched_films(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.message.chat.id
    match callback.data:
        case "5 recently":
            list_of_5 = functionals_for_databasa.get_list_of_5_movies(user_id)
            sp = "\n".join([mov[0] for mov in list_of_5])
            await callback.message.answer(f'{sp}')
        case "5 the most likes":

            pass
        case "by_keywords":
            pass


@dp.callback_query_handler(state=StepForm.genre)
async def get_list_by_genre(callback: types.CallbackQuery, state: FSMContext):
    genre = callback.data
    res = functionals_for_databasa.sort_movie(genre, callback.message.chat.id)
    await callback.message.answer(f"{res}")
    await state.finish()


@dp.message_handler(state=StepForm.name_movie)
async def input_name(message: types.Message, state: FSMContext):
    name = message.text
    async with state.proxy() as data:
        data['name_movie'] = name
    markup1 = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("Yes", callback_data="yes")
    btn2 = types.InlineKeyboardButton("No", callback_data="no")
    markup1.add(btn1, btn2)
    await message.answer(f'Do you want to add the release year and the genre of the movie?', reply_markup=markup1)

# @dp.callback_query_handler()
# async def get_top_5_list_of_movies(callback: types.CallbackQuery):


@dp.callback_query_handler(state=StepForm.name_movie)
async def add_information_about_film(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "yes":
        await bot.send_message(callback.message.chat.id, "What is the release year and genre of the movie?\n"
                                                         "Please, enter the information separated by a space")
        await StepForm.next()
    if callback.data == "no":
        data = await state.get_data()
        name_movie, user_id = data.get("name_movie"), callback.message.chat.id
        if functionals_for_databasa.add_movie_to_db(user_id, name_movie):
            await callback.message.answer(f'The movie has been added')



@dp.message_handler(state=StepForm.year_genre)
async def input_year(message: types.Message, state: FSMContext):
    year_genre = message.text
    try:
        year_, genre = year_genre.split(" ")
        year = int(year_)
        if 2025 > year > 1800:
            await StepForm.next()
            await state.update_data(year=year, genre=genre)
            data = await state.get_data()
            inf = (data["name_movie"], str(data["year"]), data["genre"])
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn1 = types.InlineKeyboardButton("Yes", callback_data="yes")
            btn2 = types.InlineKeyboardButton("No", callback_data="no")
            markup.add(btn1, btn2)
            await message.answer(f"is this information about the film correct: {' '.join([a for a in inf])}",
                                 reply_markup=markup)
        else:
            raise ValueError
    except ValueError:
        await bot.send_message(message.chat.id, "You entered the wrong values. Try to enter again")


@dp.callback_query_handler(state=StepForm.add_to_db)
async def user_check_inf(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "yes":
        data = await state.get_data()
        name, year, genre = (data["name_movie"], data["year"], data["genre"])
        id_movie = functionals_for_databasa.add_movie_to_db(callback.message.chat.id, name, year, genre)
        if id_movie:
            await callback.message.answer(f'The movie has been added')
            markup = types.InlineKeyboardMarkup(row_width=3)
            btn1 = types.InlineKeyboardButton("yes", callback_data="yes")
            btn2 = types.InlineKeyboardButton("no", callback_data="no")
            btn3 = types.InlineKeyboardButton("neutral", callback_data="neutral")
            markup.add(btn1, btn2, btn3)
            await callback.message.answer(f"The movie has been added!\n"
                                          f"Did you like this movie? {id_movie}", reply_markup=markup)
            await state.finish()
            await StepForm.like_dislike.set()
            async with state.proxy() as data:
                data['id_movie'] = id_movie

    if callback.data == "no":
        await StepForm.year_genre.set()


@dp.callback_query_handler(state=StepForm.like_dislike)
async def callback_likes_dislikes(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    id_movie = data.get("id_movie")
    if callback.data == "yes":
        if functionals_for_databasa.add_like_to_db(id_movie, 1):
            await bot.send_message(callback.message.chat.id, "Added like")

    elif callback.data == "no":
        if functionals_for_databasa.add_like_to_db(id_movie, -1):
            await bot.send_message(callback.message.chat.id, "Added dislike")
    elif callback.data == "neutral":
        if functionals_for_databasa.add_like_to_db(id_movie, 0):
            await bot.send_message(callback.message.chat.id, "Added")
    else:
        await bot.send_message(callback.message.chat.id, "Sorry, something went wrong.")
    await state.finish()







if __name__ == "__main__":
    executor.start_polling(dp)
