import os
import uuid


def rename_file(file_name):
    return uuid.uuid4().hex + os.path.splitext(file_name)[1]


def file_upload_path_generator(path):
    return lambda instance, file_name: os.path.join(path, rename_file(file_name))
