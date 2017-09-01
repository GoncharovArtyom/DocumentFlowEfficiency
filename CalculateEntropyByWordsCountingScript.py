import json as js
import WordCountDict
import Organization

result = []
errors = []
org = Organization.Organization.LoadFromJson("./CreateUnitsTree/organization.json")
units = org.GetAllUnits()
k = 1
for i in range(len(units)):
    if (units[i].Name == "<неизвестное подразделение>"):
        continue
    print(k, ") ", units[i].Name)
    k = k + 1
    docs = units[i].GetAllDocuments()
    dict = WordCountDict.WordCountDict.CreateDict(docs,True)
    dict.DeleteMistakes()
    try:
        entropy = dict.CalcEntropy()
        result.append((units[i].Name, entropy))
    except Exception:
        errors.append(units[i].Name)

result.sort(key=lambda x: x[1])
f = open("./entropy.json",'w')
js.dump(result,f,ensure_ascii=False)
f.close()


        