import Unit
import Employee

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

def AddUnitsFromResolutionObj(obj, organization):
    tasksQ = []
    tasksQ.append(obj["Tasks"])
    while len(tasksQ) != 0:
        tasks = tasksQ.pop(0)
        for i in range(len(tasks)):
            executes = tasks[i]["Executes"]
            if (executes != None):
                emp = Employee.Employee(executes["FirstName"], executes["LastName"], executes["Id"])
                AddUnitAndParentsToOrganization(executes["Unit"], [emp], organization)
            appointed = tasks[i]["Appointed"]
            if (appointed != None):
                emp = Employee.Employee(appointed["FirstName"], appointed["LastName"], appointed["Id"])
                AddUnitAndParentsToOrganization(appointed["Unit"], [emp], organization)
            parts = tasks[i]["Parts"]
            if (parts != "None"):
                for j in range(len(parts)):
                    executors = parts[j]["Executors"]
                    if (executors != None):
                        for k in range(len(executors)):
                            executor = executors[k]["Executor"]
                            if (executor != None):
                                emp = Employee.Employee(executor["FirstName"], executor["LastName"], executor["Id"])
                                AddUnitAndParentsToOrganization(executor["Unit"],[emp], organization)
                            tasksQ.append(executors[k]["Tasks"])