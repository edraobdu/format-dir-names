import os
import re
import unidecode
import sys


def remove_chars(file_name, suffix=None, is_folder=False):
    """
    Removes special characters and change diacritics by its natural char.

    Name(with special &$ chars).jpg -> Namewith special chars.jpg
    Folder($%Name)                  -> FolderName
    File.with.a.lot.of.dots.jpeg    -> Filewithalotofdots.jpeg
    """
    file_name_split = file_name.split('.')
    if is_folder:
        file_name_split = [''.join(file_name_split)]
    # The actual file name is the one before the last dot, which
    # is the file extension
    file_no_extension = ''.join(file_name_split[:-1]) if len(file_name_split) > 1 else file_name_split[0]
    new_str = re.sub('[^a-zA-Z0-9\s]', '', unidecode.unidecode(file_no_extension))
    new_str = '{}{}'.format(new_str, '' if not suffix else suffix)
    return '.'.join([new_str, file_name_split[-1]]) if len(file_name_split) > 1 else new_str

def recursive_change_file_name(parent_dir, file_name=''):
    """
    Recursively change the name of the directories
    """
    file_dir = os.path.join(parent_dir, file_name)
    print(file_dir)
    if file_name:
        dir_exists = True
        suffix = 0
        while dir_exists:
            # Before changing name
            new_dir_name = remove_chars(
                file_name,
                suffix=suffix,
                is_folder=os.path.isdir(file_dir)
            )
            new_file_dir = os.path.join(parent_dir, new_dir_name)
            if new_file_dir == file_dir:
                # this means this is the first time we found the file
                # and the changed name is the same as the original name
                # so we don't need to change it
                break
            if os.path.exists(new_file_dir):
                suffix += 1
            else:
                os.rename(file_dir, new_file_dir)
                file_dir = new_file_dir
                break

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
