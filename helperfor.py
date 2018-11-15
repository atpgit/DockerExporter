# -*- coding: utf-8 -*-
import datetime

def Stringreplace(text):
 text = text.replace("İ", "I")
 text = text.replace("ı", "i")
 text = text.replace("ı", "i")
 text = text.replace("ı", "i")
 text = text.replace("Ğ", "G")
 text = text.replace("ğ", "g")
 text = text.replace("Ö", "O")
 text = text.replace("ö", "o")
 text = text.replace("Ü", "U")
 text = text.replace("ü", "u")
 text = text.replace("Ş", "S")
 text = text.replace("ş", "s")
 text = text.replace("Ç", "C")
 text = text.replace("ç", "c")
 text = text.replace(" ", "")
 return text.lower()


def GuidConverter(guidText):
 return guidText[2:][:-1]

def DockerIdSubString(dokcerUUID):
 return dokcerUUID[:12]


def findObjectInList(hubId,virtualHub):
     print(hubId.name)
     for item in virtualHub:
      if item.hubid==hubId.hubid:
        return True
            
def GetTime():
 return datetime.datetime.now()

def CalculateTime(start,end):
 delta = end - start
 return int(delta.total_seconds() * 1000)                  