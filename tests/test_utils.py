import os


def get_html_doc(filename):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, f"fixtures/{filename}.html")
    with open(filename, mode="r", encoding="UTF-8") as file:
        return "\n".join(file.readlines())
