#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *
import ConfigParser
from pygetdata import *
import threading
import time

def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

def download_clicked():
	root2.deiconify()
	center(root2)
	t1 = threading.Thread(target=download).start()
	while Live:
		r2ll = "Загрузка |"
		time.sleep(0.5)
		r2ll = "Загрузка /"
		time.sleep(0.5)
		r2ll = "Загрузка -"
		time.sleep(0.5)
		r2ll = "Загрузка \\"
		time.sleep(0.5)

	content.set("")
	root2.withdraw()
	status.grid(row=2,column=0,columnspan=3)

def download():
	#print u"Клик! "+content.get()
	try:
		gd = getdata(port, path, content.get().encode('utf-8').strip())
		stext.set("\"" +gd.nname+ "\" передан в 1С")
	except Exception as inst:
		stext.set(inst)
	Live = False

def d_return_pressed(self):
	download_clicked()

def closea():
	root2.destroy()
	root.destroy()

config = ConfigParser.RawConfigParser()
config = ConfigParser.ConfigParser()
config.read('config.cfg')
mode = config.get('PyGetData', 'mode', 1)
port = config.get('PyGetData', 'port', 1)
path = config.get('PyGetData', 'path', 1)

root=Tk()
root2=Tk()
r2ll = ""
root.title("Загрузка из ТСД")
root2.title("Идет Загрузка..")
r2label = Label(root2, textvariable=r2ll, font=("Helvetica", 16))
r2label.grid(row=0,column=0)
root2.resizable(False, False)
#root2.geometry("+800+600")
root2.withdraw()

content = StringVar()
Live = True
stext = StringVar()
name = Entry(root, text="", textvariable=content, font=("Helvetica", 16))
name.bind("<Return>", d_return_pressed)
label = Label(root, text="Наименование: ", font=("Helvetica", 16))
status = Label(root, textvariable=stext)
buttondownload = Button(root, text="Загрузить", command=download_clicked, font=("Helvetica", 16))
label.grid(row=0,column=0)
name.grid(row=0,column=1,columnspan=2)
buttondownload.grid(row=1,column=0,columnspan=3)
root.resizable(False, False)
center(root)
root.protocol( "WM_DELETE_WINDOW", closea )
root.mainloop()
