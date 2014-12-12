#!/usr/bin/python
class Classe(object):

  mulher="Mulher de classe"
  
  def __init__(self):
    
    self.mulher="Mulher objeto"

  def __repr__(self):
    
     return self.mulher  

if __name__ == "__main__":

  mulher=Classe()
  print mulher

  print Classe.mulher

