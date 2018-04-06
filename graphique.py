import environment
from tkinter import *
import numpy as np
import tkinter
from datetime import datetime
import random
import time
from random import randint
from math import sqrt

Nods=[]
Distance=[]
first=True
last=False
HEIGHT=400
WIDTH=800
N_ants=5

root=Tk()                
canvas=Canvas(root,height=HEIGHT, width=WIDTH,bg='white') ## création du canvas
canvas.grid()


def draw_circle(event):
    global first,root,canvas ## on passe root et canves comme variable globale dans la fonction, ca permet de pouvoir y accéder de l'intérieur de la fonction
    x,y=event.x,event.y ## création de nouvelle variable
    if first==True:
        rond=canvas.create_oval(x-10,y-10,(x+10),(y+10),fill="red",width=2)
        first=False
    else:
        rond=canvas.create_oval(x-10,y-10,(x+10),(y+10),fill="grey",width=2)
    Nods.append([x,y])

def onclick_handler(event):
    global start
    Dist_temp=[]
    for i in Nods:
        Dist_temp.append([(event.x-i[0])**2+(event.y-i[1])**2])
    j=Dist_temp.index(min(Dist_temp))
    start = (Nods[j][0],Nods[j][1],j)

def onrelease_handler(event):
    global start
    if start is not None:
        x = start[0]
        y = start[1]
        jini=start[2]
        H=[]
        for i in range(len(Nods)):
            H.append([(event.x-Nods[i][0])**2+(event.y-Nods[i][1])**2])
        j=H.index(min(H))
        event.widget.create_line(x, y, Nods[j][0], Nods[j][1],dash=((4,4)),width=3)
        start = None
        Distance.append([jini,j,(Nods[j][0]-x)**2+(Nods[j][1]-y)**2])


canvas.bind('<Button-1>',draw_circle) 
canvas.bind("<Button-3>", onclick_handler)
canvas.bind("<ButtonRelease-3>", onrelease_handler)
canvas.pack()

root.mainloop() 
root.quit()


#########################################################################################

N=len(Nods)
Speed=3

Graph=np.zeros((N,N))
for i in Distance:
    Graph[i[0]][i[1]]=int(i[2])
    Graph[i[1]][i[0]]=int(i[2])
print(Graph)

dx=20
fenetre = Tk()
can = Canvas(fenetre,bg='dark grey',height=HEIGHT, width=WIDTH)
can.pack(side=LEFT,padx=5,pady=5)

rond=can.create_oval(Nods[0][0]-10,Nods[0][1]-10,(Nods[0][0]+10),(Nods[0][1]+10),fill="red",width=2)
for i in range(1,len(Nods)-1):
    rond=can.create_oval(Nods[i][0]-10,Nods[i][1]-10,(Nods[i][0]+10),(Nods[i][1]+10),fill="grey",width=2)
rond=can.create_oval(Nods[N-1][0]-10,Nods[N-1][1]-10,(Nods[N-1][0]+10),(Nods[N-1][1]+10),fill="green",width=2)
for i in range(len(Distance)):
    trait=can.create_line(Nods[Distance[i][0]][0], Nods[Distance[i][0]][1], Nods[Distance[i][1]][0], Nods[Distance[i][1]][1],dash=((4,4)),width=3)

number_ants = 100
evaporation_rate = 0.5
steps = 1000
environment = environment.Environment(Graph,number_ants,evaporation_rate)

def anime():
    environment.step()
    for i in range(0,number_ants):
        environment.population[i].move() 
    fenetre.after(5,anime)

def start():
    global flag
    flag=1
    for i in range(0,number_ants):
        environment.population[i].start()
    anime()

def stop():
    global flag
    flag=0
    for i in range(0,number_ants):
        environment.population[i].stop()

boutonGO = Button(fenetre, text='GO', width =3,command=start)
boutonGO.pack(side=BOTTOM)
boutonSTOP = Button(fenetre, text='STOP', width =3,command=stop)
boutonSTOP.pack(side=BOTTOM)
     
fenetre.mainloop()