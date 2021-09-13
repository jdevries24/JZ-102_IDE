import tkinter as tk
import tkinter.filedialog as tkfd
from front_end import *
from V_comp import *
import os.path

class IDE_Main:
   
   #Up here are the construction methods 
   
   def __init__(self,master):
      self.master = master
      self.working_file = None
      self.master.config(menu=self.create_menu_bar())
      self.create_text_box()
      self.indent_level = 0
      self.par_stack = []
      self.in_string = False
      self.previous_key = "None"
      
   def create_menu_bar(self):
      menubar = tk.Menu(self.master)
      fm = tk.Menu(menubar,tearoff=0)
      fm.add_command(label="New",command=self.nothing)
      fm.add_command(label="Open",command=self.open)
      fm.add_command(label="Save",command=self.save)
      fm.add_command(label="Save as",command=self.save_as)
      menubar.add_cascade(label="File",menu=fm)
      rm = tk.Menu(menubar,tearoff=0)
      rm.add_command(label="Compile/Run",command=self.compandrun)
      rm.add_command(label="Run",command=self.run)
      rm.add_command(label="Debug",command=self.nothing)
      menubar.add_cascade(label="Run",menu=rm)
      menubar.add_command(label="Compile",command=self.compile)
      return menubar
   
   def create_text_box(self):
      self.text = tk.Text(self.master,tabs = "1c")
      self.text.pack(side="left",expand=True,fill="both")
      self.sbar = tk.Scrollbar()
      self.sbar.pack(side="right",fill=tk.Y)
      self.sbar.config(command=self.text.yview)
      self.text.config(yscrollcommand=self.sbar.set)
      self.text.bind("<Key>",self.handle_key)
      
   #everything for handeling the box
   def handle_key(self,key):
      self.text.config(state=tk.NORMAL)
      if key.char == "\r":
         self.text.insert(tk.INSERT,"\n")
         for i in range(self.count_indent()):
            self.text.insert(tk.INSERT,"\t",'a')
         self.text.config(state=tk.DISABLED)
   
   def count_indent(self):
      indent_level = 0
      for char in self.text.get("1.0",tk.INSERT):
         if char == "}":
            indent_level -=1
         if char == "{":
            indent_level += 1
      if indent_level < 0:
         return 0
      return indent_level
   
   def nothing(self):
      pass
   
   #menu options
   
   def open(self):
      self.working_file = tkfd.askopenfilename(filetypes = [("C File",".c")])
      print(self.working_file)
      self.text.delete('1.0',tk.END)
      f = open(self.working_file,'r')
      fstr = f.read()
      f.close()
      self.text.insert(tk.INSERT,fstr,'a')
      
   def save(self):
      if self.working_file == None:
         self.save_as()
         return
      file_str = self.text.get("1.0",tk.END)
      f = open(self.working_file,'w')
      f.write(file_str)
      f.close()
      
   def save_as(self):
      self.working_file = tkfd.asksaveasfilename(filetypes=[("C File",".c")])
      if self.working_file != None:
         self.save()
         
   def compandrun(self):
      self.compile()
      self.run()
         
   def compile(self):
      print("compileing")
      if self.working_file == None:
         return False
      self.save()
      wd = str(self.working_file)[:-2]
      fe = front_end(wd)
      fe.run()
      return True
   
   def run(self):
      if self.working_file == None:
         return 
      rf = self.working_file[:-2] + ".h"
      if not os.path.isfile(rf):
         if not self.compile():
            return
      V = V_COMP(rf)
      V.run()
      

      

if __name__ == "__main__":
   root = tk.Tk()
   IDE = IDE_Main(root)
   root.mainloop()