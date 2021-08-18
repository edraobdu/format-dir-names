# REMOVE SPECIAL CHARS FROM DIRS

Removes special characters and change diacritics by its natural char on a specified folder and its children (no matter the depth).

    Name(with special &$ chars).jpg -> Namewith special chars.jpg
    Folder($%Name)                  -> FolderName
    File.with.a.lot.of.dots.jpeg    -> Filewithalotofdots.jpeg

Run the script from your terminal passing the absolute path to the folder you want to perform the changes:

```bash
python3 remove_special_chars.py /absolute/path/to/folder/
```