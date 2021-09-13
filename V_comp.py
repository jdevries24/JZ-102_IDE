from V_Processor import *
from V_RAM import *
import tkinter as tk
from os import getcwd

class V_COMP():
   
   def __init__(self,filename):
      self.root = tk.Tk()
      self.build_gui()
      hf = hex_file(filename)
      self.ram = v_ram(hf.read())
      self.CPU = V_Processor(self.ram)
      self.root.after(1000,self.exacute)
      
   def build_gui(self):
      self.terminal = tk.Text(self.root,bg="black",fg="white",tabs = "1c")
      self.terminal.pack(side="left",expand=True,fill="both")
      self.sbar = tk.Scrollbar(self.root)
      self.sbar.pack(side="right",fill=tk.Y)
      self.sbar.config(command=self.terminal.yview)
      self.terminal.config(yscrollcommand=self.sbar.set)
      self.root.bind("<Key>",self.handle_key)
      
   def handle_key(self,key):
      if len(key.char) < 1:
         return
      if ord(key.char) != 0xd:
         self.ram.keyboard_que.append(ord(key.char))
      else:
         self.ram.keyboard_que.append(0xa)
      print(hex(ord(key.char)))
      
   
   def exacute(self):
      try:
         for i in range(100):
            self.CPU.NEXT_OP()
            if len(self.ram.screen_que) != 0:
               self.update_terminal()
               break
         self.root.after(1,self.exacute)
      except ON_FIRE:
         self.terminal.config(state=tk.NORMAL)
         self.terminal.insert(tk.INSERT,'\nthe cpu is on fire')
         self.terminal.config(state=tk.DISABLED)
         self.terminal.yview_moveto('1.0')
         
   def update_terminal(self):
      self.terminal.config(state=tk.NORMAL)
      self.terminal.insert(tk.INSERT,self.ram.screen_que[0])
      self.ram.screen_que = self.ram.screen_que[1:]
      self.terminal.config(state=tk.DISABLED)
      self.terminal.yview_moveto('1.0')
      
      
   def run(self):
      self.root.mainloop()