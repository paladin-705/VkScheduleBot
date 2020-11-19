command_list = []


class Command:
   def __init__(self):
       self.__keys = []
       self.description = ''
       command_list.append(self)

   @property
   def keys(self):
       return self.__keys

   @keys.setter
   def keys(self, arr):
       for k in arr:
           self.__keys.append(k.lower())

   def process(self, uid, key, data=""):
       pass