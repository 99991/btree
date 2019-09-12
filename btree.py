MIN_KEYS = 2
MAX_KEYS = MIN_KEYS*2 + 1

class Node(object):
    def __init__(self):
        self.n = 0
        self.keys = [None] * MAX_KEYS
        self.children = [None] * (MAX_KEYS + 1)

    def is_leaf(self):
        return self.children[0] is None

    def is_full(self):
        return self.n >= MAX_KEYS

    def __str__(self):
        if self.is_leaf():
            return str(self.keys[:self.n])
        
        s = ["["]
        for i in range(self.n):
            s.append(str(self.children[i]))
            s.append(",")
            s.append(str(self.keys[i]))
            s.append(",")
        s.append(str(self.children[self.n]))
        s.append("]")
        return "".join(s)

    __repr__ = __str__

def find_key_index(node, key):
    i = 0
    while i < node.n and key > node.keys[i]:
        i += 1
    return i

def find_min(node):
    while not node.is_leaf():
        node = node.children[0]
    return node.keys[0]

def find_max(node):
    while not node.is_leaf():
        node = node.children[node.n]
    return node.keys[node.n - 1]

def traverse(node):
    if node is not None:
        for i in range(node.n):
            yield from traverse(node.children[i])
            yield node.keys[i]
        yield from traverse(node.children[node.n])

def find(node, key):
    while node is not None:
        i = find_key_index(node, key)
    
        if i < node.n and key == node.keys[i]:
            return True
    
        node = node.children[i]
    
    return False

def insert_recursive(node, key):
    # find key position in node
    i = find_key_index(node, key)
    
    # check if key already exists
    if i < node.n and key == node.keys[i]: return
    
    if node.is_leaf():
        # insert key into leaf node
        for j in range(node.n, i, -1):
            node.keys[j] = node.keys[j - 1]
        node.keys[i] = key
        node.n += 1
    else:
        # insert key and possibly split child
        split = insert_recursive(node.children[i], key)
        
        # done if no split happened
        if not split: return
        
        # split result from insertion into child
        split_key, right_node = split
        
        # find split_key position in node
        i = find_key_index(node, key)
        
        # insert split_key and right_node from split into node
        for j in range(node.n, i, -1):
            node.keys[j] = node.keys[j - 1]
            node.children[j + 1] = node.children[j]
        node.keys[i] = split_key
        node.children[i + 1] = right_node
        node.n += 1
    
    # split node into node and right part if it is full
    if node.is_full():
        # split in the middle like:
        #  node.keys / split_key / right.keys
        # [:i_split] / [i_split] / [i_split + 1:]
        i_split = node.n >> 1
        split_key = node.keys[i_split]
        right = Node()
        right.n = node.n - (i_split + 1)
        for i in range(right.n):
            j = i + i_split + 1
            right.keys[i] = node.keys[j]
            right.children[i] = node.children[j]
            node.keys[j] = None
            node.children[j] = None
        right.children[right.n] = node.children[node.n]
        node.children[node.n] = None
        node.n = i_split
        
        return (split_key, right)

def insert(node, key):
    # create new node if none exists yet
    if node is None:
        node = Node()
        node.keys[0] = key
        node.n = 1
        return node
    
    split = insert_recursive(node, key)
    
    if split:        
        # create new parent node from node and split result
        split_key, right_node = split
        parent = Node()
        parent.children[0] = node
        parent.children[1] = right_node
        parent.keys[0] = split_key
        parent.n = 1
        return parent

    return node

def remove(node, key):
    i = find_key_index(node, key)
    
    if i < node.n and key == node.keys[i]:
        if node.is_leaf():
            # move keys[i+1:] to the left by 1
            for j in range(i + 1, node.n):
                node.keys[j - 1] = node.keys[j]
            node.n -= 1
        else:
            # override key with predecessor from child, then fix child
            predecessor = find_max(node.children[i])
            node.keys[i] = predecessor
            remove(node.children[i], predecessor)
            fix(node, i)
    else:
        # key not found
        if node.is_leaf(): return
        
        remove(node.children[i], key)
        # TODO why is this true?
        assert(i <= node.n)
        fix(node, i)
    
    return node if node.n > 0 else node.children[0]

