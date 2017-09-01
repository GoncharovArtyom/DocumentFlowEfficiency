class Employee(object):
    def __init__(self, firstName, lastName, id, documents = None):
        self.FirstName = firstName
        self.LastName = lastName
        self.Id = id
        if documents==None:
            self.Documents = []
        else:
            self.Documents=documents

    def AddDocument(self, doc):
        for i in range(len(self.Documents)):
            if (self.Documents[i] == doc):
                return
        self.Documents.append(doc)
        


