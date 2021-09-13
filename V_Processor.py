from V_RAM import *

class ON_FIRE(Exception):
   pass

class V_Processor():
   
   def __init__(self,ram):
      self.RAM = ram
      self.PC = 0
      self.INS = 0
      self.OP_CODE = 0
      self.SRC = 0
      self.DEST = 0
      self.registers = []
      for i in range(16):
         self.registers.append(0)
         
   def NEXT_OP(self):
      self.registers[0] = 0 #short term fix
      INS_WRD = self.RAM.get_value(self.PC)
      self.INS = (INS_WRD & 0xff00) >> 8
      self.SRC = (INS_WRD & 0x00f0) >> 4
      self.DEST = (INS_WRD & 0x000f)
      INST = {0x00:self.NOP,
             0xa0:self.LDA,
             0xb0:self.STR,
             0xc0:self.MOV,
             0x37:self.INC,
             0x38:self.DEC,
             0x30:self.ADD,
             0x31:self.SUB,
             0x35:self.ORR,
             0x34:self.AND,
             0x36:self.XOR,
             0x32:self.LSL,
             0x33:self.LSR,
             0x3F:self.CMP,
             0x45:self.JMP,
             0x55:self.CAL,
             0x65:self.RTN,
             0x43:self.JME,
             0x42:self.JML,
             0x44:self.JMG,
             0x41:self.JMC,
             0xee:self.CIN,
             0xe0:self.RIN,
             0xe1:self.HAD,
             0xe2:self.HTI,
             0xFF:self.HCF}
      if self.INS not in INST.keys():
         raise ValueError("OPCode "+str(hex(self.INS)) + " not found")
      else:
         INST[self.INS]()
         
   def print_status(self):
      print("PC:",hex(self.PC))
      print("SP:",hex(self.registers[0xe]))
      print("FR:",bin(self.registers[0xf]))
      INSL = {0x00:"NOP",0xa0:"LDA",0xb0:"STR",0xc0:"MOV",
              0x37:"INC",0x38:"DEC",0x30:"ADD",0x31:"SUB",
              0x35:"ORR",0x34:"AND",0x36:"XOR",0x32:"LSL",
              0x33:"LSR",0x3f:"CMP",0x45:"JMP",0x55:"CAL",
              0x43:"JME",0x42:"JML",0x44:"JMG",0x41:"JMC",
             0x65:"RTN"}
      INS_WRD = self.RAM.get_value(self.PC)
      print("INS:",INSL[(INS_WRD & 0xff00) >> 8])
      print("SRC:",hex((INS_WRD & 0x00f0) >> 4))
      print("DEST:",hex(INS_WRD & 0xf))
      print("NEXT WRD",hex(self.RAM.get_value(self.PC+1)),'\n')
      
   def NOP(self):
      self.PC += 1
      
   def Norm_ALU(self,result):
      if not ((0 > result ) or (result > 0xffff)):
         if result == 0:
            self.registers[0xf] |= 1
         return result
      if result < 0:
         result = 0x10000 + result
      else:
         result -= 0x10000
      self.registers[0xf] |= 2
      if result == 0:
         self.registers[0xf]|= 1
      return result
         
      
   def LDA(self):
      oprand = self.RAM.get_value(self.PC + 1)
      if oprand > 0x7fff:
         oprand = (oprand & 0x7fff) * - 1
      addr = self.registers[self.SRC] + oprand
      self.registers[self.DEST] = self.RAM.get_value(addr)
      self.PC += 2
      
   def STR(self):
      oprand = self.RAM.get_value(self.PC + 1)
      if oprand > 0x7fff:
         oprand = (oprand & 0x7fff) * - 1
      addr = self.registers[self.DEST] + oprand
      self.RAM.set_value(addr,self.registers[self.SRC])
      self.PC += 2
      
   def MOV(self):
      self.registers[self.DEST] = self.registers[self.SRC]
      self.PC += 1
      
   def INC(self):
      oprand = self.RAM.get_value(self.PC + 1)
      result = self.Norm_ALU(self.registers[self.SRC] + oprand)
      self.registers[self.DEST] = result
      self.PC += 2
      
   def DEC(self):
      oprand = self.RAM.get_value(self.PC + 1)
      result = self.Norm_ALU(self.registers[self.SRC] - oprand)
      self.registers[self.DEST] = result
      self.PC += 2
      
   def ADD(self):
      self.registers[self.DEST] = self.Norm_ALU(self.registers[self.SRC] + self.registers[self.DEST])
      self.PC += 1
   
   def SUB(self):
      self.registers[self.DEST] = self.Norm_ALU(self.registers[self.SRC] - self.registers[self.DEST])
      self.PC += 1
   
   def AND(self):
      self.registers[self.DEST] = self.Norm_ALU(self.registers[self.SRC] & self.registers[self.DEST])
      self.PC += 1
      
   def ORR(self):
      self.registers[self.DEST] = self.Norm_ALU(self.registers[self.SRC] | self.registers[self.DEST])
      self.PC += 1
   
   def XOR(self):
      self.registers[self.DEST] = self.Norm_ALU(self.registers[self.SRC] ^ self.registers[self.DEST])
      self.PC += 1
   
   def LSL(self):
      self.registers[self.DEST] = (self.registers[self.SRC] << 1) & 0xFFFF
      self.PC += 1
   
   def LSR(self):
      self.registers[self.DEST] = (self.registers[self.SRC] >> 1) & 0xFFFF
      self.PC += 1
   
   def CMP(self):
      x = self.registers[self.SRC]
      y = self.registers[self.DEST]
      self.registers[0xf] &= 0b11
      if x < y:
         self.registers[0xf] |= 0b100
      if x == y:
         self.registers[0xf] |= 0b1000
      if x > y:
         self.registers[0xf] |= 0b10000
      self.PC += 1
      
      
   def CAL(self):
      next_ins = self.PC + 2
      self.RAM.set_value(self.registers[0xe],next_ins)
      self.JMP()
      
   def JMP(self):
      oprand = self.RAM.get_value(self.PC + 1)
      if oprand > 0x7fff:
         oprand = (oprand & 0x7fff) * -1
      self.PC = self.PC + oprand
   
   def RTN(self):
      self.PC = self.RAM.get_value(self.registers[0xe])
   
   def JML(self):
      if (self.registers[0xf] & 0b100) != 0:
         self.JMP()
         return
      self.PC += 2
   
   def JMC(self):
      if (self.registers[0xf] & 0b010) != 0:
         self.JMP()
         return
      self.PC += 2
      
   def JMG(self):
      if (self.registers[0xf] & 0b10000) != 0:
         self.JMP()
         return
      self.PC += 2
      
   def JME(self):
      if (self.registers[0xf] & 0b1000) != 0:
         self.JMP()
         return
      self.PC += 2
      
   def RIN(self):
      raise NotImplementedError()
      
   def HAD(self):
      raise NotImplementedError()
      
   def CIN(self):
      raise NotImplementedError()
      
   def HTI(self):
      raise NotImplementedError()
      
   def HCF(self):
      raise ON_FIRE()
         
          


      