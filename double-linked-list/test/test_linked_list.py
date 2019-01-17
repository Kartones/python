from linked_list import LinkedList


def test_initial_list_state() -> None:
    linked_list = LinkedList()
    assert linked_list.head is None
    assert linked_list.tail is None


def test_prepending_elements() -> None:
    node_1_data = {"id": 1}
    node_2_data = {"id": 2}
    node_3_data = {"id": 3}
    linked_list = LinkedList()

    linked_list.prepend(data=node_1_data)
    assert linked_list.head is not None
    assert linked_list.head.data == node_1_data
    assert linked_list.tail is not None
    assert linked_list.tail.data == node_1_data

    linked_list.prepend(data=node_2_data)
    assert linked_list.head.data == node_2_data
    assert linked_list.head.next_node is not None
    assert linked_list.head.next_node.data == node_1_data
    assert linked_list.head.previous_node is None
    assert linked_list.tail.data == node_1_data
    assert linked_list.tail.next_node is None
    assert linked_list.tail.previous_node is not None
    assert linked_list.tail.previous_node.data == node_2_data

    linked_list.prepend(data=node_3_data)
    assert linked_list.head.data == node_3_data
    assert linked_list.head.next_node is not None
    assert linked_list.head.next_node.data == node_2_data
    assert linked_list.head.previous_node is None
    assert linked_list.tail.data == node_1_data
    assert linked_list.tail.next_node is None
    assert linked_list.tail.previous_node is not None
    assert linked_list.tail.previous_node.data == node_2_data

    middle_node = linked_list.head.next_node
    assert middle_node.data == node_2_data
    assert middle_node.next_node is not None
    assert middle_node.next_node.data is not None
    assert middle_node.next_node.data == node_1_data
    assert middle_node.previous_node is not None
    assert middle_node.previous_node.data is not None
    assert middle_node.previous_node.data == node_3_data


def test_appending_elements() -> None:
    node_1_data = {"id": 1}
    node_2_data = {"id": 2}
    node_3_data = {"id": 3}
    linked_list = LinkedList()

    linked_list.append(data=node_1_data)
    assert linked_list.head is not None
    assert linked_list.head.data == node_1_data
    assert linked_list.tail is not None
    assert linked_list.tail.data == node_1_data

    linked_list.append(data=node_2_data)
    assert linked_list.head.data == node_1_data
    assert linked_list.head.next_node is not None
    assert linked_list.head.next_node.data == node_2_data
    assert linked_list.head.previous_node is None
    assert linked_list.tail.data == node_2_data
    assert linked_list.tail.next_node is None
    assert linked_list.tail.previous_node is not None
    assert linked_list.tail.previous_node.data == node_1_data

    linked_list.append(data=node_3_data)
    assert linked_list.head.data == node_1_data
    assert linked_list.head.next_node is not None
    assert linked_list.head.next_node.data == node_2_data
    assert linked_list.head.previous_node is None
    assert linked_list.tail.data == node_3_data
    assert linked_list.tail.next_node is None
    assert linked_list.tail.previous_node is not None
    assert linked_list.tail.previous_node.data == node_2_data

    middle_node = linked_list.head.next_node
    assert middle_node.data == node_2_data
    assert middle_node.next_node is not None
    assert middle_node.next_node.data is not None
    assert middle_node.next_node.data == node_3_data
    assert middle_node.previous_node is not None
    assert middle_node.previous_node.data is not None
    assert middle_node.previous_node.data == node_1_data


def test_finding_elements() -> None:
    node_1_data = {"id": 1}
    node_2_data = {"id": 2}
    node_3_data = {"id": 3}
    other_data = {"id": 4}
    linked_list = LinkedList()
    linked_list.append(node_1_data)
    linked_list.append(node_2_data)
    linked_list.append(node_3_data)

    node = linked_list.find(target_key="id", target_value=node_1_data["id"])
    assert node is not None
    assert node.data == node_1_data

    node = linked_list.find(target_key="id", target_value=node_2_data["id"])
    assert node is not None
    assert node.data == node_2_data

    node = linked_list.find(target_key="id", target_value=node_3_data["id"])
    assert node is not None
    assert node.data == node_3_data

    assert linked_list.find(target_key="id", target_value=other_data["id"]) is None
    assert linked_list.find(target_key="inexistant_key", target_value="an_irrelevant_value") is None


