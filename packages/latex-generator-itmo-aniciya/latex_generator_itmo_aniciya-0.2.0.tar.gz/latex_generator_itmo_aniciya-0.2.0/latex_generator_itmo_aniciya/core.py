import os
from string import Template
from typing import List, Any

from .utils import get_date, get_username

TEMPLATE = Template(r"""\documentclass{article}
\usepackage{graphicx}
\title{python}
\author{ $user }
\date{ $date }
\begin{document}
$content
\end{document}""")
IMAGE_TEMPLATE = Template(r"""\begin{figure}
    \centering
    \includegraphics[width=1\linewidth]{ $path }
    \caption{ $filename }
    \label{fig:enter-label}
\end{figure}""")


def generate_table(table: List[List[Any]]) -> str:
    """
    Generates a latex table from the given list of rows.

    :param table: 2d list of cells
    :return: latex document with table
    """
    count_columns = max(map(len, table))  # максимальное количество столбцов
    table_str = [
        list(map(str, row)) + [''] * (count_columns - len(row))  # заполняем пустыми строками остальные столбцы
        for row in table
    ]

    content = r'''\begin{table}
    \centering
    \begin{tabular}{''' + '|c' * count_columns + '|}\n'''
    for row in table_str:
        content += '        \\hline \n'
        content += '        ' + ' & '.join(row) + ' \\\\\n'
    content += r'''         \hline
    \end{tabular}
\end{table}'''
    return TEMPLATE.substitute(
        date=get_date(),
        user=get_username(),
        content=content
    )


def generate_image(filename: str) -> str:
    """
    Generates a latex document with the given image.

    :param filename: filename of the image
    :return: latex document with image
    """
    abs_path = os.path.abspath(filename).replace('\\', '/')
    only_filename = os.path.basename(filename)
    return TEMPLATE.substitute(
        date=get_date(),
        user=get_username(),
        content=IMAGE_TEMPLATE.substitute(
            path=abs_path,
            filename=only_filename
        )
    )
