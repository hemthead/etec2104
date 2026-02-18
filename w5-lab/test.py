from table import Table

table = Table()

for i in range(0, 100):
    table.add_val((i + int(i/10)) % 10)
    if (i+1) % 10 == 0:
        table.finish_row()

table.print()
