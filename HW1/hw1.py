import os
from anytree import Node, RenderTree, findall, PreOrderIter
from anytree.exporter import DotExporter
from collections import namedtuple



# Define the item structure using namedtuple for convenience
Item = namedtuple('Item', 'name value weight')
# items = [
#     Item('A', 14, 2),
#     Item('B', 15, 3),
#     Item('C', 18, 3),
#     Item('D', 24, 4),
#     Item('E', 28, 7)
# ]

items = [
    Item('A', 14, 2),
    Item('D', 24, 4),
    Item('C', 18, 3),
    Item('B', 15, 3),
    Item('E', 28, 7)
]

total_capacity = 10

# def sort_items_by_value_per_weight(items):
#     return sorted(items, key=lambda item: item.value / item.weight, reverse=True)

# items = sort_items_by_value_per_weight(items)
# print(items)
def calculate_future_value(node_value, node_weight, remaining_items):
    remaining_capacity = total_capacity - node_weight
    if not remaining_items:
        return f"{node_value}", node_value 
    max_avg_value = max((item.value / item.weight) for item in remaining_items)
    future_value = remaining_capacity * max_avg_value + node_value
    ev_string = f"{remaining_capacity}*{max_avg_value} + {node_value} = {future_value}"
    return (ev_string, future_value)

def find_max_value(root):
    """Finds and returns the node with the maximum future value that hasn't been searched."""
    max_node = max((node for node in PreOrderIter(root) if not node.searched),
                   key=lambda node: node.future_value, default=None)
    return max_node.future_value if max_node else None, max_node


root = Node("S", weight=0, value=0, future_value=0, remaining_items=items, searched=False)

best_node = root


addition_index = 0
def search_node(node, remaining_items):
    global best_node, addition_index
    if not remaining_items:
        return
    
    node.searched = True  # Mark the node as searched
    # print(remaining_items)
    current_item = remaining_items[0]
    new_remaining_items = remaining_items[1:]
    # print(new_remaining_items)
    if node.weight + current_item.weight <= total_capacity:
        addition_index += 1

        future_value_str_, ev_value = calculate_future_value(
                                node.value + current_item.value, 
                                node.weight + current_item.weight, 
                                new_remaining_items)
        
        include_name = f"i:{addition_index}\nADDING {current_item.name}\nVALUE: {node.value + current_item.value}\nWEIGHT: {node.weight + current_item.weight}\n{future_value_str_}\n"
        include_node = Node(include_name, parent=node, 
                            weight=node.weight + current_item.weight, 
                            value=node.value + current_item.value, 
                            future_value=ev_value,
                            remaining_items=new_remaining_items,
                            searched=False)
    
    addition_index += 1
    future_value_str_, ev_value = calculate_future_value(
                            node.value, 
                            node.weight, 
                            new_remaining_items)
    
    exclude_name = f"i:{addition_index}\nEXCLUDING {current_item.name}\nVALUE: {node.value}\nWEIGHT: {node.weight}\n{future_value_str_}"
    
    excluded_node = Node(exclude_name, parent=node, 
                         weight=node.weight, 
                         value=node.value, 
                         future_value=ev_value,
                        remaining_items=new_remaining_items,
                        searched=False)
    
    max_value, max_node = find_max_value(root)

    print(f"Best node: {max_node.name} with value: {max_value}")

    search_node(max_node, max_node.remaining_items)

    

# Build the decision tree
search_node(root, items)

# Print the tree and highlight the node with the highest value
for pre, fill, node in RenderTree(root):
    highlight = " <<< Best!" if node is best_node else ""
    # print(f"{pre}{node.name}")

# Setup directory and export the tree to a DOT file
output_dir = os.path.join(os.getcwd(), "build")
os.makedirs(output_dir, exist_ok=True)
dot_path = os.path.join(output_dir, "hw1v2.dot")

max_value = max(item.value for item in items)
# Function to determine node color based on value using a gradient from white to green
def get_node_color(value, is_overweight=False):
    if is_overweight:
        return "#ff0000"  # Return red if the weight limit is exceeded
    if max_value == 0:
        return "#FFFFFF"  # Return white if max_value is 0 to avoid division by zero
    green_intensity = int(255 * (value / max_value))  # Scale the value to 255
    return f"#{255-green_intensity:02x}ff{255-green_intensity:02x}"


# Export to DOT file
DotExporter(root, nodeattrfunc=lambda n: f'label="{n.name}" fillcolor="{get_node_color(n.value)}"').to_dotfile(dot_path)
