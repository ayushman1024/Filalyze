import os
import pandas as pd
from shutil import copy2
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
# import filecmp

now = datetime.now()
timestamp = now.strftime("%d%b%Y%H%M%S")
print(timestamp)

gui = tk.Tk()
gui.withdraw()

root = filedialog.askdirectory(initialdir="/", title="Folder to Analyze")
fname = root.split(os.path.sep)[-1]

backup_pt_select = filedialog.askdirectory(initialdir="/",title="Select Path Backup Folder")
backup_pt = os.path.join(backup_pt_select, fname) + timestamp

root_uq = os.path.join(backup_pt, fname) + "_unique"
root_bk = os.path.join(backup_pt, fname) + "_backup"
allFiles_list = []
unqPath_list = []

def iterate(folder, base):
    #pass2
    file_dir = os.path.join(base, folder)
    dir_list = os.listdir(file_dir) #ls
    for f in dir_list:
        fpath = os.path.join(file_dir, f)
        if os.path.isdir(fpath):
            iterate(f, file_dir)
        else:
            if fpath in unqPath_list:
                destination_path = os.path.join(root_uq, file_dir.split(os.path.sep)[-1])
                dest = os.path.join(root_uq, os.path.join(file_dir.split(os.path.sep)[-1], f))
                if not os.path.exists(destination_path):
                    os.makedirs(destination_path)
                copy2(fpath, os.path.join(root_uq, dest))
                print("saved: " + os.path.join(root_uq, os.path.join(file_dir.split(os.path.sep)[-1], f)))

            else:
                destination_path = os.path.join(root_bk, file_dir.split(os.path.sep)[-1])
                dest = os.path.join(root_bk, os.path.join(file_dir.split(os.path.sep)[-1], f))
                if not os.path.exists(destination_path):
                    os.makedirs(destination_path)
                copy2(fpath, dest)
                os.remove(fpath)
                print("removed: ", fpath)

def generate_allFiles_list(folder, base):
    #pass1
    fdir = os.path.join(base, folder)
    dirlist = os.listdir(fdir)
    for f in dirlist:
        fpath = os.path.join(fdir, f)
        if os.path.isdir(fpath):
            generate_allFiles_list(f, fdir)
        else:
            allFiles_list.append([f, fpath, os.stat(fpath).st_size])

def execute():
    generate_allFiles_list(root, "") # recursively list all files found in "blist"

    #unique finder
    allFile_df = pd.DataFrame(allFiles_list, columns=['filename', 'location', 'size'])

    unqFiles_df = allFile_df.drop_duplicates(subset='size', keep='first')
    duplicate_count = allFile_df.shape[0] - unqFiles_df.shape[0]
    print("Duplicates ", duplicate_count)

    unqFiles_list = list(unqFiles_df.values)
    for _ in unqFiles_list:
        unqPath_list.append(_[1])
    iterate(root, "")

    #Report generation
    if len(fname)>20:
        report_fname = fname[:20] +"_"+timestamp+ ".xlsx"
    else:
        report_fname = fname +"_"+timestamp+ ".xlsx"

    allFile_df.to_excel(report_fname)
    print("Totals files ", len(allFiles_list))
