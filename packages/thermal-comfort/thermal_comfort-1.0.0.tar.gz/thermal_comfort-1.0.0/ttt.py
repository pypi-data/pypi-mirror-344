class C:
    class D:
        def __call__(self, *args, **kwds):
            print(f'I am {self.__class__.__name__}')

    class E:
        def __call__(self, *args, **kwds):
            print(f'I am {self.__class__.__name__}')

C.D()()
C.E()()