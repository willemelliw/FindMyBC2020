import requests
from bs4 import BeautifulSoup
from requests_ntlm import HttpNtlmAuth
import subprocess
from tkinter import *


'''Set these before usage'''
bcFolder = 'C:\\WillemTemp\\broadcasts\\'
notepaddir = r'C:\Program Files (x86)\Notepad++\notepad++.exe'
'''
w= overwrite (only shows last bc)
a= append (shows latest bc after previous ones)
'''
mode = 'a'


window=Tk()
window.wm_title('Find My Broadcast v20.26')

#mixtest = 4330991


#scrape broadcast from Q-bay
def getBc(mix):
    url = 'http://vcatsvcg.gen.volvocars.net/qbay/base/vinviewer/VinVCC.asp'
    payload = {'VIN':mix,'BuildstatusID':'2'}

    cookie = requests.get('http://vcatsvcg.gen.volvocars.net/qbay/base/vinviewer/vinsummary.asp?', params=payload).cookies

    #requests.get(url, auth=HttpNtlmAuth('VCCNET\wvanouyt', '20Wvo=02'), cookies=cookie)
    r = requests.get(url, auth=HttpNtlmAuth('wvanouyt', '20Wvo=02'), cookies=cookie)
    raw = BeautifulSoup(r.text,'html.parser')
    all = raw.find_all('td')
    #print(raw)
    try:
        bcdata = all[0].text.replace('<br/>','')
        bcstate = all[2].text + ' = state mix below%\r'
        bcdate = all[1].text + ' = date bc below% \r'
        bc = ('\r' + str(bcdate) + str(bcstate) + str(bcdata) + '%\r')
    except IndexError:
        bc = 'error no result from Q-bay \r' + str(raw)

    return bc

#save broadcast to file
def saveBc(mix,bc, bcFolder,mode):
    dir = bcFolder
    bcFile = open(dir + mix.replace(" ","") + '.txt',mode)
    bcFile.write(str(bc))
    bcFile.close()
    t1.delete("1.0", END)
    t1.insert(END, 'File saved at '+dir)
    #print('File saved at ' +dir)

#input mixnummer
def mixIn():
    mix = e2_value.get().strip()
    try:
        int(mix) + 1
        return mix
    except ValueError:
        t1.delete("1.0", END)
        t1.insert(END, "non numeric")

def openfile(mix,notepaddir, bcFolder):
    dir = bcFolder
    b1 = (dir + mix.replace(" ","") + '.txt')
    subprocess.Popen([notepaddir, b1])


def loop():
    mix = mixIn()
    bc = getBc(mix)
    saveBc(mix, bc, bcFolder,mode)
    openfile(mix, notepaddir, bcFolder)


e1 = Label(window, text="Mixnummer?")
e1.grid(row=0, column=0)

e2_value = StringVar()
e2 = Entry(window, textvariable=e2_value)
e2.grid(row=0, column=1)

b1 = Button(window, text="Get BC", command=loop)
b1.grid(row=0, column=2)
#window.bind('<Return>', loop)

t1 = Text(window, height=2, width=42)
t1.grid(row=1, column=0, columnspan=3)


window.mainloop()













