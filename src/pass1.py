import os
import pandas as pd
from shutil import copy2
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
# import filecmp

k = open("test.txt",'w+')
now = datetime.now()
timestamp = now.strftime("%d%b%Y%H%M%S")
print(timestamp)

gui = tk.Tk()
gui.withdraw()

root = filedialog.askdirectory(initialdir="/",title="Folder to Analyze")
fname = root.split(os.path.sep)[-1]

backup_pt_select = filedialog.askdirectory(initialdir="/",title="Select Path Backup Folder")
backup = os.path.join(backup_pt_select, fname) + timestamp

root_uq = os.path.join(backup, fname) + "_unique"
root_bk = os.path.join(backup, fname) + "_backup"
blist = []
bqlistpath = []

def iterate(folder, base):
    fdir = os.path.join(base, folder)
    dirlist = os.listdir(fdir)
    for f in dirlist:
        fpath = os.path.join(fdir, f)
        if os.path.isdir(fpath):
            iterate(f, fdir)
        else:
            if fpath in bqlistpath:
                destF = os.path.join(root_uq, fdir.split(os.path.sep)[-1])
                dest = os.path.join(root_uq, os.path.join(fdir.split(os.path.sep)[-1], f))
                if not os.path.exists(destF):
                    os.makedirs(destF)
                copy2(fpath, os.path.join(root_uq, dest))
                print("saved: " + os.path.join(root_uq, os.path.join(fdir.split(os.path.sep)[-1], f)))

            else:
                destF = os.path.join(root_bk, fdir.split(os.path.sep)[-1])
                dest = os.path.join(root_bk, os.path.join(fdir.split(os.path.sep)[-1], f))
                if not os.path.exists(destF):
                    os.makedirs(destF)
                copy2(fpath, dest)
                os.remove(fpath)
                print("removed: ", fpath)

# def findDups(books: pd.DataFrame):
#     books[books.duplicated(['size'])]
#     pass

def getBookList(folder, base):
    fdir = os.path.join(base, folder)
    dirlist = os.listdir(fdir)
    for f in dirlist:
        fpath = os.path.join(fdir, f)
        if os.path.isdir(fpath):
            getBookList(f, fdir)
        else:
            blist.append([f, fpath, os.stat(fpath).st_size])

def execute():
    getBookList(root, "") # recursively list all files found in "blist"
    books = pd.DataFrame(blist, columns=['filename', 'location', 'size'])
    if len(fname)>20:
        report_fname = fname[:20] +"_"+timestamp+ ".xlsx"
    else:
        report_fname = fname +"_"+timestamp+ ".xlsx"
    books.to_excel(report_fname)
    print("Totals files ", len(blist))

    books_unq = books.drop_duplicates(subset='size', keep='first')
    print("Duplicates ", books.shape[0] - books_unq.shape[0])

    bqlist = list(books_unq.values)
    for bq in bqlist:
        bqlistpath.append(bq[1])
    iterate(root, "")