def test_finding_elements_on_empty_list() -> None:
    linked_list = LinkedList()

    linked_list.find(target_key="id", target_value="an_irrelevant_value")

    assert linked_list.head is None
    assert linked_list.tail is None


def test_removing_elements() -> None:
    node_1_data = {"id": 1}
    node_2_data = {"id": 2}
    node_3_data = {"id": 3}
    node_4_data = {"id": 4}
    linked_list = LinkedList()
    linked_list.append(node_1_data)
    linked_list.append(node_2_data)
    linked_list.append(node_3_data)
    linked_list.append(node_4_data)

    node_2 = linked_list.find(target_key="id", target_value=node_2_data["id"])
    linked_list.remove(node_2)
    assert linked_list.head is not None
    assert linked_list.head.data == node_1_data
    assert linked_list.head.next_node is not None
    assert linked_list.head.next_node.data == node_3_data
    assert linked_list.tail is not None
    assert linked_list.tail.data == node_4_data
    assert linked_list.tail.previous_node is not None
    assert linked_list.tail.previous_node.data == node_3_data

    node_1 = linked_list.find(target_key="id", target_value=node_1_data["id"])
    linked_list.remove(node_1)
    assert linked_list.head is not None
    assert linked_list.head.data == node_3_data
    assert linked_list.head.next_node is not None
    assert linked_list.head.next_node.data == node_4_data
    assert linked_list.tail is not None
    assert linked_list.tail.data == node_4_data
    assert linked_list.tail.previous_node is not None
    assert linked_list.tail.previous_node.data == node_3_data

    node_4 = linked_list.find(target_key="id", target_value=node_4_data["id"])
    linked_list.remove(node_4)
    assert linked_list.head is not None
    assert linked_list.head.data == node_3_data
    assert linked_list.head.next_node is None
    assert linked_list.tail is not None
    assert linked_list.tail.data == node_3_data
    assert linked_list.tail.previous_node is None

    node_3 = linked_list.find(target_key="id", target_value=node_3_data["id"])
    linked_list.remove(node_3)
    assert linked_list.head is None
    assert linked_list.tail is None


def test_reversing_list() -> None:
    node_1_data = {"id": 1}
    node_2_data = {"id": 2}
    node_3_data = {"id": 3}
    node_4_data = {"id": 4}
    linked_list = LinkedList()
    linked_list.append(node_1_data)
    linked_list.append(node_2_data)
    linked_list.append(node_3_data)
    linked_list.append(node_4_data)

    linked_list.reverse()

    assert linked_list.head is not None
    assert linked_list.head.data == node_4_data
    assert linked_list.head.previous_node is None

    second_node = linked_list.head.next_node
    assert second_node is not None
    assert second_node.data == node_3_data
    third_node = second_node.next_node
    assert third_node is not None
    assert third_node.data == node_2_data
    fourth_node = third_node.next_node
    assert fourth_node is not None
    assert fourth_node.data == node_1_data
    assert fourth_node.next_node is None

    assert linked_list.tail is not None
    assert fourth_node.data == linked_list.tail.data

    # Now go back to check previous links
    third_node = fourth_node.previous_node
    assert third_node is not None
    assert third_node.data == node_2_data
    second_node = third_node.previous_node
    assert second_node is not None
    assert second_node.data == node_3_data
    first_node = second_node.previous_node
    assert first_node is not None
    assert first_node.data == node_4_data


def test_reversing_empty_list() -> None:
    linked_list = LinkedList()
    linked_list.reverse()

    assert linked_list.head is None
    assert linked_list.tail is None


