from typing import Any, Dict, Optional


# Based on https://dbader.org/blog/python-linked-list

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
    """
    Double linked list implementation
    """

    def __init__(self) -> None:
        # H <-> N1 <-> N2 <-> ... <-> T
        self.head = None    # type: Optional["LinkedListNode"]
        self.tail = None    # type: Optional["LinkedListNode"]

    def __repr__(self) -> str:
        nodes = []

        current_node = self.head
        while current_node is not None:
            nodes.append(str(current_node))
            current_node = current_node.next_node

        return " , ".join(nodes)

    def prepend(self, data: Dict) -> None:
        """
        O(1) Insert new element at the list head
        """
        new_head_node = LinkedListNode(data=data, next_node=self.head)
        if self.head is not None:
            self.head.previous_node = new_head_node
            new_head_node.next_node = self.head
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
            new_tail_node.previous_node = self.tail
        else:
            self.head = new_tail_node
        self.tail = new_tail_node

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

    def remove(self, target_key: str, target_value: Any) -> None:
        """
        O(N) Delete first occurrence of desired data
        """
        target_item = self.find(target_key=target_key, target_value=target_value)
        if target_item is None:
            return

        previous_node = target_item.previous_node
        next_node = target_item.next_node

        if previous_node is not None:
            previous_node.next_node = next_node
        if next_node is not None:
            next_node.previous_node = previous_node

        if self.head == target_item:
            self.head = next_node
        if self.tail == target_item:
            self.tail = previous_node

        target_item.previous_node = None
        target_item.next_node = None

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
