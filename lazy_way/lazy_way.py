#!/usr/bin/env python3

# Using JSON
#
import json, re


def separate(col_lens):
    line = ""
    for l in col_lens:
        line += "+" + ("-" * l)
    return line


def to_col(cell):
    cell = re.match(r"([a-z]+)(\d+)", cell.lower())
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


class Table:
    def __init__(self, file_path):
        with open(file_path, "r") as data:
            sheet = json.loads(data.read())
        self.table = sheet["table"]
        self.size = sheet["size"]

    def insert(self, cell, value):
        self.set(cell, value)

    def set(self, cell, value):
        self.table[cell] = value

    def delete(self, cell):
        self.table.delete(cell)

    def search(self, value):
        for cell in self.table.keys():
            if self.table[cell] == value:
                return cell

    ### Extras
    def __str__(self):
        # table start
        col_lens = self._max_lens()
        to_print = separate(col_lens) + "+\n"
        for row in range(self.size["row"]):
            for col in range(self.size["col"]):
                cell = to_cell(col, row)
                val = self.table.get(cell.upper()) or ""
                l = len(val)
                to_print += "| " + val + (" " * (col_lens[col] - l - 1))
            to_print += "|\n" + separate(col_lens) + "+\n"
        return to_print

    def _max_lens(self):
        column_widths = [3 for i in range(self.size["col"])]

        for cell in self.table.keys():
            col = to_col(cell)[0]
            column_widths[col] = max(column_widths[col], len(self.table[cell]) + 2)
        return column_widths

    def make_entry(self, entries):
        for col, val in entries:
            self.set(col, val)

    def save(self, file_path):
        with open(file_path, "w") as f:
            f.write(json.dumps({"size": self.size, "table": self.table}))


if __name__ == "__main__":
    table = Table("example.sheet")
    table.make_entry(
        [
            ("A2", "1/6/2020"),
            ("B2", "Pencil"),
            ("C2", "50"),
            ("D2", "0.5"),
            ("E2", "25"),
        ]
    )
    table.make_entry(
        [
            ("A3", "1/7/2020"),
            ("B3", "Pen"),
            ("C3", "25"),
            ("D3", "1"),
            ("E3", "25"),
        ]
    )
    table.make_entry(
        [
            ("A4", "1/9/2020"),
            ("B4", "Desk"),
            ("C4", "2"),
            ("D4", "50"),
            ("E4", "100"),
        ]
    )
    print(table)
    table.save("example.sheet2")
