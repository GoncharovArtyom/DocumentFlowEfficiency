import json as js
import os

from CreateUnitsTree.Organization import Organization
from WordCountDict import WordCountDict
from Analyzer import dd_analyzer, analyzer

#Settings
ORG_FILE = "organization.json"
ENTROPY_FILE = "entropy_normalized.json"
PATH_TO_DATA = "./Data"

result = []
errors = []
org = Organization.LoadFromJson(os.path.join("./Files", ORG_FILE))
units = org.GetAllUnits()
k = 1
for i in range(len(units)):
    if (units[i].Name == "<неизвестное подразделение>"):
        continue
    print(k, ") ", units[i].Name)
    k = k + 1
    docs = units[i].GetAllDocuments()
    dict = WordCountDict.create_dict(docs, analyzer, True, path_to_data=PATH_TO_DATA)
    dict.delete_words_with_freq_lower_than(1)
    try:
        entropy = dict.calc_entropy()
        max_entropy = dict.max_entropy()
        result.append({"ent_divide_by_max_ent":entropy/max_entropy,
                       "entropy":entropy,
                       "max_entropy":max_entropy,
                       "num_docs":len(docs),
                       "num_words":dict.Total,
                       "num_distinct_words":dict.num_distinct_words,
                       "name": units[i].Name,
                       "id": units[i].Id})
    except Exception:
        errors.append(units[i].Name)

result.sort(key=lambda x: x["ent_divide_by_max_ent"])
f = open(os.path.join("./Files", ENTROPY_FILE),'w')
js.dump(result,f,ensure_ascii=False)
f.close()

with open(os.path.join("./Files", ENTROPY_FILE),'r') as f:
    result = js.load(f)
print(result)

        