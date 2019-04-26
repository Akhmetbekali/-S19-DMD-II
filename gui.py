from tkinter import *
from q import *


class Example(Frame):

	def __init__(self, parent):
		Frame.__init__(self, parent, background="white")   
		self.parent = parent
		self.parent.title("Tables")
		self.pack(fill=BOTH, expand=1)
		self.centerWindow()
		self.showMain()

	def centerWindow(self):
		w = 500
		h = 600

		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()

		x = (sw - w)/2
		y = (sh - h)/2
		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


	def showMain(self):

		Button(self,width=500, height=5, text='users', 
             	        command=lambda: self.createQueriesWindow(queries.get('users'),"users")).pack(side="top")
		Button(self,width=500, height=5, text='students', 
             	        command=lambda: self.createQueriesWindow(queries.get('students'),"students")).pack(side="top")
		Button(self,width=500, height=5, text='grades', 
             	        command=lambda: self.createQueriesWindow(queries.get('grades'),"grades")).pack(side="top")


	def refillText(self,text,new):
		text.delete(1.0, 100.0)
		text.insert(1.0,new)

	def createQueriesWindow(self, q,title):
		t = Toplevel(self)
		t.wm_title(title)
		button = Button(t, width=500, height=5, text='Select', 
             	                 command=lambda: self.createQueryWindow(q,'Select', select))
		button.pack(side="top")
		button = Button(t, width=500, height=5, text='Insert', 
             	                 command=lambda: self.createQueryWindow(q,'Insert', insert))
		button.pack(side="top")
		button = Button(t, width=500, height=5, text='Delete', 
             	                 command=lambda: self.createQueryWindow(q,'Delete', delete))
		button.pack(side="top")
		button = Button(t, width=500, height=5, text='Update', 
             	                 command=lambda: self.createQueryWindow(q,'Update', update))
		button.pack(side="top")




	def createQueryWindow(self, q, title, f):

		t = Toplevel(self)
		t.wm_title(title)

		entries = {}
		row = 0

		for i in q.get('pk'):
			label = Label(t,text=i+'*:')
			label.grid(row=row, column=0, sticky="w")
			string = StringVar()
			entry = Entry(t, textvariable=string)
			entry.grid(row=row,column=1, padx=5, pady=5)
			entries.update({i: string})
			row+=1
		if title == 'Insert' or title == 'Select':
			for i in q.get('unic'):
				label = Label(t,text=i+'*:')
				label.grid(row=row, column=0, sticky="w")
				string = StringVar()
				entry = Entry(t, textvariable=string)
				entry.grid(row=row,column=1, padx=5, pady=5)
				entries.update({i: string})
				row+=1
		if title == 'Insert' or title == 'Update' or title == 'Select' :
			for i in q.get('fields'):
				label = Label(t,text=i+':')
				label.grid(row=row, column=0, sticky="w")
				string = StringVar()
				entry = Entry(t, textvariable=string)
				entry.grid(row=row,column=1, padx=5, pady=5)
				entries.update({i: string})
				row+=1

		text = Text(t, height=5, width=65, borderwidth=2, relief="groove")
		text.grid(row=row,column=0, padx=5, pady=5, columnspan=2)

		button = Button(t, text="Select", 
             	                 command=lambda: self.refillText(text, f(entries,q)))
		button.grid(row=row+1,column=1, padx=5, pady=5)

		# print(entries)
		
		# label1 = Label(t,text="User Type:")
		# label1.grid(row=0, column=0, sticky="w")
		# entry1 = Entry(t)
		# entry1.grid(row=0,column=1, padx=5, pady=5)

		# label2 = Label(t,text="Sername:")
		# label2.grid(row=1, column=0, sticky="w")
		# entry2 = Entry(t)
		# entry2.grid(row=1,column=1, padx=5, pady=5)

		# label3 = Label(t,text="Name:")
		# label3.grid(row=2, column=0, sticky="w")
		# entry3 = Entry(t)
		# entry3.grid(row=2,column=1, padx=5, pady=5)

		

		


def kek():
	print('kek')
 
def main():
	root = Tk()
	ex = Example(root)
	root.mainloop()  
 
if __name__ == '__main__':
    main()