import ast
code = """
import spaces
@spaces.GPU
def test():
    pass
"""
tree = ast.parse(code)
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Attribute) and decorator.value.id == "spaces" and decorator.attr == "GPU":
                print("Found @spaces.GPU")