def test_insert_after() -> None:
    node_1_data = {"id": 1}
    node_2_data = {"id": 2}
    node_3_data = {"id": 3}
    node_4_data = {"id": 4}
    linked_list = LinkedList()
    linked_list.append(node_1_data)
    linked_list.append(node_2_data)

    node_1 = linked_list.find(target_key="id", target_value=node_1_data["id"])

    # Normal insert scenario
    linked_list.insert_after(data=node_3_data, node=node_1)

    assert linked_list.head.data == node_1_data
    second_node = linked_list.head.next_node
    assert second_node is not None
    assert second_node.data == node_3_data
    third_node = second_node.next_node
    assert third_node is not None
    assert third_node.data == node_2_data
    assert third_node.next_node is None
    assert linked_list.tail.data == node_2_data

    node_2 = linked_list.find(target_key="id", target_value=node_2_data["id"])

    # Insert at tail scenario
    linked_list.insert_after(data=node_4_data, node=node_2)

    assert linked_list.head.data == node_1_data
    second_node = linked_list.head.next_node
    assert second_node is not None
    assert second_node.data == node_3_data
    third_node = second_node.next_node
    assert third_node is not None
    assert third_node.data == node_2_data
    fourth_node = third_node.next_node
    assert fourth_node is not None
    assert fourth_node.data == node_4_data
    assert fourth_node.next_node is None
    assert linked_list.tail.data == node_4_data


def test_flip() -> None:
    node_1_data = {"id": 1}
    node_2_data = {"id": 2}
    node_3_data = {"id": 3}
    node_4_data = {"id": 4}
    node_5_data = {"id": 5}
    linked_list = LinkedList()
    linked_list.append(node_1_data)
    linked_list.append(node_2_data)
    linked_list.append(node_3_data)
    linked_list.append(node_4_data)
    linked_list.append(node_5_data)

    # non-consecutive nodes:
    # 1 2 3 4 5 -> 1 4 3 2 5
    linked_list.flip(linked_list.head.next_node, linked_list.tail.previous_node, "id")

    first_node = linked_list.head
    assert first_node.data == node_1_data
    assert first_node.previous_node is None
    assert first_node.next_node.data == node_4_data
    second_node = linked_list.head.next_node
    assert second_node is not None
    assert second_node.data == node_4_data
    assert second_node.previous_node.data == node_1_data
    assert second_node.next_node.data == node_3_data
    third_node = second_node.next_node
    assert third_node is not None
    assert third_node.data == node_3_data
    assert third_node.previous_node.data == node_4_data
    assert third_node.next_node.data == node_2_data
    fourth_node = third_node.next_node
    assert fourth_node is not None
    assert fourth_node.data == node_2_data
    assert fourth_node.previous_node.data == node_3_data
    assert fourth_node.next_node.data == node_5_data
    fifth_node = fourth_node.next_node
    assert fifth_node is not None
    assert fifth_node.data == node_5_data
    assert fifth_node.previous_node.data == node_2_data
    assert fifth_node.next_node is None
    assert linked_list.tail.data == node_5_data

    # consecutive nodes:
    # 1 4 3 2 5 -> 1 4 2 3 5
    linked_list.flip(linked_list.tail.previous_node.previous_node, linked_list.tail.previous_node, "id")

    first_node = linked_list.head
    assert first_node.data == node_1_data
    assert first_node.previous_node is None
    assert first_node.next_node.data == node_4_data
    second_node = linked_list.head.next_node
    assert second_node is not None
    assert second_node.data == node_4_data
    assert second_node.previous_node.data == node_1_data
    assert second_node.next_node.data == node_2_data
    third_node = second_node.next_node
    assert third_node is not None
    assert third_node.data == node_2_data
    assert third_node.previous_node.data == node_4_data
    assert third_node.next_node.data == node_3_data
    fourth_node = third_node.next_node
    assert fourth_node is not None
    assert fourth_node.data == node_3_data
    assert fourth_node.previous_node.data == node_2_data
    assert fourth_node.next_node.data == node_5_data
    fifth_node = fourth_node.next_node
    assert fifth_node is not None
    assert fifth_node.data == node_5_data
    assert fifth_node.previous_node.data == node_3_data
    assert fifth_node.next_node is None
    assert linked_list.tail.data == node_5_data

    # A = head B = tail
    # 1 4 3 2 5 -> 5 4 2 3 1
    linked_list.flip(linked_list.head, linked_list.tail, "id")

    first_node = linked_list.head
    assert first_node.data == node_5_data
    assert first_node.previous_node is None
    assert first_node.next_node.data == node_4_data
    second_node = linked_list.head.next_node
    assert second_node is not None
    assert second_node.data == node_4_data
    assert second_node.previous_node.data == node_5_data
    assert second_node.next_node.data == node_2_data
    third_node = second_node.next_node
    assert third_node is not None
    assert third_node.data == node_2_data
    assert third_node.previous_node.data == node_4_data
    assert third_node.next_node.data == node_3_data
    fourth_node = third_node.next_node
    assert fourth_node is not None
    assert fourth_node.data == node_3_data
    assert fourth_node.previous_node.data == node_2_data
    assert fourth_node.next_node.data == node_1_data
    fifth_node = fourth_node.next_node
    assert fifth_node is not None
    assert fifth_node.data == node_1_data
    assert fifth_node.previous_node.data == node_3_data
    assert fifth_node.next_node is None
    assert linked_list.tail.data == node_1_data


