

def generate_latext_table(input: list[list]):
    column_format = " | ".join(["c"] * len(input[0]))

    latex_code = [
        "\\begin{table}[h]",
        "    \\centering",
        f"    \\begin{{tabular}}{{| {column_format} |}}",
        "    \\hline"
    ]

    for row in input:
        latex_code.append("    " + " & ".join(map(str, row)) + " \\\\ ")
        latex_code.append("    \\hline")

    latex_code.extend(
        [
            "    \\end{tabular}",
            "\\end{table}"]
    )

    return "\n".join(latex_code)


def generate_latex_image(image_path: str):
    return '\includegraphics{' + image_path + '}'
