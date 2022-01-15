import os


def script(file_path, directory_path):
    file = os.path.join(os.path.dirname(os.path.abspath(file_path)), directory_path)
    content = ""
    with open(file) as f:
        content = f.read()

    return f"<script defer type='text/javascript'>{content}</script>"
