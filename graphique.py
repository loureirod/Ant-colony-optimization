import environment as env
from tkinter import *
import numpy as np
import tkinter
from datetime import datetime
import random
import time
from random import randint
from math import sqrt
import tkinter.font as tkfont

################################### Hyperparameters ######################################
Nods=[]
Distance=[]
first=True
last=False
HEIGHT=400
WIDTH=800

nb_individuals = 10
nb_ants_max = 100
env_iterations = 100
genetic_iterations = 10
crossover_rate = 0.30
mutations_rate = 0.30


######################## First window : the one where we draw lines and circles ###########################

root=Tk()                
canvas=Canvas(root,height=HEIGHT, width=WIDTH,bg='white') ## creation of the canvas
canvas.grid()


def draw_circle(event):
    global first,root,canvas 
    x,y=event.x,event.y 
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

canvas.bind('<Button-1>',draw_circle) # creation of the buttons
canvas.bind("<Button-3>", onclick_handler)
canvas.bind("<ButtonRelease-3>", onrelease_handler)
canvas.pack()


##################################### Speed Scale #####################################################
def newvalue(x):
    global p
    p = x

scale2 = Scale(
    root,
    orient='horizontal',
    from_=1,
    to=10,
    length=1000,
    label='Speed',
    command=newvalue,
)
scale2.pack()
root.mainloop()



###################################  The first window is now closed  #######################################

try: #to know whether the value p exists (the value of the scale)
    a=p
except: #if not, we say that p=1
    p=1

N=len(Nods)
Graph=np.zeros((N,N))

def ConstructionGraph():
    for i in Distance:
        Graph[i[0]][i[1]]=int(sqrt(i[2])/int(p)) #the higher the speed is, the largest the step of every ant is  
        Graph[i[1]][i[0]]=int(sqrt(i[2])/int(p))

ConstructionGraph()



############################### To reproduce the exact graph we've drawn before ################################

fenetre = Tk()
can = Canvas(fenetre,bg='dark grey',height=HEIGHT, width=WIDTH)
can.pack(side=LEFT,padx=5,pady=5)
bold_font = tkfont.Font(family="Helvetica", size=12, weight="bold")


rond=can.create_oval(Nods[0][0]-12,Nods[0][1]-12,(Nods[0][0]+12),(Nods[0][1]+12),fill="red",width=2)
can.create_text(Nods[0][0]-15, Nods[0][1]-15,text='0',fill="purple",font=bold_font)
for i in range(1,len(Nods)-1):
    rond=can.create_oval(Nods[i][0]-12,Nods[i][1]-12,(Nods[i][0]+12),(Nods[i][1]+12),fill="grey",width=2)
    can.create_text(Nods[i][0]-15, Nods[i][1]-15,text='%s'%i,fill="purple",font=bold_font)
rond=can.create_oval(Nods[N-1][0]-12,Nods[N-1][1]-12,(Nods[N-1][0]+12),(Nods[N-1][1]+12),fill="green",width=2)
can.create_text(Nods[-1][0]-15, Nods[-1][1]-15,text='%s'%(len(Nods)-1),fill="purple",font=bold_font)
for i in range(len(Distance)):
    trait=can.create_line(Nods[Distance[i][0]][0], Nods[Distance[i][0]][1], Nods[Distance[i][1]][0], Nods[Distance[i][1]][1],dash=((4,4)),width=3)



######################################################### Genetic training of the population ####################################################

genetic = env.Genetic(nb_individuals,nb_ants_max,env_iterations,genetic_iterations,crossover_rate,mutations_rate,Graph)
environment = genetic.compute_best_individual()
genetic.print_best_individual_params()
active=False



####################################################### Gestion of the movment of the ants ######################################################

def anime():
    environment.step()
    for i in range(0,environment.number_ants):
        afficher(environment.population[i])
    if active==True:
    	fenetre.after(5,anime)

    
def start():
	global active
	active=True
	if hasattr(environment.population[0],'oval'): #hasattr() allows us to know if there is an oval attribute in population, so if start has aready been clicked one time
		pass
	else:
		for i in range(0,environment.number_ants):
			environment.population[i].x=Nods[environment.population[i].road[0]][0]
			environment.population[i].y=Nods[environment.population[i].road[0]][1]
			environment.population[i].oval=can.create_oval(environment.population[i].x-5,environment.population[i].y-5,environment.population[i].x+5,environment.population[i].y+5,width=2,fill="blue") #draw the initial corps of the ant
	anime()	

def stop():
	global active
	active=False
	print('Pheromone levels:')
	print(np.around(environment.pheromone,2))
	print('Best path:')
	print(environment.best_path())


def afficher(Anti):
	Anti.x=Nods[Anti.road[0]][0] + Anti.road_step/(Graph[Anti.road[0]][Anti.road[1]]+1)*(Nods[Anti.road[1]][0]-Nods[Anti.road[0]][0])
	Anti.y=Nods[Anti.road[0]][1] + Anti.road_step/(Graph[Anti.road[0]][Anti.road[1]]+1)*(Nods[Anti.road[1]][1]-Nods[Anti.road[0]][1])
	
	can.coords(Anti.oval,Anti.x-5,Anti.y-5,Anti.x+5,Anti.y+5)





############################################################ Start and stop buttons #####################################################

boutonGO = Button(fenetre, text='GO', width =20,command=start)
boutonGO.pack(side=BOTTOM)
boutonSTOP = Button(fenetre, text='STOP', width =20,command=stop)
boutonSTOP.pack(side=BOTTOM)
     
fenetre.mainloop()

