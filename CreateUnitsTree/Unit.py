from AdditionalFunctions import *

class Unit(object):
    def __init__(self,name, id, parentId, employees, children):
        self.Name = name
        self.Id = id
        self.ParentId = parentId
        self.Children = children
        self.Employees = employees

    def AddChild(self, unit):
        self.Children.append(unit)

    def GetAllDocuments(self):
        documents = []
        q = []
        q.append(self)
        while (len(q) != 0):
            curUnit = q.pop(0)
            for i in range(len(curUnit.Employees)):
                documents = MergeListWithoutDuplication(documents, curUnit.Employees[i].Documents)
            for i in range(len(curUnit.Children)):
                q.append(curUnit.Children[i])
        return documents




