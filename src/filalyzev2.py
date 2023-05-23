import os
import shutil
from collections import defaultdict
from openpyxl import Workbook

def find_duplicate_files(path, delete_duplicates):
    # dictionary to store file sizes and paths
    files = defaultdict(list)

    # traverse the folder and subfolders recursively
    for foldername, subfolders, filenames in os.walk(path):
        for filename in filenames:
            # get the full path of the file
            filepath = os.path.join(foldername, filename)

            # get the size of the file
            filesize = os.path.getsize(filepath)

            # add the file path to the dictionary using its size as key
            files[filesize].append(filepath)

    # create an Excel workbook and worksheet
    wb = Workbook()
    ws = wb.active

    # write the header row to the worksheet
    ws.append(['Filename', 'Path'])

    # create a backup folder for this run
    backup_folder = os.path.join(os.path.dirname(path), 'backup_duplicate_files')
    os.makedirs(backup_folder, exist_ok=True)

    # loop through the dictionary and find duplicate files
    for filesize, paths in files.items():
        # if there is more than one path for a given size, it means the file is a duplicate
        if len(paths) > 1:
            # get the original file path by sorting the paths list and selecting the first item
            paths.sort()
            original_path = paths.pop(0)

            # loop through the remaining paths and delete the files if required
            for path in paths:
                if delete_duplicates:
                    # move the duplicate file to the backup folder
                    backup_path = os.path.join(backup_folder, os.path.basename(path))
                    shutil.move(path, backup_path)
                else:
                    # add the duplicate file path to the worksheet
                    filename = os.path.basename(path)
                    ws.append([filename, path])

            # add the original file path to the worksheet
            filename = os.path.basename(original_path)
            ws.append([filename, original_path])

    # save the workbook to a file
    wb.save('duplicate_files.xlsx')

if __name__ == '__main__':
    # get the folder path and delete option from the user
    folder_path = input('Enter the folder path: ')
    delete_duplicates = input('Do you want to delete duplicates? (y/n): ').lower() == 'y'

    # find the duplicate files and generate the Excel report
    find_duplicate_files(folder_path, delete_duplicates)

    print('Duplicate files found and Excel report generated.')
    if delete_duplicates:
        print('Duplicate files have been moved to backup folder.')
