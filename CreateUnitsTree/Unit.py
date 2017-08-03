class Unit(object):
    def __init__(self,name, id, parentId, employees, children):
        self.Name = name
        self.Id = id
        self.ParentId = parentId
        self.Children = children
        self.Employees = employees

    def AddChild(self, unit):
        self.Children.append(unit)