def test_clear() -> None:
    node_1_data = {"id": 1}
    node_2_data = {"id": 2}
    node_3_data = {"id": 3}
    node_4_data = {"id": 4}

    linked_list = LinkedList()
    linked_list.append(node_4_data)
    linked_list.append(node_3_data)
    linked_list.append(node_2_data)
    linked_list.append(node_1_data)

    linked_list.clear()

    assert linked_list.head is None
    assert linked_list.tail is None


def test_sorting() -> None:

    def node_comparison_function(node):
        return int(node.data["id"]) if node else 0

    node_1_data = {"id": 1}
    node_2_data = {"id": 2}
    node_3_data = {"id": 3}
    node_4_data = {"id": 4}

    linked_list = LinkedList()
    linked_list.append(node_4_data)
    linked_list.append(node_3_data)
    linked_list.append(node_2_data)
    linked_list.append(node_1_data)

    # 4 3 2 1 -> 1 2 3 4
    linked_list.sort(comparison_function=node_comparison_function)

    first_node = linked_list.head
    assert first_node.data == node_1_data
    assert first_node.previous_node is None
    assert first_node.next_node.data == node_2_data
    second_node = linked_list.head.next_node
    assert second_node is not None
    assert second_node.data == node_2_data
    assert second_node.previous_node.data == node_1_data
    assert second_node.next_node.data == node_3_data
    third_node = second_node.next_node
    assert third_node is not None
    assert third_node.data == node_3_data
    assert third_node.previous_node.data == node_2_data
    assert third_node.next_node.data == node_4_data
    fourth_node = third_node.next_node
    assert fourth_node is not None
    assert fourth_node.data == node_4_data
    assert fourth_node.previous_node.data == node_3_data
    assert fourth_node.next_node is None
    assert linked_list.tail.data == node_4_data

    linked_list = LinkedList()
    linked_list.append(node_1_data)
    linked_list.append(node_2_data)
    linked_list.append(node_3_data)
    linked_list.append(node_4_data)

    # 1 2 3 4 -> 4 3 2 1
    linked_list.sort(comparison_function=node_comparison_function, reverse=True)

    first_node = linked_list.head
    assert first_node.data == node_4_data
    assert first_node.previous_node is None
    assert first_node.next_node.data == node_3_data
    second_node = linked_list.head.next_node
    assert second_node is not None
    assert second_node.data == node_3_data
    assert second_node.previous_node.data == node_4_data
    assert second_node.next_node.data == node_2_data
    third_node = second_node.next_node
    assert third_node is not None
    assert third_node.data == node_2_data
    assert third_node.previous_node.data == node_3_data
    assert third_node.next_node.data == node_1_data
    fourth_node = third_node.next_node
    assert fourth_node is not None
    assert fourth_node.data == node_1_data
    assert fourth_node.previous_node.data == node_2_data
    assert fourth_node.next_node is None
    assert linked_list.tail.data == node_1_data
