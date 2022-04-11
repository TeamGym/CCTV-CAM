import dill

class DillClass:
    def __init__(self, a, b, dillInnerClass):
        self.a = a
        self.b = b

        self.dillInnerClass = dillInnerClass

class DillInnerClass:
    def __init__(self):
        pass

dillInstance = DillClass(10, "s", DillInnerClass())

with open("test.class", "wb") as file:
    dill.dump(dillInstance, file)

with open("test.class", "rb") as file:
    instance = dill.load(file)
    
    print(instance)
    print(instance.a)
    print(instance.b)
    print(instance.dillInnerClass)
