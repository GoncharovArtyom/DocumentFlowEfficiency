import json as js
import os
import logging
import pickle
import csv
import math

from CreateUnitsTree.Organization import Organization
from WordCountDict import WordCountDict
from Analyzer import dd_analyzer, analyzer

#Settings
ORG_FILE = "organization.json"
PATH_TO_DATA = "../Data"
SAVE_DIR = "../Files/TopicModeling"

# logging.basicConfig(level=logging.DEBUG, filename=os.path.join(SAVE_DIR, "logging_categories.txt"),
#                     filemode="w")
#
# result = []
# errors = []
# org = Organization.LoadFromJson(os.path.join("../Files", ORG_FILE))
# units = org.GetAllUnits()
# k = 1
# cat_set = set()
# for i in range(len(units)):
#     if (units[i].Name == "<неизвестное подразделение>"):
#         continue
#     print(k, ") ", units[i].Name)
#     k = k + 1
#     docs = units[i].GetAllDocuments()
#     for doc_name in docs:
#         with open(os.path.join(PATH_TO_DATA, doc_name, "document.json"),'r') as f:
#             doc_json = js.load(f)
#             for cat in doc_json["Categories"]:
#                 cat_set.add(cat['Name'])
#
# print(cat_set)
with open(os.path.join(SAVE_DIR,"categories.pkl"),'rb') as f:
    cat_set = pickle.load(f)

cat_list = list(cat_set)
org = Organization.LoadFromJson(os.path.join("../Files", ORG_FILE))
units = org.GetAllUnits()
k = 1

with open(os.path.join(SAVE_DIR, 'cat_entropy.csv'), 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Unit Id", "Unit name","Num docs", "Entropy"] + cat_list)

    for i in range(len(units)):
        if (units[i].Name == "<неизвестное подразделение>"):
            continue
        print(k, ") ", units[i].Name)
        k = k + 1
        docs = units[i].GetAllDocuments()

        unit_cat_dict = {}
        for cat in cat_list:
            unit_cat_dict[cat] = 0;

        Total = 0
        for doc_name in docs:
            with open(os.path.join(PATH_TO_DATA, doc_name, "document.json"),'r') as f:
                doc_json = js.load(f)
                for cat in doc_json["Categories"]:
                    unit_cat_dict[cat['Name']]+=1
                    Total += 1

        if Total>0:
            ent = 0
            for num in unit_cat_dict.values():
                if(num!=0):
                    ent += num/Total*math.log(num/Total)
            ent = -ent

            res_row = []
            for m in range(len(cat_list)):
                res_row.append(unit_cat_dict[cat_list[m]]/Total)

            csv_writer.writerow([units[i].Id, units[i].Name, Total, ent] + res_row)









