
# AVL Tree & BST Implementation in Python

An efficient, object-oriented implementation of an **AVL Tree** (Self-Balancing Binary Search Tree) alongside a standard **Binary Search Tree (BST)** mode, written in Python.

This project was developed with a strong focus on algorithmic efficiency, pointer manipulation, and dynamic balancing strategies.

---

## 🛠️ Key Features & Architecture

- **Automatic Rebalancing**: Dynamic recalculation of balance factors and heights with automatic single (LL, RR) and double (LR, RL) rotations.
- **Dual Mode Operation (`is_avl`)**: Configurable to run as either an auto-balancing AVL tree or a classic non-balancing Binary Search Tree.
- **Virtual Sentinel Nodes**: Uses virtual nodes (`real=False`) to streamline boundary condition checks and avoid null-pointer errors.
- **Iterative In-Order Traversal (`avl_to_list`)**: Efficiently exports sorted `(key, value)` pairs using an explicit stack to guarantee safety against recursion limits.
- **Node Successor Deletion**: Robust implementation for deleting nodes with up to 2 children by swapping with in-order successors.

---

## ⏱️ Complexity Analysis

| Operation  | AVL Tree   | Standard BST (Worst Case) | Space Complexity |
| **Search** | `O(log n)` | `O(n)` | `O(1)` |
| **Insert** | `O(log n)` | `O(n)` | `O(1)` |
| **Delete** | `O(log n)` | `O(n)` | `O(1)` |
| **Traversal (`avl_to_list`)** | `O(n)` | `O(n)` | `O(n)` |

---

## 💻 Usage Example

```python
from AVLTree import AVLTree

# Initialize an AVL Tree
tree = AVLTree(is_avl=True)

# Insert key-value pairs
tree.insert(10, "A")
tree.insert(20, "B")
tree.insert(30, "C")  # Triggers automatic rotation to balance

# Search for a node
node, search_time = tree.search(20)
if node:
    print(f"Found value: {node.value} (Search operations: {search_time})")

# Get sorted list of all key-value pairs
print("Sorted Elements:", tree.avl_to_list())
