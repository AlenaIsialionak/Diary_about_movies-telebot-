import logging

logging.basicConfig(level=logging.INFO)

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
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
from translation import get_translation

import functionals_for_databasa
from getting_outfit_model1 import process_model_output
import logging
import sys

import json




with open("TOKEN.txt", 'r') as f:
    TOKEN = f.read().strip()

USER_PHOTO_DIR = "user_photos"
os.makedirs(USER_PHOTO_DIR, exist_ok=True)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()


try:
    with open("translations.json", "r", encoding="utf-8") as f:
        translations = json.load(f)
except FileNotFoundError:
    logging.error("Error: translations.json file not found.")
    exit()
except json.JSONDecodeError as e:
    logging.error(f"Error decoding JSON: {e}")
    exit()
except Exception as e:
    logging.error(f"An unexpected error occurred: {e}")
    exit()

class StepForm(StatesGroup):
    language = State()
    second_step = State()
    outfit = State()
    text = State()
    gender = State()
    occasion = State()
    final_step = State()
    text = State()
    find_text = State()
    style = State()
    find_image = State()



def get_translation(language, key_path):
    keys = key_path.split('.')
    current_node = translations.get("messages", {}).get(language, {})
    for key in keys:
        if isinstance(current_node, dict) and key in current_node:
             current_node = current_node[key]
        else:
           return None
    return current_node


@dp.message(CommandStart())
async def start_command(message: types.Message, state: FSMContext):
    default_language = translations["settings"].get("default_language", "en")
    names_button = [get_translation(default_language, 'button_labels.set_english'),
                    get_translation(default_language, 'button_labels.set_russian')]
    cal_d = ["en", "ru"]

    if all(name is not None for name in names_button):
        builder = InlineKeyboardBuilder()
        for index in range(len(names_button)):
            if names_button[index] is not None:
                builder.button(text=names_button[index], callback_data=cal_d[index])

        greeting = get_translation(default_language, 'start_menu.select_language')
        await message.answer(greeting, reply_markup=builder.as_markup())
        await state.set_state(StepForm.language)


@dp.callback_query(StepForm.language)
async def option_callback_language(callback: types.CallbackQuery, state: FSMContext):
    user_language = callback.data
    if user_language not in ["en", "ru"]:
        await callback.message.answer("Invalid option")
        return

    await state.update_data(language=user_language)
    await state.set_state(StepForm.second_step) # Reset the language state
    greeting_message = get_translation(user_language, "start_menu.greeting")
    instruction = get_translation(user_language, "start_menu.instruction")

    names_button = [
        get_translation(user_language, "button_labels.making_outfit"),
        get_translation(user_language, "button_labels.getting_outfit"),
    ]
    cal_d = ["making_outfit", "getting_outfit"]

    if all(name is not None for name in names_button):
        builder = InlineKeyboardBuilder()
        for index in range(len(names_button)):
            if names_button[index] is not None:
                builder.button(text=names_button[index], callback_data=cal_d[index])
        await callback.message.answer(f"{greeting_message}\n{instruction}", reply_markup=builder.as_markup())
    else:
        await callback.message.answer("Error: Translations not found")


