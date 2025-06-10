import os


def delete_files_in_folder(folder_path):
    """
    删除指定文件夹下的所有文件。

    :param folder_path: 文件夹的路径
    """
    if os.path.exists(folder_path):
        files = os.listdir(folder_path)
        for file in files:
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    else:
        print("文件夹不存在:", folder_path)

if __name__ == '__main__':
    delete_files_in_folder('./output')