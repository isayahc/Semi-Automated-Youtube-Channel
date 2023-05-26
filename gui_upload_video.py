import tkinter as tk
from tkinter import filedialog
from argparse import Namespace

from src.utils.upload_video import get_authenticated_service, initialize_upload, validate_shorts
from googleapiclient.errors import HttpError

def browse_files(entry):
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files", "*.mp4*"), ("all files", "*.*")))
    entry.delete(0, tk.END)
    entry.insert(tk.END, filename)

def upload():
    options = Namespace(
        file=file_entry.get(),
        title=title_entry.get(),
        description=description_entry.get(),
        category=category_entry.get(),
        keywords=keywords_entry.get(),
        privacyStatus=privacy_status_var.get(),
        thumbnail=thumbnail_entry.get(),
        madeForKids=bool(made_for_kids_var.get()),
        youtubeShort=bool(youtube_short_var.get())
    )

    if options.youtubeShort:
        validate_shorts(options)

    youtube = get_authenticated_service()
    try:
        initialize_upload(youtube, options)
    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred:\n{e.content}')

root = tk.Tk()

file_label = tk.Label(root, text="Video file")
file_label.pack()
file_entry = tk.Entry(root)
file_entry.pack()
browse_button = tk.Button(root, text="Browse", command=lambda: browse_files(file_entry))
browse_button.pack()

title_label = tk.Label(root, text="Title")
title_label.pack()
title_entry = tk.Entry(root)
title_entry.insert(tk.END, 'Test Title')
title_entry.pack()

description_label = tk.Label(root, text="Description")
description_label.pack()
description_entry = tk.Entry(root)
description_entry.insert(tk.END, 'Test Description')
description_entry.pack()

category_label = tk.Label(root, text="Category")
category_label.pack()
category_entry = tk.Entry(root)
category_entry.insert(tk.END, '27')
category_entry.pack()

keywords_label = tk.Label(root, text="Keywords")
keywords_label.pack()
keywords_entry = tk.Entry(root)
keywords_entry.insert(tk.END, '')
keywords_entry.pack()

privacy_status_var = tk.StringVar(root)
privacy_status_var.set("private") 
privacy_status_option = tk.OptionMenu(root, privacy_status_var, "public", "private", "unlisted")
privacy_status_option.pack()

thumbnail_label = tk.Label(root, text="Thumbnail")
thumbnail_label.pack()
thumbnail_entry = tk.Entry(root)
thumbnail_entry.insert(tk.END, '')
thumbnail_entry.pack()
thumbnail_browse_button = tk.Button(root, text="Browse", command=lambda: browse_files(thumbnail_entry))
thumbnail_browse_button.pack()

made_for_kids_var = tk.BooleanVar(root)
made_for_kids_check = tk.Checkbutton(root, text='Made for Kids', variable=made_for_kids_var)
made_for_kids_check.pack()

youtube_short_var = tk.BooleanVar(root)
youtube_short_check = tk.Checkbutton(root, text='YouTube Shorts', variable=youtube_short_var)
youtube_short_check.pack()

upload_button = tk.Button(root, text="Upload", command=upload)
upload_button.pack()

root.mainloop()
