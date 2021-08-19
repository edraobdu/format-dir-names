import os
import re
import unidecode
import sys


def remove_chars(file_name, suffix=''):
    """
    Removes special characters and change diacritics by its natural char.

    Name(with special &$ chars).jpg -> Namewith special chars.jpg
    Folder($%Name)                  -> FolderName
    File.with.a.lot.of.dots.jpeg    -> Filewithalotofdots.jpeg
    """
    file_name_split = file_name.split('.')
    # The actual file name is the one before the last dot, which
    # is the file extension
    file_no_extension = ''.join(file_name_split[:-1]) if len(file_name_split) > 1 else file_name_split[0]
    new_str = re.sub('[^a-zA-Z0-9]', '', unidecode.unidecode(file_no_extension))
    new_str = '{}{}'.format(new_str, str(suffix) if suffix else '')
    return '.'.join([new_str, file_name_split[-1]]) if len(file_name_split) > 1 else new_str

def recursive_change_file_name(parent_dir, file_name=''):
    """
    Recursively change the name of the directories
    """
    file_dir = os.path.join(parent_dir, file_name)
    # print(file_dir)
    if file_name:
        file_exists = True
        suffix = 0
        while file_exists:
            new_dir_name = remove_chars(file_name, suffix)
            new_file_dir = os.path.join(parent_dir, new_dir_name)
            if os.path.isfile(new_file_dir) or os.path.isdir(new_file_dir):
                suffix += 1
                continue
            else:
                os.rename(file_dir, new_file_dir)
                print(new_dir_name, new_file_dir)
                file_exists = False
                file_dir = new_file_dir

    try:
        files_list = os.listdir(file_dir)
    except NotADirectoryError:
        # Is a file
        pass
    except FileNotFoundError as e:
        print('Error', e)
    else:
        for file in files_list:
            recursive_change_file_name(file_dir, file_name=file)


def main():
    """
    Call the script in your console with the absolute path
    to the folder you wanna start the change, like so:

    python3 remove_special_chars.py /path/to/the/folder
    """
    root_dir = sys.argv[1]
    recursive_change_file_name(root_dir)


if __name__ == '__main__':
    main()
