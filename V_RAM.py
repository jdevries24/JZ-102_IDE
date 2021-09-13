import keyboard

class v_ram:
   
   def __init__(self,ram = None):
      self.r_array = []
      if ram == None:
         for i in range(0x10000):
            self.r_array.append(0)
      else:
         self.r_array = ram
      self.screen_que = []
      self.keyboard_que = []

   def set_value(self,address,value):
      self.r_array[address] = value
      if address == 0xffff:
         self.screen_que.append(chr(value))
      if address == 0xfffe:
         self.keyboard_que = self.keyboard_que[1:]
   
   def get_value(self,address):
      if address != 0xfffe:
         return int(self.r_array[address])
      else:
         if len(self.keyboard_que) > 0:
            value = self.keyboard_que[0]
            return value
         return 0

   def set_range(self,new_values,start_point,end_point):
      self.r_array = self.r_array[:start_point] + new_values + self.r_array[end_point:] 
      

class hex_file:
   
   def __init__(self,file_name):
      self.f_name = file_name
      
   def niev_read(self):
      f = open(self.f_name,'r')
      hex_str = f.read()
      if "v2.0 raw" not in hex_str:
         raise Format_Error("needs to be hex_file")
      hex_str = hex_str.replace("v2.0 raw\n","")
      hex_str = hex_str.replace("\n","")
      hex_list = hex_str.split(" ")
      new_ram = []
      for hex_words in hex_list:
         try:
            new_ram.append(int(hex_words,16))
         except:
            print("Unknown number: ",hex_words)
      return new_ram
   
   def read(self):
      f = open(self.f_name,'r')
      hex_str = f.read()
      if "v2.0 raw" not in hex_str:
         raise Format_Error("needs to be hex_file")
      hex_str = hex_str.replace("v2.0 raw\n","")
      hex_str = hex_str.replace("\n","")
      hex_list = hex_str.split(" ")
      new_ram = []
      for hex_words in hex_list:
         repeats = 1
         if "*" in hex_words:
            hex_words = hex_words.split("*")
            repeats = int(hex_words[1])
            hex_words = hex_words[0]
         for i in range(repeats):
            try:
               new_ram.append(int(hex_words,16))
            except:
               print("Unknown number: ",hex_words)
      for i in range(0x10000 - len(new_ram)):
         new_ram.append(0)
      return new_ram
            
