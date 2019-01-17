from typing import (Any, Callable, Dict, Optional)


# Initial single-linked list idea: https://dbader.org/blog/python-linked-list

class LinkedListNode:

    def __init__(self,
                 data: Dict = None,
                 previous_node: Optional["LinkedListNode"] = None,
                 next_node: Optional["LinkedListNode"] = None) -> None:
        if data is None:
            data = dict()
        self.data = data
        self.previous_node = previous_node
        self.next_node = next_node

    def __repr__(self) -> str:
        return "|{} <- {} -> {}|".format(
            str(self.previous_node.data) if self.previous_node else "{}",
            str(self.data),
            str(self.next_node.data) if self.next_node else "{}"
        )


class LinkedList:

    def __init__(self) -> None:
        # H <-> N1 <-> N2 <-> ... <-> T
        self.head: Optional["LinkedListNode"] = None
        self.tail: Optional["LinkedListNode"] = None

        self.__iteration_cursor: Optional[LinkedListNode] = self.head

    def __repr__(self) -> str:
        nodes = []

        current_node = self.head
        while current_node is not None:
            nodes.append(str(current_node))
            current_node = current_node.next_node

        return "\n".join([
            "H:{} T:{} ".format(self.head.data if self.head else "{}", self.tail.data if self.tail else "{}"),
            " , ".join(nodes)
        ])

    def __iter__(self) -> "LinkedList":
        self.__iteration_cursor = self.head
        return self

    def __next__(self) -> LinkedListNode:
        if self.__iteration_cursor:
            current_node = self.__iteration_cursor
        else:
            raise StopIteration
        self.__iteration_cursor = self.__iteration_cursor.next_node
        return current_node

    def prepend(self, data: Dict) -> None:
        """
        O(1) Insert new element at the list head
        """
        new_head_node = LinkedListNode(data=data, next_node=self.head)
        if self.head is not None:
            self.head.previous_node = new_head_node
        else:
            self.tail = new_head_node
        self.head = new_head_node

    def append(self, data: Dict) -> None:
        """
        O(1) Insert new element at list tail
        """
        new_tail_node = LinkedListNode(data=data, previous_node=self.tail)
        if self.tail is not None:
            self.tail.next_node = new_tail_node
        else:
            self.head = new_tail_node
        self.tail = new_tail_node

    def insert_after(self, data: Dict, node: LinkedListNode) -> None:
        """
        O(1) Insert new node after a specified one
        """
        if not node:
            raise ValueError("Must specify an origin node to insert after")

        new_node = LinkedListNode(data=data, previous_node=node, next_node=node.next_node)
        if node.next_node:
            node.next_node.previous_node = new_node
        node.next_node = new_node

        if self.tail == node:
            self.tail = new_node

    def find(self, target_key: str, target_value: Any) -> Optional["LinkedListNode"]:
        """
        O(N) Search for first occurrence of desired data (key-value pair)
        """
        current_node = self.head
        while (
            current_node is not None and (
                target_key not in current_node.data.keys() or
                (target_key in current_node.data.keys() and current_node.data[target_key] != target_value)
            )
        ):
            current_node = current_node.next_node

        return current_node

    def remove(self, target: LinkedListNode) -> None:
        """
        O(1) Delete first occurrence of desired data
        """
        if target is None:
            raise ValueError("Must specify a node to remove")

        previous_node = target.previous_node
        next_node = target.next_node

        if previous_node is not None:
            previous_node.next_node = next_node
        if next_node is not None:
            next_node.previous_node = previous_node

        if self.head == target:
            self.head = next_node
        if self.tail == target:
            self.tail = previous_node

        target.previous_node = None
        target.next_node = None

    def reverse(self) -> None:
        """
        O(N) Reverse list in-place
        """
        current_node = self.head
        new_tail_node = self.head
        previous_node = None
        next_node = None
        while current_node is not None:
            # 1. reversing cursors
            next_node = current_node.next_node

            # 2. next node becomes previous node
            current_node.previous_node = next_node
            # 3. previous node becomes next node
            current_node.next_node = previous_node

            # 4. reversing cursors
            previous_node = current_node
            # 5. reversing cursors
            current_node = next_node

        self.head = previous_node
        if self.head is not None:
            self.head.previous_node = None
        self.tail = new_tail_node
        if self.tail is not None:
            self.tail.next_node = None

    def flip(self, first_node: LinkedListNode, second_node: LinkedListNode, key: str) -> None:
        """
        O(N) Flips/interchanges two nodes' positions in-place
             Note: Assumes second_node is always after first_node
        """
        if not first_node or not second_node:
            raise ValueError("Must provide non-empty nodes")
        if not key:
            raise ValueError("Must provide non-empty key")

        node_a = self.find(target_key=key, target_value=first_node.data[key])
        if not node_a:
            raise IndexError("first_node not found")

        node_b = self.find(target_key=key, target_value=second_node.data[key])
        if not node_b:
            raise IndexError("second_node not found")

        node_a_previous_node = node_a.previous_node
        node_b_previous_node = node_b.previous_node

        # special case, consecutive nodes
        if node_b_previous_node == node_a:
            # because we'll first insert A, then B, so prepending B will make it end up before A
            node_b_previous_node = node_a_previous_node

        self.remove(node_a)
        self.remove(node_b)
        if node_b_previous_node:
            self.insert_after(data=node_a.data, node=node_b_previous_node)
        else:
            self.prepend(data=node_a.data)
        if node_a_previous_node:
            self.insert_after(data=node_b.data, node=node_a_previous_node)
        else:
            self.prepend(data=node_b.data)

    def clear(self) -> None:
        """
        O(N) Removes all elements from the list
        """
        current_node = self.head
        next_node = None
        while current_node is not None:
            next_node = current_node.next_node
            current_node.previous_node = None
            current_node.next_node = None
            current_node = next_node
        self.head = None
        self.tail = None

    def sort(self, comparison_function: Callable, reverse: bool = False) -> None:
        """
        O(N^2) Sorts the list items given a custom comparison function. By default sort is ascending.
               Note: No safety checks on comparison_function.
        """
        ordered_list = sorted(self, key=comparison_function, reverse=reverse)

        self.clear()

        for node in ordered_list:
            self.append(data=node.data)
