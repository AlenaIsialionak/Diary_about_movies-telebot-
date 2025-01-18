import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch

df_summer = pd.read_excel('/content/summer for women.xlsx')



model = SentenceTransformer('my_model')

query_description = """I need a summer outfit for going out with friends. 
                        I don't like short skirt. It could be something with a long skirt or some kind of costume.
                    pip"""


try:
  corpus_embeddings = model.encode(df_summer['description'].tolist(), convert_to_tensor=True)
  query_embedding = model.encode(query_description, convert_to_tensor=True)
  cosine_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
except Exception as e:
  print(f"Ошибка кодирования: {e}")
  exit()


scores = {}
for i, score in enumerate(cosine_scores):
    scores[i + 1] = score
sorted_scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))


count = 0
for index in sorted_scores:
    try:
        row = df_summer[df_summer['index'] == index]
        image = row['images'].iloc[0]
        description = row['description'].iloc[0]
        print(f"Индекс: {index}, Сходство: {sorted_scores[index]:.4f}, Картинка: {image}, Описание: {description}")

        count += 1
        if count >= 3:  # Ограничение вывода на 3 строки
            break
    except (IndexError, KeyError):
        print(f"Ошибка при получении данных для индекса {index}. Проверьте данные.")
