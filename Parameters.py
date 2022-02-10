class Parameters:

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def info(self):
        print("The parameters, and data-type are: ")
        for key,values in self.__dict__.items():
            print("{} = {}, {}\n".format(key, values, type(values)))