import os


def get_file_name(path):
    if not os.path.isdir(path):
        return os.path.splitext(os.path.basename(path))[0].split(".")[0]


def get_file_extension(path):
    extensions = []
    copy_path = path
    while True:
        copy_path, result = os.path.splitext(copy_path)
        if result != '':
            extensions.append(result)
        else:
            break
    extensions.reverse()
    return "".join(extensions)
