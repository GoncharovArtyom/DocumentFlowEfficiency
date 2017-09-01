import Unit
import Employee
import copy
import math

def AddUnitAndParentsToOrganization(unit, employees, organization):
    curUnitJson = unit
    curUnit = Unit.Unit(curUnitJson["Name"], curUnitJson["Id"], None, employees, [])
    while curUnitJson["Parent"] != None:
        prevUnitJson = curUnitJson
        curUnitJson = curUnitJson["Parent"]
        curUnit.ParentId = curUnitJson["Id"]
        newUnit = Unit.Unit(curUnitJson["Name"], curUnitJson["Id"],None, [], [])
        newUnit.AddChild(curUnit)
        curUnit = newUnit
    organization.AddChain(curUnit)
    return

def AddUnitsFromResolutionObj(obj, organization, doc):
    tasksQ = []
    tasksQ.append(obj["Tasks"])
    while len(tasksQ) != 0:
        tasks = tasksQ.pop(0)
        for i in range(len(tasks)):
            executes = tasks[i]["Executes"]
            if (executes != None):
                emp = Employee.Employee(executes["FirstName"], executes["LastName"], executes["Id"], [doc])
                AddUnitAndParentsToOrganization(executes["Unit"], [emp], organization)
            appointed = tasks[i]["Appointed"]
            if (appointed != None):
                emp = Employee.Employee(appointed["FirstName"], appointed["LastName"], appointed["Id"], [doc])
                AddUnitAndParentsToOrganization(appointed["Unit"], [emp], organization)
            parts = tasks[i]["Parts"]
            if (parts != "None"):
                for j in range(len(parts)):
                    executors = parts[j]["Executors"]
                    if (executors != None):
                        for k in range(len(executors)):
                            executor = executors[k]["Executor"]
                            if (executor != None):
                                emp = Employee.Employee(executor["FirstName"], executor["LastName"], executor["Id"], [doc])
                                AddUnitAndParentsToOrganization(executor["Unit"],[emp], organization)
                            tasksQ.append(executors[k]["Tasks"])

def BinarySearch(list, value):
    if (len(list) == 0):
        return (False, 0)
    left = 0
    right = len(list) - 1
    if (value == list[right]):
        return (True, right+1)
    if (value < list[left]):
        return (False, 0)
    pos = math.floor((left + right) / 2)
    while left!=pos:
        if (value < list[pos]):
            right = pos
        else:
            left = pos
        pos = math.floor((left + right) / 2)
    if (list[pos] == value):
        return (True, pos + 1)
    else:
        return (False, pos + 1)

def MergeListWithoutDuplication(list1, list2):
    result = copy.copy(list1)

    result.sort()
    for i in range(len(list2)):
        res = BinarySearch(result, list2[i])
        if (res[0] == False):
            result.insert(res[1],list2[i])

    return result