

def f1():
    print('f1')
    return True


def f2():
    print('f2')
    return False


if f2() & f1():
    print(1)
