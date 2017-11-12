#!/usr/bin/python

import json
import os
from typing import Dict

import requests

import secrets as config


def fetch_boards() -> Dict:
    response = requests.get("https://api.trello.com/1/members/me/boards?&key={key}&token={token}".format(
        key=config.KEY, token=config.TOKEN))
    json_data = json.loads(response.text)
    if not config.INCLUDE_CLOSED:
        json_data = [item for item in json_data if item["closed"] is False]
    if not config.INCLUDE_ORGANIZATIONS:
        json_data = [item for item in json_data if item["idOrganization"] is None]
    return json_data


def fetch_board_details(board_id: str) -> Dict:
    response = requests.get(
        ("https://api.trello.com/1/boards/{id}?actions=all&actions_limit=1000" +
         "&card_attachment_fields=all&cards=all&lists=all&members=all&member_fields=all&card_attachment_fields=all" +
         "&checklists=all&fields=all&key={key}&token={token}").format(id=board_id, key=config.KEY, token=config.TOKEN)
    )
    return json.loads(response.text)


def save_all_attachments(board_data: Dict) -> None:
    data_folder = get_data_folder(board_data)
    for action in board_data["actions"]:
        if "attachment" in action["data"] and "url" in action["data"]["attachment"]:
            response = requests.get(action["data"]["attachment"]["url"])
            filename = os.path.join(data_folder, action["data"]["attachment"]["name"])
            with open(filename, "w+b") as file:
                file.write(response.content)
            print("    > Written attachment '{}'".format(action["data"]["attachment"]["name"]))


def basic_boards_info(boards_list: Dict) -> None:
    print("> Boards count: {}".format(len(boards_list)))
    print("> Boards: ")
    for board in boards_list:
        print("    {} ({})".format(board["name"], board["url"]))


def get_data_folder(board_data: Dict) -> str:
    return os.path.join(".", board["id"])


def save_to_file(board_data: Dict) -> None:
    data_folder = get_data_folder(board_data)
    if not os.path.exists(data_folder):
        os.mkdir(data_folder)
    filename = os.path.join(data_folder, "data.json")
    with open(filename, "w+") as file:
        file.write(json.dumps(board_data))
    print("> Written file '{}'".format(filename))


if __name__ == "__main__":
    boards_list = fetch_boards()
    basic_boards_info(boards_list)
    for board in boards_list:
        board_data = fetch_board_details(board["id"])

        save_to_file(board_data)
        if config.INCLUDE_ATTACHMENTS:
            save_all_attachments(board_data)
