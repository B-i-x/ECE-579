import os

from anytree import Node, RenderTree, PreOrderIter
from anytree.exporter import DotExporter
from collections import namedtuple

# Define the item structure using namedtuple for convenience
Item = namedtuple('Item', 'name value weight')
items = [
    Item('A', 14, 2),
    Item('B', 15, 3),
    Item('C', 18, 3),
    Item('D', 24, 4),
    Item('E', 28, 7)
]

max_value = sum(item.value for item in items)  # Sum of all item values

# Function to determine node color based on value using a gradient from white to green
def get_node_color(value):
    if max_value == 0:
        return "#FFFFFF"  # Return white if max_value is 0 to avoid division by zero
    green_intensity = int(255 * (value / max_value))  # Scale the value to 255
    return f"#{255-green_intensity:02x}ff{255-green_intensity:02x}"


# Function to create sub-nodes representing decision to include or exclude items
def add_children(node, item_index, current_value, current_weight, capacity):
    if item_index >= len(items) or current_weight == capacity:
        # No more items to process or capacity is fully utilized
        return

    item = items[item_index]
    next_index = item_index + 1

    # If we can add the item, we do it and recurse
    if current_weight + item.weight <= capacity:
        included = Node(f"Include {item.name}\nValue: {current_value + item.value}\nWeight: {current_weight + item.weight}\nU: {item.value}/{item.weight}",
                        parent=node,
                        value=current_value + item.value,
                        weight=current_weight + item.weight,
                        decision=f"Include {item.name}",
                        color=get_node_color(current_value))
        add_children(included, next_index, current_value + item.value, current_weight + item.weight, capacity)

    # We always have the option to exclude the item
    excluded = Node(f"Exclude {item.name} (Value: {current_value}, Weight: {current_weight})",
                    parent=node,
                    value=current_value,
                    weight=current_weight,
                    decision=f"Exclude {item.name}",
                    color=get_node_color(current_value))
    add_children(excluded, next_index, current_value, current_weight, capacity)

# Initialize the tree
root = Node("Root (Start, Value: 0, Weight: 0)", value=0, weight=0)
add_children(root, 0, 0, 0, 10)  # Start with the first item and zero value/weight

# Print the tree in a text format, including value-to-weight ratio where applicable
for pre, fill, node in RenderTree(root):
    ratio = node.value / node.weight if node.weight > 0 else 0
    print(f"{pre}{node.name} (Value/Weight Ratio: {ratio:.2f})")

output_dir = os.path.join(os.getcwd(), "build")
os.makedirs(output_dir, exist_ok=True)  # Ensures the directory exists
dot_path = os.path.join(output_dir, "hw1_bnb_tree.dot")

# Export to DOT file
DotExporter(root).to_dotfile(dot_path)
print("DOT file created at:", dot_path)