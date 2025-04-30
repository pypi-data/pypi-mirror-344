# import sys
# from pathlib import Path


# sys.path.insert(0, '/home/evinai/Desktop/ref_python_1224/1-packaging/ud-taking-python-next-level-0425')
# not recommended, but works for testing
# hardcoding the path to the package not recommended because it makes the code less portable
# and harder to maintain. It's better to use relative imports or package management tools like pip.
# alternatively
# path = Path(__file__).resolve()
# print(path.parent.parent.parent)
# sys.path.insert(0, str(path.parent.parent.parent)))
# # sys.path.insert(0, str(path.parent.parent))


# print(sys.path)
# from test_gpt_package.my_other_file import CONSTANT as CONSTANT2


CONSTANT = "hello"

# # This is a constant defined in the current file
# print(CONSTANT2)
# This is a constant imported from another file
