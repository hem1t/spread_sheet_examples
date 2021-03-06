#!/usr/bin/env python3

from bintrees import AVLTree
import json, re

## function to create seperate lines while printing
def separate(col_lens):
    line = ""
    for l in col_lens:
        line += "+" + ("-" * l)
    return line

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

def to_cell(cl, row):
    col = ""
    cl += 1
    #### REUSING
    ### I know this might be badly written
    ### will fix it later
    while cl > 0:
        i = cl % 27
        if i == 0:
            cl -= 26
            continue
        col = chr(i + 96) + col
        cl = cl // 27
    return col + str(row + 1)


def _json_to_table(tree):
    table = AVLTree()
    for key in tree.keys():
        table.insert(key, tree[key])
    return table

class Sheet:
    def __init__(self, file_name):
        with open(file_name, "r") as file:
            sheet = json.loads(file.read())
        self.table = _json_to_table(sheet["table"])
        self.size = sheet["size"]

    def set(self, cell, value):
        "Treats table as mutable"
        # size check
        (col, row) = to_col(cell)
        ## are lengths not indices
        (col, row) = (col+1, row+1)
        ## update if greater
        if col > self.size["col"]:
            self.size["col"] = col
        if row > self.size["row"]:
            self.size["row"] = row
        # set
        self.table.insert(cell, value)

    def insert(self, col, value):
        "Treats table as non-mutable, returns bool"
        # add if not avail
        if self.table.get(col) is not None:
            return False
        else:
            self.set(col, value)
            return True

    def delete(self, col):
        if self.table.get(col) is not None:
            self.table.remove(col)

    def search(self, value):
        cells = []
        for item in self.table.items():
            if item[1] == value:
                cells.append(item[0])
        return cells

    ### Extras
    def __str__(self):
        # table start
        col_lens = self._max_lens()
        to_print = separate(col_lens) + "+\n"
        for row in range(self.size["row"]):
            for col in range(self.size["col"]):
                cell = to_cell(col, row)
                ### str is used for int values
                val = str(self.table.get(cell.upper()) or "")
                l = len(val)
                to_print += "| " + val + (" " * (col_lens[col] - l - 1))
            to_print += "|\n" + separate(col_lens) + "+\n"
        return to_print

    def _max_lens(self):
        column_widths = [3 for _ in range(self.size["col"])]
        for item in self.table.items():
            col = to_col(item[0])[0]
            column_widths[col] = max(column_widths[col], len(str(item[1])) + 2)
        return column_widths

    def make_entry(self, entries):
        for col, val in entries:
            self.set(col, val)

    def save(self, file_path):
        with open(file_path, "w") as f:
            f.write(json.dumps({"size": self.size, "table": dict(self.table)}))


if __name__ == "__main__":
    sheet = Sheet("example.json")
    print(sheet.table)
    sheet.make_entry([("A3", "Dummy_name"), ("B3", "N/A"), ("C3", "A"), ("E3", "N/A")])
    sheet.save("example1.json")
