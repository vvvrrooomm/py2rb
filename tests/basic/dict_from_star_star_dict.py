input={"in_1": "foo"}


class WrappedDict():
  def __init__(self,param):
    self.dict=param
test = {**input}
print(f"test:")
[print(x) for x in test.keys()]
wrapped_dict = WrappedDict(input)
nested_test = {**wrapped_dict.dict}
print(f"nested_test:")
[print(x) for x in nested_test.keys()]