def merge(parent, i):
    # merge child and its successor with parent's key[i] inbetween
    child = parent.children[i]
    successor = parent.children[i + 1]
    
    # remove key from node by moving keys and children to the left by 1
    key = parent.keys[i]
    for j in range(i + 1, parent.n):
        parent.keys[j - 1] = parent.keys[j]
        parent.children[j] = parent.children[j + 1]
    parent.children[parent.n] = None
    parent.n -= 1
    
    # append key and successor keys and children to child
    child.keys[child.n] = key
    for i in range(successor.n):
        child.keys[child.n + 1 + i] = successor.keys[i]
        child.children[child.n + 1 + i] = successor.children[i]
    child.children[child.n + 1 + successor.n] = successor.children[successor.n]
    child.n += successor.n + 1

def fix(node, i):
    # make it so that node's child[i] has at least MIN_KEYS
    if node.children[i].n >= MIN_KEYS: return
    if i == 0:
        # steal from successor if that node has keys
        if node.children[i + 1].n > MIN_KEYS:
            steal_from_successor(node, i)
        else:
            # merge child and its successor if both have few keys
            merge(node, i)
    else:
        # steal from predecessor if that node has keys
        if node.children[i - 1].n > MIN_KEYS:
            steal_from_predecessor(node, i)
        else:
            # merge child and its predecessor if both have few keys
            merge(node, i - 1)

def steal_from_predecessor(parent, i):
    child = parent.children[i]
    predecessor = parent.children[i - 1]
    # move child keys and values to the right
    child.children[child.n + 1] = child.children[child.n]
    for j in reversed(range(child.n)):
        child.keys[j + 1] = child.keys[j]
        child.children[j + 1]  = child.children[j]
    # child steals key form parent and node from predecessor
    child.keys[0] = parent.keys[i - 1]
    child.children[0] = predecessor.children[predecessor.n]
    # parent steals key from predecessor of child
    parent.keys[i - 1] = predecessor.keys[predecessor.n - 1]
    predecessor.children[predecessor.n] = None
    child.n += 1
    predecessor.n -= 1

def steal_from_successor(parent, i):
    child = parent.children[i]
    successor = parent.children[i + 1]
    # child steals key from parent and node from successor
    child.keys[child.n] = parent.keys[i]
    child.children[child.n + 1] = successor.children[0]
    # parent steals key from successor
    parent.keys[i] = successor.keys[0]
    # move successor keys and children to the left
    for j in range(1, successor.n):
        successor.keys[j - 1] = successor.keys[j]
        successor.children[j - 1] = successor.children[j]
    successor.children[successor.n - 1] = successor.children[successor.n]
    successor.children[successor.n] = None
    child.n += 1
    successor.n -= 1

def get_depths(node, depth=0):
    if node.is_leaf():
        yield depth
    else:
        for i in range(node.n + 1):
            yield from get_depths(node.children[i], depth + 1)

def check_node(node, lower_bound=-float("inf"), upper_bound=float("inf"), depth=0):
    if node is None:
        assert(depth == 0)
        return
    assert(node.n < MAX_KEYS)
    if depth == 0:
        depths = list(get_depths(node))
        assert(all(depth == depths[0] for depth in depths))
    else:
        assert(node.n >= MIN_KEYS)
    # check if keys exist
    assert(all(node.keys[i] is not None for i in range(node.n)))
    # check if keys are within bounds
    assert(all(lower_bound < node.keys[i] < upper_bound for i in range(node.n)))
    # check if either all or no childen exist
    if node.is_leaf():
        assert(all(node.children[i] is None for i in range(node.n + 1)))
    else:
        assert(all(node.children[i] is not None for i in range(node.n + 1)))
        # check children within bounds
        check_node(node.children[0], lower_bound, node.keys[0], depth + 1)
        for i in range(1, node.n):
            check_node(node.children[i], node.keys[i - 1], node.keys[i], depth + 1)
        check_node(node.children[node.n], node.keys[node.n - 1], upper_bound, depth + 1)

class BTreeSet(object):
    def __init__(self):
        self.root = None
    
    def add(self, key):
        self.root = insert(self.root, key)
    
    def remove(self, key):
        self.root = remove(self.root, key)
    
    def __iter__(self):
        yield from traverse(self.root)

    def check(self):
        check_node(self.root)

    def min(self):
        return find_min(self.root)
    
    def max(self):
        return find_max(self.root)

    def __in__(self, key):
        return find(self.root, key)

    def __str__(self):
        return "BTreeSet(%s)" % str(self.root)
    
    __repr__ = __str__
