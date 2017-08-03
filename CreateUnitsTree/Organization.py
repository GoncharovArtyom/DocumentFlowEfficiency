import json
import Unit
import Employee
import json as js
from MyEncoder import MyEncoder

class Organization(object):
    def __init__(self, root = None):
        if (root == None):
            self.root = Unit.Unit("root",None,None,[],[])
        else:
            self.root = root

    def __merge(self, targetUnit, unitToMerge):
        emp = unitToMerge.Employees[0]
        for i in range(len(targetUnit.Employees)):
            if (emp.Id == targetUnit.Employees[i].Id):
                return
        targetUnit.Employees.append(emp)
    
    @staticmethod
    def __from_json(jsonObject):
        if ('FirstName' in jsonObject):
            return Employee.Employee(jsonObject["FirstName"], jsonObject["LastName"], jsonObject["Id"])
        if ('ParentId' in jsonObject):
            return Unit.Unit(jsonObject["Name"],jsonObject["Id"], jsonObject["ParentId"], jsonObject["Employees"], jsonObject["Children"])
        if("root" in jsonObject):
            return Organization(jsonObject["root"])
    
    @staticmethod
    def LoadFromJson(path):
        f = open(path,'r')
        s = f.read()
        obj = json.loads(s,object_hook = Organization.__from_json )
        f.close()
        return obj
    
    def SaveToJson(self, path):
        f = open(path,'w')
        js.dump(self.__dict__,f,ensure_ascii=False, cls = MyEncoder)
        f.close()

    def AddChain(self, unit):
        curUnit = unit
        curRoot = self.root
        while True:
            b = False
            for i in range(len(curRoot.Children)):
                if (curRoot.Children[i].Id == curUnit.Id):
                    b = True
                    curRoot = curRoot.Children[i]
                    if (len(curUnit.Children) !=0):
                        curUnit = curUnit.Children[0]
                    else:
                        self.__merge(curRoot, curUnit)
                        return
                    break
            if (not b):
                curRoot.Children.append(curUnit)
                return

    def FindUnitById(self, id):
        q = []
        q.append(root)
        while (len(q)!=0):
            curUnit = q.pop(0)
            if (curUnit.Id == id):
                return curUnit  
            for i in range(len(curUnit.Children)):
                q.append(curUnit.Children[i])
        return None




