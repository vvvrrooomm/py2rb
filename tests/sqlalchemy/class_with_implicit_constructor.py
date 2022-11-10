db=None

class Organizers(db.Model):
    foo = []
    bar = {}

    @staticmethod
    def show_method(a):
        print(a)
    @staticmethod
    def make():
        r = Organizers(
            foo=[1,2],
            bar={'a':4,'b':5},
        )
        return r

r = Organizers(
    foo=[1,2],
    bar={'a':4,'b':5},
)