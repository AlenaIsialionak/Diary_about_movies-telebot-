import torch
from sentence_transformers import SentenceTransformer
from transformers import MarianMTModel, MarianTokenizer

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import re
import string
from nltk.corpus import stopwords
import nltk
from typing import List

import logging

logging.basicConfig(level=logging.INFO)

try:
    nltk.data.find('corpora/stopwords')
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))


def load_or_train_models():

    """
    Loads or trains models and the tokenizer.
    Returns a tuple (model_1, model_2, tokenizer)
    Returns None if the models could not be loaded or trained.
    """
    model_path_1 = 'my_model_sentence.pt'
    model_path_translate = 'my_model_translate.pt'
    model_path_translate_ru_en = 'my_model_translate_ru_en.pt'
    tokenizer_path = 'tokenizer'
    tokenizer_path_en_ru = 'tokenizer_en_ru'

    model_1 = None
    model_2 = None
    model_3 = None
    tokenizer = None
    tokenizer_2 = None

    try:

        try:
           model_1 = torch.load(model_path_1)

        except FileNotFoundError:

            model_1 = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            torch.save(model_1, model_path_1)

        try:
            model_2 = torch.load(model_path_translate)

        except FileNotFoundError:
            model_2 = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-ru-en")
            torch.save(model_2, model_path_translate)
        try:
            model_3 = torch.load(model_path_translate_ru_en)
        except FileNotFoundError:
            model_3 = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-en-ru")
            torch.save(model_3, model_path_translate_ru_en)
        try:
           tokenizer = torch.load(tokenizer_path)
        except FileNotFoundError:
            tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ru-en")
            torch.save(tokenizer, tokenizer_path)

        try:
           tokenizer_2 = torch.load(tokenizer_path_en_ru)
        except FileNotFoundError:
            tokenizer_2 = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-ru")
            torch.save(tokenizer_2, tokenizer_path_en_ru)

        return model_1, model_2, model_3, tokenizer, tokenizer_2
    except Exception as e:
        return None, None, None


def translate_ru_to_en(text: str, tokenizer, model_2) -> str:

  """
  Translates a given Russian text into English.

  :param text: Russian text to translate.
  :return: translated text in English.
  """
  logging.info(f"translate_ru_to_en")

  input_ids  = tokenizer.encode(text, return_tensors="pt")
  outputs = model_2.generate(input_ids)
  decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

  return str(decoded)


def translate_en_to_ru(text: str, tokenizer_2, model_3) -> str:

  """
  Translates a given English text into Russian.

  :param text: English text to translate.
  :return: translated text in Russian.
  """
  logging.info(f"translate_en_to_ru")

  input_ids  = tokenizer_2.encode(text, return_tensors="pt")
  outputs = model_3.generate(input_ids)
  decoded = tokenizer_2.decode(outputs[0], skip_special_tokens=True)

  return str(decoded)

def clean_text(text:str, remove_stop_words: bool=False) -> str:

  """
  Cleans the input text by converting it to lowercase, removing unnecessary spaces,
  punctuation marks, and optionally removing stop words.

  :param text: the text to be cleaned.
  :param remove_stop_words: a boolean indicating whether to remove stop words.
  :return: the cleaned text.
  """
  logging.info(f"clean_text")
  try:
      if not isinstance(text, str):
          raise ValueError("Аргумент 'text' должен быть строкой.")

      logging.info(f"clean_text(text='{text}', remove_stop_words={remove_stop_words})")

      text = text.lower()
      text = re.sub('\s+', ' ', text).strip()
      text = text.translate(str.maketrans('', '', string.punctuation))

      text = re.sub(r"won't", "will not", text)
      text = re.sub(r"can't", "cannot", text)

      if remove_stop_words:
          text_words = text.split()
          text_words = [word for word in text_words if word not in stop_words]
          text = ' '.join(text_words)

      logging.info(f"clean_text результат = '{text}'")
      return text
  except Exception as e:
      logging.error(f"Ошибка при очистке текста: {e}")
      return text

def prepare_text(texts: List[str], model_2, remove_stop_words: bool=False, ) -> np.ndarray:

   """
   Prepare text for the model by cleaning and encoding it into embeddings.

  :param texts: a list of texts to prepare.
  :param remove_stop_words: a boolean indicating whether to remove stop words.
  :return: an array of embeddings corresponding to the cleaned texts.
   """
   logging.info(f"prepare_text")
   cleaned_texts = [clean_text(text, remove_stop_words=remove_stop_words) for text in texts]

   embeddings = model_2.encode(cleaned_texts)

   return embeddings


def find_relevant_outfits(model_1, user_query:str, embeddings:np.ndarray, outfit_ids:list, top_n:int=1 ) -> List:

  """
  Search for relevant outfits based on the user's query and
  return the top matching outfits.

  :param user_query: the query from user for which relevant outfits are to be found.
  :param embeddings: the embeddings of all texts from the dataset.
  :param outfit_ids: list of identifiers or names corresponding to each outfit.
  :param top_n: the number of top matching outfits to return (default is 1).
  :return: the list of tuples containing the outfit IDs and their corresponding similarity scores.

  """
  logging.info(f"find_relevant_outfits")
  cleaned_query = clean_text(user_query, remove_stop_words=False)
  query_embedding = model_1.encode([cleaned_query])

  cosine_sim = cosine_similarity(query_embedding, embeddings)
  similarity_scores = cosine_sim[0]

  ranked_indices = np.argsort(similarity_scores)[::-1]

  relevant_outfits = []

  for i in ranked_indices[:top_n]:
    relevant_outfits.append((outfit_ids[i], similarity_scores[i]))


  return relevant_outfits


def process_model_output(user_query, user_language, path):
    """
    Обрабатывает пользовательский запрос, ищет подходящие наряды и возвращает список словарей с результатами.

    Args:
        user_query (str): Запрос пользователя.
        user_language (str): Язык пользователя ('ru' или 'en').
        path (str): Путь к Excel-файлу с данными о нарядах.

    Returns:
        list: Список словарей с информацией о нарядах.
               Каждый словарь содержит ключи 'image', 'description', 'score'.
               Возвращает None при ошибках.
    """
    try:
        model_1, model_2, model_3, tokenizer, tokenizer_2= load_or_train_models()
        if not model_1 or not model_2 or not model_3 or not tokenizer or not tokenizer_2:
            print("Ошибка при загрузке моделей")
            return None
        df_outfits = pd.read_excel(path)
        outfit_ids = df_outfits["images"].to_list()
        descriptions = df_outfits["description"].to_list()

        if user_language == 'ru':
            user_query = translate_ru_to_en(user_query, tokenizer, model_2)

        embeddings_description = prepare_text(descriptions, model_1, remove_stop_words=True)
        relevant_outfits = find_relevant_outfits(model_1, user_query, embeddings_description, outfit_ids)
        outfit_id_to_index = {outfit_id: index for index, outfit_id in enumerate(outfit_ids)}
        results = []

        for outfit_id, score in relevant_outfits:
            index = outfit_id_to_index.get(outfit_id)
            if index is None:
                continue
            if user_language == 'ru':
                description = translate_ru_to_en(descriptions[index], tokenizer_2, model_3)
            else:
                description = descriptions[index]

            results.append({'image': outfit_id, 'description': description, 'score': score}) #добавляем результат в список

        return results
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден по пути '{path}'")
        return None
    except KeyError as e:
        print(f"Ошибка: Проверьте excel файл! Колонка '{e}' не найдена.")
        return None
    except Exception as e:
        print(f"Произошла общая ошибка: {e}")
        return None

