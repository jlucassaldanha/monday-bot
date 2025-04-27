def doc(docstring):
    def document(func):
        func.__doc__ = docstring
        return func

    return document

@doc("this command accepts these values: {values}".format(values=[1, 2, 3]))
def do_this(self, arg):
    pass

print(do_this.__doc__)