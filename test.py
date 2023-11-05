class Tricky():
    def __init__(self,val) -> None:
        self.val = val
    
    def __str__(self) -> str:
        return self.val
    
    def __call__(self, val):
        return val

obj = Tricky(' b1')


if __name__ == "__main__":
    print(obj)     # prints 1
    print(obj(5))  # prints 5