@dp.callback_query(StepForm.second_step)
async def option_callback(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_language = user_data.get('language', "en")
    logging.info("user_language: %s", user_language)

    if callback.data == "making_outfit":
        message_text = get_translation(user_language, "text_second_step.image_to_getting_outfit")
        await callback.message.answer(message_text)
        await state.set_state(StepForm.outfit)

    elif callback.data == "getting_outfit":
        message = get_translation(user_language, "text_second_step.text_gender")
        names_button = [
            get_translation(user_language, "button_labels.man"),
            get_translation(user_language, "button_labels.woman"),
        ]
        cal_d = ["man", "woman"]

        if all(name is not None for name in names_button):
            builder = InlineKeyboardBuilder()
            for index in range(len(names_button)):

                if names_button[index] is not None:
                    builder.button(text=names_button[index], callback_data=cal_d[index])
            await callback.message.answer(f"{message}", reply_markup=builder.as_markup())
            await state.set_state(StepForm.gender)

        else:
            await callback.message.answer("Error: Gender not found")


@dp.callback_query(StepForm.gender)
async def option_callback_gender(callback: types.CallbackQuery, state: FSMContext):
    logging.info("Callback data received: %s", callback.data)
    user_data = await state.get_data()
    user_language = user_data.get('language', "en")
    logging.info("user_language: %s", user_language)
    gender = callback.data
    await state.update_data(gender=gender)

    message = get_translation(user_language, "text_second_step.text_occasion")

    names_button = [
        get_translation(user_language, "button_labels.type_clothes.summer"),
        get_translation(user_language, "button_labels.type_clothes.party"),
        get_translation(user_language, "button_labels.type_clothes.casual"),
        get_translation(user_language, "button_labels.type_clothes.winter"),
    ]
    cal_d = ["summer", "party", "casual", "winter"]

    if all(name is not None for name in names_button):
        builder = InlineKeyboardBuilder()
        for index in range(len(names_button)):
            if names_button[index] is not None:
                builder.button(text=names_button[index], callback_data=cal_d[index])
        await callback.message.answer(f"{message}", reply_markup=builder.as_markup())
        await state.set_state(StepForm.style)
    else:
        await callback.message.answer("Error: Occasion not found")


@dp.callback_query(StepForm.style)
async def style(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(style=callback.data)
    user_data = await state.get_data()
    user_language = user_data.get('language', "en")
    message_text = get_translation(user_language, "text_second_step.text_to_outfit")
    await callback.message.answer(message_text)
    await state.set_state(StepForm.find_text)


@dp.message(StepForm.find_text)
async def process_text(message: Message, state: FSMContext):
    CHAT_ID = message.chat.id
    user_data = await state.get_data()
    user_language = user_data.get('language', "en")
    path_excel = f'excel_styles/{user_data.get("gender", "woman")}/{user_data.get("style", "casual")}.xlsx'
    text = message.text
    result_string = process_model_output(text, user_language, path_excel)
    logging.info(f"result_string: {result_string}")

    if isinstance(result_string, list):
        for item in result_string:
            if "error" in item:
                await message.answer(f"Ошибка: {item['error']}")
                continue

            image_name = item.get('image')
            description = item.get('description', "Нет описания")
            if image_name:
                image_path = f"images/{user_data.get('gender', 'woman')}/{user_data.get('style', 'casual')}/{image_name}"
            else:
                await message.answer("Не найдено имя файла изображения!")
                continue

            try:
                await message.answer(description)

                with open(image_path, 'rb') as photo:
                    photo_bytes = photo.read()
                await bot.send_photo(chat_id=CHAT_ID, photo=types.BufferedInputFile(photo_bytes, filename=image_name))
            except FileNotFoundError:
                await message.answer(f"Не найдено изображение по пути: {image_path}")
            except Exception as e:
                await message.answer(f"Ошибка при отправке сообщения: {e}")
    else:
        await message.answer("Не удалось обработать результаты или нет результатов.")

    await state.clear()



@dp.callback_query(StepForm.final_step)
async def final_step(callback: types.CallbackQuery, state: FSMContext):

    user_data = await state.get_data()
    user_language = user_data.get('language', 'en')
    gender = user_data.get('gender', 'man')
    occasion = user_data.get('occasion', 'casual')

    final_message = f"Language: {user_language}, Gender: {gender}, Occasion: {occasion}"
    await callback.message.answer(final_message)
    await state.set_state(None)


@router.message(F.photo, StepForm.outfit)
async def handle_photo(message: types.Message, bot:Bot, state: FSMContext):
    """
    Обрабатывает фотографии, сохраняет их в локальную папку и отправляет сообщение об успехе или ошибке.

    Args:
        message: Message объект от aiogram.
        bot: bot объект от aiogram
        state: FSMContext объект для управления состояниями.
    """
    try:
        user_id = message.from_user.id
        if not message.photo:
             await message.reply("Вы не отправили ни одной фотографии!")
             return
        if not os.path.exists(USER_PHOTO_DIR):
            os.makedirs(USER_PHOTO_DIR)

        photo = message.photo[-1] # Берем только последнюю (самую большую) фотографию
        photo_id = photo.file_id
        photo_file = await bot.get_file(photo_id)
        unique_filename = f"user_photo_{uuid.uuid4()}.jpg"
        photo_path = os.path.join(USER_PHOTO_DIR, unique_filename)
        await bot.download_file(photo_file.file_path, destination=photo_path)
        logging.info(f"Image saved for user {user_id} to {photo_path}")
        await message.reply(f"Изображение получено и сохранено!")


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



