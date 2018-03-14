import csv
import json
import os

PATH_TO_DATA = "../Files"
ENTROPY_FILE = "dd_entropy_normalized.json"
NAME = "dd_entropy"

with open(os.path.join(PATH_TO_DATA,ENTROPY_FILE), 'r') as f:
    ent_obj = json.load(f)

with open(os.path.join(PATH_TO_DATA, NAME + '_csv.csv'), 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Нормализованная энтропия", "Энторопия", "Энтропия, посчитанная по "
                                                                  "закону Ципфа", "Максимальная "
                                                                                  "энтропия",
                         "Количество документов", "Количество слов","Количество уникальных слов",
                         "Имя подразделения", "Идентифифкатор подразделения"])
    for unit in ent_obj:
        csv_writer.writerow([unit["ent_divide_by_max_ent"],unit["entropy"],unit["zipf_entropy"],
                             unit["max_entropy"], unit["num_docs"], unit["num_words"],
                             unit["num_distinct_words"], unit["name"], unit["id"]])
    