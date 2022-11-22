
class A:
    def __eq__(self,other):
        if type(self) != type(other):
            return False
        return self.name == other.name

    
a=A()

