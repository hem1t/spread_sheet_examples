#!/usr/bin/env python3

from bintrees import AVLTree
import json, re

def _json_to_table(tree):
    table = AVLTree()
    for row in tree.keys():
        for cell in tree[row].keys():
            key = cell + row
            table.insert(key, tree[row][cell])
    return table


class Sheet:
    def __init__(self, file_name):
        with open(file_name, "r") as file:
            sheet = json.loads(file.read())
        self.table = _json_to_table(sheet["table"])
        self.size = sheet["size"]


    def set(self, col, value):
        pass

if __name__ == "__main__":
    sheet = Sheet("example.json")
    print(sheet.table)
