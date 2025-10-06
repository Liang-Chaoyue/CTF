code = compile('3+5', '<string>', 'eval')
eval(code)  # 输出：hello world


def dummy():
    pass
print(code)
dummy.__code__ = code
print(dummy.__doc__)
print(dummy())  # 输出：hello world