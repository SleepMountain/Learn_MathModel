class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.size = 1

def insert(root, val):
    if not root:
        return TreeNode(val)

    if val < root.val:
        root.left = insert(root.left, val)
    else:
        root.right = insert(root.right, val)

    root.size += 1
    return root


def rank(root, val):
    if not root:
        return 0

    if val == root.val:
        return root.left.size if root.left else 0

    if val < root.val:
        return rank(root.left, val)
    else:
        return 1 + (root.left.size if root.left else 0) + rank(root.right, val)


def ith_successor(root, i):
    if not root:
        return None

    r = root.left.size if root.left else 0
    if r + 1 == i:
        return root.val
    elif r + 1 < i:
        return ith_successor(root.right, i - r - 1)
    else:
        return ith_successor(root.left, i)



if __name__ == "__main__":

    root = None
    elements = [3, 1, 4, 2, 5]
    for val in elements:
        root = insert(root, val)

    i = 3
    successor = ith_successor(root, i)
    print(f"顺序中的第{i}个继承者是：{successor}")
