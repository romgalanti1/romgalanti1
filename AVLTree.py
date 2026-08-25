
"""A class representing a node in an AVL tree"""


class AVLNode(object):
    """
    @type key: int
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """

    def __init__(self, key, value, is_real=True):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1
        self.real=is_real

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def is_real_node(self):
        return self.real
    
    def update_height(self):
        if not self.real:
            self.height = -1
            return
        self.height = max(self.right.height, self.left.height) + 1

    def get_balance_factor(self):
        if not self.real:
            return 0
        return self.left.height - self.right.height

"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
    @type is_avl: boolean
    @param is_avl: If True then tree is AVL, otherwise it is just a "regular" binary search tree, without rotations.
    """

    def __init__(self, is_avl):
        self.root = None
        self.is_avl = is_avl
        self.virtual_node=AVLNode(None,None,False)
        self.tree_size=0

    """searches for a node in the dictionary corresponding to the key (starting at the root)

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x, search_time) where x is the node corresponding to key (or None if not found)
    and search_time is the search time, as defined and explained in the assignment.
    """

    def search(self, key):
        if self.root is None:
            return None,1
        search_time = 0
        node=self.root
        while node.real:
            search_time+=1
            if node.key == key:
                return node, search_time
            elif key < node.key:
                node = node.left
            else:
                node=node.right

        return None, search_time+1

    """inserts a new node into the dictionary with corresponding key and value (starting at the root)

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int,int)
    @returns: a 4-tuple (x, search_time, rotations, height_changes), where x is the new node
    and the other 3 return values are as defined and explained in the assignment.
    """

    def insert(self, key, val):
        node=AVLNode(key,val)
        node.right=self.virtual_node
        node.left=self.virtual_node
        node.update_height()
        if self.root is None:
            self.root=node
            self.tree_size=1
            return node,1,0,0
        curr=self.root
        search_time=1
        while (curr.real):
            search_time+=1
            prev=curr
            if key>curr.key:
                curr=curr.right
            else:
                curr=curr.left
        node.parent=prev
        if key>prev.key:
            prev.right=node
        else:
            prev.left=node
        self.tree_size+=1
        if not self.is_avl:
            return node,search_time,0,0
        else:
            rotations,height_changes=self.AVL_balance(node.parent)
        return node, search_time, rotations, height_changes


    def AVL_balance(self,node,insert=True):
        curr=node
        rotations=0
        height_changes=0
        while curr is not None:
            old_height=curr.height
            curr.update_height()
            bf=curr.get_balance_factor()
            if abs(bf)<2 and curr.height==old_height:
                break
            elif abs(bf)<2:
                curr=curr.parent
                height_changes+=1
            else:
                parent=curr.parent
                rotations+=self.rotation(curr)
                if(insert):
                    break
                else:
                    curr=parent

        return rotations,height_changes         


    def rotation(self,node):
        BF=node.get_balance_factor()
        if (BF==-2):
            R_BF=node.right.get_balance_factor()
            if(R_BF<=0):
                return self.rotation_L_L(node)
            else:
                return self.rotation_R_L(node)
        elif(BF==2):
            L_BF=node.left.get_balance_factor()
            if(L_BF>=0):
                return self.rotation_R_R(node)
            else:
                return self.rotation_L_R(node)
        return 0

    def rotate_left(self,node):
        parent=node.parent
        node_right=node.right
        right_left=node_right.left

        node_right.parent=parent
        if(parent is None):
            self.root=node_right
        elif(parent.right==node):
            parent.right=node_right
        else:
            parent.left=node_right

        node_right.left=node
        node.parent=node_right
        node.right=right_left
        if(right_left.real):
            right_left.parent=node

        node.update_height()
        node_right.update_height()
        return 1

    def rotate_right(self,node):
        parent=node.parent
        node_left=node.left
        left_right=node_left.right

        node_left.parent=parent
        if(parent is None):
            self.root=node_left
        elif(parent.right==node):
            parent.right=node_left
        else:
            parent.left=node_left

        node_left.right=node
        node.parent=node_left
        node.left=left_right
        if(left_right.real):
            left_right.parent=node

        node.update_height()
        node_left.update_height()
        return 1
        
    def rotation_L_L(self,node):
        return self.rotate_left(node)
    
    def rotation_R_R(self,node):
        return self.rotate_right(node)
    
    def rotation_R_L(self,node):
        self.rotate_right(node.right)
        self.rotate_left(node)
        return 2
    
    def rotation_L_R(self,node):
        self.rotate_left(node.left)
        self.rotate_right(node)
        return 2
    
    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """
    def successor(self,node):
        curr=node
        curr=curr.right
        while curr.left.real:
            curr=curr.left
        return curr

    def delete(self, node):
        parent=node.parent
        node_to_balance=parent
        if (not node.right.real and not node.left.real):
            self.replace_parent_node(parent,node,self.virtual_node)
        elif(node.right.real and not node.left.real):
            self.replace_parent_node(parent,node,node.right)
        elif(not node.right.real and node.left.real):
            self.replace_parent_node(parent,node,node.left)
        else:
            old_node_height=node.height
            succ=self.successor(node)
            if succ.parent!=node:
                node_to_balance=succ.parent
            else:
                node_to_balance=succ
            if succ.parent!=node:
                succ.parent.left=succ.right
                if succ.right.real:
                    succ.right.parent=succ.parent
            self.replace_parent_node(parent,node,succ)
            succ.left=node.left
            succ.left.parent=succ
            if succ!=node.right:
                succ.right=node.right
                succ.right.parent=succ
            succ.update_height()
            if node_to_balance==succ:
                succ.height=old_node_height
        self.tree_size-=1
        if node_to_balance is None:
            return
        if self.is_avl:
            self.AVL_balance(node_to_balance,False)
        return
    
    def replace_parent_node(self,parent,old_node,new_node):
        if parent is None and new_node.real:
            self.root = new_node
            new_node.parent=None
        elif parent is None and not new_node.real:
            self.root=None
        elif parent.right==old_node:
            parent.right=new_node
            if new_node.real:
                new_node.parent=parent
        else:
           parent.left=new_node
           if new_node.real:
               new_node.parent=parent

    """returns a list representing dictionary 

    @rtype: list
    @returns: a list of (key, value) tuples sorted by key, representing the data structure
    """

    def avl_to_list(self):
        stack=[]
        res=[]
        curr=self.root
        if (curr is None):
            return []
        while len(stack)>0 or curr.real:
            while curr.real:
                stack.append(curr)
                curr=curr.left
            curr = stack.pop()
            res.append((curr.key,curr.value))
            curr=curr.right
        return res

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self):
        return self.tree_size

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self):
        return self.root

    """returns the height of the tree

        @rtype: int
        @returns: the height of the tree 
        """

    def get_height(self):
        if self.root is None:
            return -1
        if(self.is_avl):
            return self.root.height
        else:
            stack = [(self.root, 0)]
            max_height = 0
            while stack:
                curr, depth = stack.pop()
                if depth > max_height:
                    max_height = depth
                if curr.right.real:
                    stack.append((curr.right, depth + 1))
                if curr.left.real:
                    stack.append((curr.left, depth + 1))
            return max_height
