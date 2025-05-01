import json

class BSTNode:
    def __init__(self, key, value, left=None, right=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right
        self.size = 1

    def __str__(self, level=0, prefix="Root: "):
        ret = " " * (level * 4) + prefix + str(self.key) + "\n"
        if self.left is not None:
            ret += self.left.__str__(level + 1, "L--- ")
        else:
            ret += " " * ((level + 1) * 4) + "L--- None\n"
        if self.right is not None:
            ret += self.right.__str__(level + 1, "R--- ")
        else:
            ret += " " * ((level + 1) * 4) + "R--- None\n"
        return ret

class BST:
    """
    A class representing a Binary Search Tree (BST).

    Methods
    -------
    __init__():
        Initializes an empty BST.
    get(key):
        Retrieves the value associated with the given key in the BST.
    get_min():
        Finds the minimum key in the BST.
    get_max():
        Finds the maximum key in the BST.
    put(key, value):
        Inserts a key-value pair into the BST. If the key already exists, updates its value.
    delete_min():
        Deletes the node with the minimum key in the BST.
    delete_max():
        Deletes the node with the maximum key in the BST.
    delete(key):
        Deletes the node with the given key from the BST.
    floor(key):
        Finds the largest key less than or equal to the given key.
    ceil(key):
        Finds the smallest key greater than or equal to the given key.
    inorder():
        Returns a list of key-value pairs in the BST in in-order traversal.
    items():
        Returns a list of key-value pairs in the BST.
    keys():
        Returns a list of keys in the BST.
    values():
        Returns a list of values in the BST.
    size():
        Returns the number of nodes in the BST.
    __str__():
        Returns a string representation of the BST.
    """
    
    def __init__(self):
        """
        Initializes an empty BST.
        """
        self.root = None

    def _create_node(self, key, value):
        return BSTNode(key, value)

    def get(self, key):
        """
        Retrieves the value associated with the given key in the BST.

        Parameters
        ----------

        key : any
            The key to search for in the BST.

        Returns
        -------

        any
            The value associated with the given key, or None if the key is not found.
        """
        return self._get(key, self.root)
    
    def _get(self, key, node):
        if node is None: return None

        if key == node.key: return node.value
        if key < node.key: return self._get(key, node.left)
        if key > node.key: return self._get(key, node.right)

    def get_min(self):
        """
        Finds the minimum key in the BST.

        Returns
        -------

        any
            The minimum key in the BST.
        """
        return self._get_min(self.root)
    
    def _get_min(self, node):
        if node.left is None: return node.key

        return self._get_min(node.left)
    
    def get_max(self):
        """
        Finds the maximum key in the BST.

        Returns
        -------

        any
            The maximum key in the BST.
        """
        return self._get_max(self.root)
    
    def _get_max(self, node):
        if node.right is None: return node.key

        return self._get_max(node.right)
    
    def put(self, key, value):
        """
        Inserts a key-value pair into the BST. If the key already exists, updates its value.

        Parameters
        ----------

        key : any
            The key to insert into the BST.
        value : any
            The value to associate with the key.
        """
        self.root = self._put(key, value, self.root)
    
    def _put(self, key, value, node):
        if node is None: return self._create_node(key, value)

        if key == node.key: node.value = value
        if key < node.key: node.left = self._put(key, value, node.left)
        if key > node.key: node.right = self._put(key, value, node.right)

        self._update(node)
        return node
    
    def delete_min(self):
        """
        Deletes the node with the minimum key in the BST.
        """
        if self.root:
            self.root = self._delete_min(self.root)
    
    def _delete_min(self, node):
        if node.left is None:
            return node.right
        node.left = self._delete_min(node.left)
        self._update(node)
        return node
    
    def delete_max(self):
        """
        Deletes the node with the maximum key in the BST.
        """
        if self.root: 
            self.root = self._delete_max(self.root)

    def _delete_max(self, node):
        if node.right is None:
            return node.left
        node.right = self._delete_max(node.right)
        self._update(node)
        return node
    
    def delete(self, key):
        """
        Deletes the node with the given key from the BST.

        Parameters
        ----------

        key : any
            The key of the node to delete from the BST.
        """
        self.root = self._delete(key, self.root)

    def _delete(self, key, node):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(key, node.left)
        elif key > node.key:
            node.right = self._delete(key, node.right)
        else:
            # Key match
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            temp = node
            node = self._get_min(temp.right)
            node.right = self._delete_min(temp.right)
            node.left = temp.left

        self._update(node)
        return node
    
    def _update(self, node):
        node.size = 1 + self._size(node.left) + self._size(node.right)
    
    def floor(self, key):
        """
        Finds the largest key less than or equal to the given key.

        Parameters
        ----------

        key : any
            The key to compare against.

        Returns
        -------

        any
            The largest key less than or equal to the given key, or None if no such key exists.
        """
        return self._floor(key, self.root)

    def _floor(self, key, node):
        if node is None: return None

        if key == node.key: return key
        if key < node.key: return self._floor(key, node.left)
        if key > node.key:
            fl = self._floor(key, node.right)
            return fl if fl else node.key
        
    def ceil(self, key):
        """
        Finds the smallest key greater than or equal to the given key.

        Parameters
        ----------

        key : any
            The key to compare against.

        Returns
        -------

        any
            The smallest key greater than or equal to the given key, or None if no such key exists.
        """
        return self._ceil(key, self.root)
    
    def _ceil(self, key, node):
        if node is None:
            return None
    
        if key == node.key:
            return key
        if key > node.key:
            return self._ceil(key, node.right)
        if key < node.key:
            cl = self._ceil(key, node.left)
            return cl if cl else node.key
        
    def inorder(self):
        """
        Returns a list of key-value pairs in the BST in in-order traversal.

        Returns
        -------

        list of tuple
            A list of key-value pairs in the BST in in-order traversal.
        """
        order = []
        self._inorder(self.root, order)
        return order
    
    def _inorder(self, node, path):
        if node is None: return

        self._inorder(node.left, path)
        path.append((node.key, node.value))
        self._inorder(node.right, path)

    def range_select(self, lo, hi):
        """
        Returns a list of key-value pairs in the BST in the range [lo, hi].

        Parameters
        ----------

        lo : any
            The lower bound of the range.
        hi : any
            The upper bound of the range.

        Returns
        -------

        list of tuple
            A list of key-value pairs in the BST in the range [lo, hi].
        """
        result = []
        self._range_select(self.root, lo, hi, result)
        return result

    def _range_select(self, node, lo, hi, result):
        if node is None:
            return

        if lo < node.key:
            self._range_select(node.left, lo, hi, result)

        if lo <= node.key <= hi:
            result.append((node.key, node.value))

        if hi > node.key:
            self._range_select(node.right, lo, hi, result)

    def items(self):
        """
        Returns a list of key-value pairs in the BST.

        Returns
        -------

        list of tuple
            A list of key-value pairs in the BST.
        """
        return self.inorder()
    
    def keys(self):
        """
        Returns a list of keys in the BST.

        Returns
        -------

        list
            A list of keys in the BST.
        """
        return [x for x,_ in self.items()]
    
    def values(self):
        """
        Returns a list of values in the BST.

        Returns
        -------

        list
            A list of values in the BST.
        """
        return [x for _,x in self.items()]
    
    def size(self):
        """
        Returns the number of nodes in the BST.

        Returns
        -------

        int
            The number of nodes in the BST.
        """
        return self._size(self.root)
    
    def _size(self, node):
        return node.size if node else 0

    def __str__(self):
        """
        Returns a string representation of the BST.

        Returns
        -------

        str
            A string representation of the BST.
        """
        return str(self.root) if self.root is not None else "Empty tree"
    
class BSTCodec:
    @staticmethod
    def encode(bst, key_codec, val_codec):
        """
        Encodes a BST to a JSON string.

        Parameters
        ----------
        bst : BST
            The BST to encode.
        key_codec : object
            An object with an encode() method for encoding keys.
        val_codec : object
            An object with an encode() method for encoding values.

        Returns
        -------
        str
            The encoded JSON string representation of the BST.
        """
        def _encode_node(node):
            if node is None:
                return None
            return {
                "key": key_codec.encode(node.key),
                "value": val_codec.encode(node.value),
                "left": _encode_node(node.left),
                "right": _encode_node(node.right)
            }
        
        return json.dumps(_encode_node(bst.root))

    @staticmethod
    def decode(data, key_codec, val_codec):
        """
        Decodes a JSON string to a BST.

        Parameters
        ----------
        data : str
            The JSON string representation of the BST.
        key_codec : object
            An object with a decode() method for decoding keys.
        val_codec : object
            An object with a decode() method for decoding values.

        Returns
        -------
        BST
            The decoded BST.
        """
        def _decode_node(data):
            if data is None:
                return None
            node = BSTNode(
                key_codec.decode(data["key"]),
                val_codec.decode(data["value"])
            )
            node.left = _decode_node(data["left"])
            node.right = _decode_node(data["right"])
            return node
        
        bst = BST()
        bst.root = _decode_node(json.loads(data))
        return bst