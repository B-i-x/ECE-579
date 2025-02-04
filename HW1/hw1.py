import os
from anytree import Node, RenderTree, findall
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

total_capacity = 10

def calculate_future_value(current_weight, remaining_items, current_value):
    remaining_capacity = total_capacity - current_weight
    if not remaining_items:
        return current_value
    max_avg_value = max((item.value / item.weight) for item in remaining_items)
    return remaining_capacity * max_avg_value + current_value

root = Node("Root", weight=0, value=0, future_value=calculate_future_value(0, items, 0))
best_value = 0
best_node = None

max_value = max(item.value for item in items)
# Function to determine node color based on value using a gradient from white to green
def get_node_color(value, is_overweight=False):
    if is_overweight:
        return "#ff0000"  # Return red if the weight limit is exceeded
    if max_value == 0:
        return "#FFFFFF"  # Return white if max_value is 0 to avoid division by zero
    green_intensity = int(255 * (value / max_value))  # Scale the value to 255
    return f"#{255-green_intensity:02x}ff{255-green_intensity:02x}"

def add_children(node, remaining_items):
    global best_value, best_node
    if not remaining_items:
        return
    
    current_item = remaining_items[0]
    new_remaining_items = remaining_items[1:]
    
    # Include current item if it fits
    if node.weight + current_item.weight <= total_capacity:
        included_path = f"{node.path}/{current_item.name}"
        included_node = Node(included_path, parent=node, 
                             weight=node.weight + current_item.weight, 
                             value=node.value + current_item.value, 
                             future_value=calculate_future_value(node.weight + current_item.weight, new_remaining_items, node.value + current_item.value),
                             path=included_path)
        add_children(included_node, new_remaining_items)

    # Exclude current item
    excluded_path = f"{node.path}"
    excluded_node = Node(excluded_path, parent=node, 
                         weight=node.weight, value=node.value, 
                         future_value=calculate_future_value(node.weight, new_remaining_items, node.value),
                         path=excluded_path)
    add_children(excluded_node, new_remaining_items)

# Build the decision tree
add_children(root, items)

# Print the tree and highlight the node with the highest value
for pre, fill, node in RenderTree(root):
    highlight = " <<< Best!" if node is best_node else ""
    print(f"{pre}{node.name} (Value: {node.value}, Weight: {node.weight}, Future Value: {node.future_value}){highlight}")

# Setup directory and export the tree to a DOT file
output_dir = os.path.join(os.getcwd(), "build")
os.makedirs(output_dir, exist_ok=True)
dot_path = os.path.join(output_dir, "hw1.dot")
DotExporter(root, nodeattrfunc=lambda node: f'style=filled, fillcolor="{get_node_color(node.future_value)}"').to_dotfile(dot_path)
print("DOT file created at:", dot_path)