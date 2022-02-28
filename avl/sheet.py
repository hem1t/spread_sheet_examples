#!/usr/bin/env python3

from bintrees import AVLTree
import json, re

def to_col(cell):
    cell = re.match(r"([a-z]+)(\d+)", cell.lower())
    if cell is None:
        return (0, 0)
    col, row = cell.group(1, 2)
    sum = 0
    order = 0
    for ch in col[::-1]:
        sum += (ord(ch) - 96) * (26 ** order)
        order += 1
    return sum - 1, int(row) - 1

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
        "Treats table as mutable"
        # size check
        (col, row) = to_col(col)
        ## update if greater
        if col > self.size["col"]:
            self.size["col"] = col
        if row > self.size["row"]:
            self.size["row"] = row
        # set
        self.table.insert(col, value)

    def insert(self, col, value):
        "Treats table as non-mutable, returns bool"
        # add if not avail
        if self.table.get(col) is not None:
            return False
        else:
            self.table.insert(col, value)
            return True

    def delete(self, col, value):
        if self.table.get(col) is not None:
            self.table.remove(col)

    def search(self, value):
        cells = []
        for item in self.table.items():
            if item[1] == value:
                cells.append(item[0])
        return cells

if __name__ == "__main__":
    sheet = Sheet("example.json")
    print(sheet.table)
