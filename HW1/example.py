import os

from anytree import Node, RenderTree
from anytree.exporter import DotExporter

# Example: Creating a mini BnB tree
root = Node("root")
child1 = Node("Pick item A", parent=root)
child2 = Node("Don't pick item A", parent=root)
# …and so on.

# Text (ASCII) view
for pre, fill, node in RenderTree(root):
    print(f"{pre}{node.name}")

output_dir = os.path.join(os.getcwd(), "build")
os.makedirs(output_dir, exist_ok=True)  # Ensures the directory exists
dot_path = os.path.join(output_dir, "mini_bnb_tree.dot")

# Export to DOT file
DotExporter(root).to_dotfile(dot_path)
print("DOT file created at:", dot_path)
