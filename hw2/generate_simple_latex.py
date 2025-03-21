from vnazarov_latex.latex_writer import generate_latext_table

with open('artifacts/result_table.tex', 'w') as file:
    result_table = generate_latext_table(
        [
            ['a', 'b', 'sum'],
            [1, 2, 3],
            [2, 3, 5],
            [6, 1, 7],
            [1, 4, 5]
        ]
    )
    file.write(result_table)
