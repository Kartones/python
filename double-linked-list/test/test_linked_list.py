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

    linked_list.remove(target_key="id", target_value=node_2_data["id"])
    assert linked_list.head is not None
    assert linked_list.head.data == node_1_data
    assert linked_list.head.next_node is not None
    assert linked_list.head.next_node.data == node_3_data
    assert linked_list.tail is not None
    assert linked_list.tail.data == node_4_data
    assert linked_list.tail.previous_node is not None
    assert linked_list.tail.previous_node.data == node_3_data

    linked_list.remove(target_key="id", target_value=node_1_data["id"])
    assert linked_list.head is not None
    assert linked_list.head.data == node_3_data
    assert linked_list.head.next_node is not None
    assert linked_list.head.next_node.data == node_4_data
    assert linked_list.tail is not None
    assert linked_list.tail.data == node_4_data
    assert linked_list.tail.previous_node is not None
    assert linked_list.tail.previous_node.data == node_3_data

    linked_list.remove(target_key="id", target_value=node_4_data["id"])
    assert linked_list.head is not None
    assert linked_list.head.data == node_3_data
    assert linked_list.head.next_node is None
    assert linked_list.tail is not None
    assert linked_list.tail.data == node_3_data
    assert linked_list.tail.previous_node is None

    linked_list.remove(target_key="id", target_value=node_3_data["id"])
    assert linked_list.head is None
    assert linked_list.tail is None


def test_removing_from_empty_list() -> None:
    linked_list = LinkedList()

    linked_list.remove(target_key="id", target_value="an_irrelevant_value")

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
