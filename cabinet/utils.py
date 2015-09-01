#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
BUG: Be careful,

nodes = ['test/asdf', 'test']
print TreeList(nodes).get_tree()

{
    'test': null
}

but,

nodes = ['test', 'test/asdf']
print TreeList(nodes).get_tree()

{
    'test': {
        'asdf': null
    }
}

as a workaround, sorting the node list seems to 'fix' it.
"""


class TreeList(object):
    """
    Tree (dict) and list representation of nodes.
    """
    def __init__(self, items=None):
        """
        :param items: the nodes to initialize the tree
        :type items: list
        """
        if items is None:
            self._node_list = []
        else:
            self._node_list = items

    def _list_to_tree(self, nodes):
        base_tree = tree = {}

        for n in nodes:
            parts = n.split('/')
            for i in parts:
                if i == parts[-1]:
                    tree[i] = None
                else:
                    if tree.get(i) is None:
                        tree[i] = {}
                    tree = tree[i]

            tree = base_tree

        return tree

    def _tree_to_list(self, root):
        l = []
        print root
        for n in root.keys():
            if root[n] is None:
                l.append(n)
            else:
                for i in self._tree_to_list(root[n]):
                    item = n + '/' + i
                    l.append(item)

        return l

    def get_tree(self):
        return self._list_to_tree(self._node_list)

    def get_list(self):
        return self._node_list

    def get_from_tree(self, key):
        """
        None -> ok
        exception -> not ok
        """
        value = self.get_tree()

        for n in key.split('/'):
            value = value[n]

        return value

if __name__ == "__main__":
    nodes = [
        "sample-item",
        "demo-stuff",
        "test/yahoo-mail",
        "test/family-safe-code",
        "my-company/alarm-code",
        "my-company/admin-mail",
        "my-company/mails/admin",
        "my-company/mails/userA",
    ]

    my_tree = TreeList(nodes)

    import pprint
    pprint.pprint(my_tree.get_tree())
    pprint.pprint(my_tree.get_list())
    print my_tree.get_from_tree('my-company/alarm-code')
