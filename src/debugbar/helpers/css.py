import os


def css(file_path, directory_path):
    file = os.path.join(os.path.dirname(os.path.abspath(file_path)), directory_path)
    content = ""
    with open(file) as f:
        content = f.read()

    return f"<style>{content}</style>"
