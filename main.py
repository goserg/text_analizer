import time
import os
from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog
from typing import List

import text_manager
from ta_text import TaText
from author import Author

last_dir = os.getcwd()

album: List[TaText] = []


def update_list() -> None:
    list_box_for_texts.delete(0, tkinter.END)
    for i in album:
        list_box_for_texts.insert(tkinter.END, i)


def add() -> None:
    start = time.time()
    progress_bar.pack_forget()
    status_bar.pack_forget()
    progress_bar.pack(side=BOTTOM, fill=BOTH)
    status_bar.pack(side=BOTTOM, fill=BOTH)
    status_bar["text"] = "start processing"
    progress_bar['value'] = 0
    root.update_idletasks()

    global last_dir
    files = tkinter.filedialog.askopenfilenames(initialdir=last_dir,
                                                title="Select file",
                                                filetypes=(("txt files", "*.txt"), ("all files", "*.*")),
                                                )
    for filename in files:
        last_dir = filename.rsplit("/", 1)[0]
        if filename not in list_box_for_texts.get(0, tkinter.END):
            book = TaText.from_file(filename)
            book.title = filename.split("/")[-1].rstrip(".txt")
            album.append(book)
            status_bar["text"] = f"{book.title} processed"
            progress_bar.step(100 / len(files))
            root.update_idletasks()
    update_list()

    progress_bar.pack_forget()
    status_bar["text"] = f"processing complete in {time.time() - start: .1f} second(s)"


def del_text() -> None:
    album.pop(list_box_for_texts.curselection()[0])
    update_list()


def on_select(evt) -> None:
    try:
        w = evt.widget
        index = w.curselection()[0]
        author_entry.delete(0, END)
        author_entry.insert(0, album[index].author)
        title_entry.delete(0, END)
        title_entry.insert(0, album[index].title)
    except IndexError:
        pass


def generate() -> None:
    text_manager.generate_name_distribution_plot(book_list=album,
                                                 colors=["red",
                                                         "orange",
                                                         "yellow",
                                                         "green",
                                                         "lightblue",
                                                         "blue",
                                                         "violet",
                                                         ],
                                                 )


root = Tk()
root.geometry("600x300")

# RIGHT FRAME STUFF
right_frame = LabelFrame(root, text="Book")
right_frame.pack(side=RIGHT, fill=BOTH)

author_label = Label(right_frame, text="Author")
author_label.grid(row=0, column=0, columnspan=2, sticky="w")

author_entry = Entry(right_frame, width=40)
author_entry.grid(row=1, column=0, columnspan=2)

title_label = Label(right_frame, text="Title")
title_label.grid(row=2, column=0, columnspan=2, sticky="w")

title_entry = Entry(right_frame, width=40)
title_entry.grid(row=3, column=0, columnspan=2)

edit_btn = Button(right_frame, text="edit")
edit_btn.grid(row=4, column=0)


def save():
    index = list_box_for_texts.curselection()[0]
    album[index].title = title_entry.get()
    album[index].author = Author.from_string(author_entry.get())
    title_entry.delete(0, END)
    author_entry.delete(0, END)
    update_list()


save_btn = Button(right_frame, text="save", command=save)
save_btn.grid(row=4, column=1)

# LEFT FRAME STUFF
left_frame = Frame(root)
left_frame.pack(side=LEFT)

list_box_frame = Frame(left_frame)
list_box_frame.pack()

scrollbar = Scrollbar(list_box_frame)
scrollbar.pack(side=RIGHT, fill=BOTH)

list_box_for_texts = Listbox(list_box_frame, width=50, yscrollcommand=scrollbar.set)
list_box_for_texts.pack(side=LEFT)
list_box_for_texts.bind('<<ListboxSelect>>', on_select)

scrollbar.config(command=list_box_for_texts.yview)

buttons_frame = Frame(left_frame)
buttons_frame.pack()

add_text_btn = Button(buttons_frame, text="add", command=add)
add_text_btn.grid(row=0, column=0)

del_text_btn = Button(buttons_frame, text="delete", command=del_text)
del_text_btn.grid(row=1, column=0)

generate_diagram_btn = Button(buttons_frame, text="generate", command=generate)
generate_diagram_btn.grid(row=0, column=1)

progress_bar = Progressbar(left_frame)

status_bar = Label(left_frame, text="status")
status_bar.pack(side=BOTTOM, fill=BOTH)

root.mainloop()
