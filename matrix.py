#!/usr/bin/env python3

# Defining A 2D Array
#
# +---+---+---+---+---+
# |A1 |B1 |C1 |D1 |E1 |
# +---+---+---+---+---+
# |A2 |B2 |C2 |D2 |E2 |
# +---+---+---+---+---+
# |A3 |B3 |C3 |D3 |E3 |
# +---+---+---+---+---+
# |A4 |B4 |C4 |D4 |E4 |
# +---+---+---+---+---+
#


class Sheet:
    def __init__(self, col, row):
        # what you're providing is considered as sizes
        # not index where it would end
        self.col = col
        self.row = row
        self.Columns = [[None for _ in range(row)] for _ in range(col)]

    def insert_col(self, at_col):
        # you can write like this
        # self.Columns.insert(at_col, [None for _ in range(self.row)])
        # But

        # Store and make entry
        temp = Columns[at_col]
        Columns[at_col] = [None for _ in range(self.row)]

        # Now shift
        for i in range(at_col + 1, self.col - 1):
            (Columns[i], temp) = (temp, Columns[i + 1])
        # Appending increases the size of array and then adds it
        Columns.append(temp)

    def insert_row(self, at_row):
        # can do
        # for column in self.Columns:
        #     column.insert(row, None)
        #
        for rows in self.Columns:
            temp, rows[at_row] = rows[at_row], None
            for i in range(at_row + 1, self.row - 1):
                rows[i], temp = temp, rows[i + 1]
            rows.append(temp)

    def delete_col(self, col):
        # can do
        # Columns.pop(col)

        for i in (col, self.col - 1):
            self.Columns[i] = self.Columns[i + 1]

    def delete_row(self, row):
        # can do
        # for column in self.Columns:
        #   column.pop(row)
        #
        for rows in self.Columns:
            for i in (row, self.row - 1):
                self.rows[i] = self.rows[i + 1]

    def search(self, value):
        for col in range(self.col):
            for row in range(self.row):
                if Columns[col][row] == value:
                    return (col, row)
