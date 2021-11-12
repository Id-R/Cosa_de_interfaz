

#from tkinter import Tk, Frame, Button, Label, ttk
import tkinter
from tkinter import Tk, Frame, Button, Label
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#import math
#import valores
#import time
#from numpy import random
#from DFRobot_RaspberryPi_Expansion_Board import DFRobot_Expansion_Board_IIC as Board
""""
board = Board(1, 0x10)    # Select i2c bus 1, set address to 0x10

def board_detect():
  l = board.detecte()
  #print("Board list conform:")
  #print(l)
  
def print_board_status():
  if board.last_operate_status == board.STA_OK:
    print("board status: everything ok")
  elif board.last_operate_status == board.STA_ERR:
    print("board status: unexpected error")
  elif board.last_operate_status == board.STA_ERR_DEVICE_NOT_DETECTED:
    print("board status: device not detected")
  elif board.last_operate_status == board.STA_ERR_PARAMETER:
    print("board status: parameter error")
  elif board.last_operate_status == board.STA_ERR_SOFT_VERSION:
    print("board status: unsupport board framware version")

board_detect()    # If you forget address you had set, use this to detected them, must have class instance

while board.begin() != board.STA_OK:    # Board begin and check board status
    print_board_status()
    print("board begin faild")
    time.sleep(2)
print("board begin success")

board.set_adc_enable()

"""
fig, ax = plt.subplots(2)
#fig, ax = plt.subplots()
plt.title('Grafica Matplotlib')
#plt.grid(True)

fields, volts = [0,0], [0,0]
X,Y = [],[]
Maximo = 0
flujo,tiempo = [0,0], [0,0]
key = True
promedio = 0
hormiga = "hola"

#plt.xlabel("Eje x", size=16)
#plt.ylabel("Eje y", size=10)
ax[0].set_facecolor('black')
ax[0].xaxis.label.set_color('yellow')
ax[0].yaxis.label.set_color('yellow')
ax[0].tick_params(axis='x', colors='yellow')
ax[0].tick_params(axis='y', colors='yellow')
ax[1].tick_params(axis='x', colors='yellow')
ax[1].tick_params(axis='y', colors='yellow')
plt.xlim(0,60)
#ax[0].tick_params(axis='y', colors='yellow')

fig.patch.set_color('black')
#fig.set_facecolor('white')
enable = False
contar = 0
contar2 = 0
datito = 0
volumen =[0]
def animate(i):
    global fields, volts, X, Y
    global key
    global flujo, tiempo
    global enable, contar, contar2
    global datito, volumen
    contar2 +=1
    #volts.append(np.random.randint(-50, 50))
    val = board.get_adc_value(board.A0)
    vol = val * 3.3 / 4095
    time.sleep(0.1)
    print("vol: %f" % vol)
    volts.append(vol)
    #volts.append(np.sin(2*np.pi*i/30))
    plt.grid(True)
    fields = range(0, len(volts))
    #fields = [x / 10 for x in fields]
    flujo.append( flujo[-1] + np.random.randint(-3,3))
    tiempo = range(0, len(flujo))
    if volts[-1] < volts[-2] and key == True:
        X.append(fields[-2])
        Y.append(volts[-2])
        key = False
    elif volts[-1] > volts[-2]:
        key = True

    line, = ax[0].plot(fields, volts, c='y')
    volumen.append(.1*((abs(volts[-1])+abs(volts[-2]))/2))
    Grafica_2, = ax[1].plot(tiempo, flujo, c ='y')
    global promedio
    promedio = (str(round(np.mean(volts),2)))

    """
    ax[0].text(0.95, 0.01, "Promedio: " + promedio,
            verticalalignment='bottom', horizontalalignment='right',
            transform=ax[0].transAxes,
            color='gray', fontsize=15)
    """
    if len(volumen) > 59:
        volumen.pop(0)
    if volts[-1]<-.25 and volts[-2]>=-.25 and enable == False:
        enable = True
        contar += contar2
        X.append(fields[-2])
        Y.append(volts[-2])
    if enable == True:
        contar += 1

    if volts[-1]>.25 and volts[-2]<=.25 and enable == True:
        X.append(fields[-2])
        Y.append(volts[-2])
        datito = contar/10
        contar = 0
        contar2 = 0
        enable = False
    dos = ax[0].scatter(X, Y, c='r')
    if len(volts) > 60:
        volts.pop(0)
        #tres = tres[-1:-31]
        X = [i - 1 for i in X if i > 0]
        Y = Y[len(Y) - len(X):len(Y)]
    if len(flujo) > 10:
        flujo.pop(0)
    return line, dos, Grafica_2
    #return line, tres

def iniciar():
    plt.cla()
    canvas.close_event()
    global ani
    plt.xlabel("Tiempo (Decisegundos)", size=10)
    plt.ylabel("Presion", size=10)
    ani = animation.FuncAnimation(fig, animate, interval = 100,blit = True)
    canvas.draw()
    ventana.after(1000, update_gauge)
def pausar():
    ani.event_source.stop()

def reanudar():
    ani.event_source.start()

ventana = Tk()
#ventana.attributes('-zoomed',True)
ventana.state('zoomed')
ventana.geometry('642x535')
ventana.wm_title('Grafica matplotlib')
ventana.minsize(width = 642, height = 535)
#ventana.minsize(width = 800, height = 535)

frame = Frame(ventana, bg = 'black', bd = 3)
frame.pack(expand = 1, fill = 'both')

canvas = FigureCanvasTkAgg(fig, master = frame)
#canvas.get_tk_widget().pack(padx = 5, pady = 5, expand= 1, fill = 'both')
canvas.get_tk_widget().grid(row = 0, column =0,columnspan = 3, rowspan=4)
#Promedio = Label(frame,text = 'Promedio')
#Promedio.pack(side = tkinter.RIGHT)
boton_inicio=Button(frame,text ='Graficar Datos',width ='15',bg = 'purple4',fg = 'white',command = iniciar).grid(
    row = 4, column =0)

boton_pausa = Button(frame, text ='Pausar', width ='15', bg = 'salmon', fg = 'white',command=pausar).grid(
    row = 4, column =1)

boton_reanudar = Button(frame, text ='Reanudar', width ='15', bg = 'green', fg = 'white',command=reanudar).grid(
    row = 4, column =2)

#tortita = Label(frame,text =promedio).grid(row=0, column = 3)
#promedio.set("ERADASD")
cnvs = tkinter.Canvas(frame, width=400, height=300, bg = "black")
cnvs.grid(row=5, column=0, columnspan = 3)
aceptar = True
def update_gauge():
    global Maximo
    global aceptar
    if aceptar== True and len(volts)==60:
        aceptar = False
        iniciar()
        #print(Maximo,max(volts))
        plt.grid(True)
    global promedio
    if float(promedio) < 0:
        tortita = Label(frame, text=str(promedio) + " Kpa",
                        fg="red", bg="black", font="Helvetica 16 bold italic"
                        ).grid(row=0, column=4)
    else:
        tortita = Label(frame, text=str(promedio) + " Kpa",
                        fg="yellow", bg="black", font="Helvetica 16 bold italic"
                        ).grid(row=0, column=4)
    tortuga = Label(frame, text= str(round(max(volts),2)) + " Kpa",
        fg = "yellow" ,bg = "black",font = "Helvetica 16 bold italic").grid(
        row=1, column=4)
    otro = Label(frame, text=str(round(sum(volumen),2)) + " Kpa*segs",
                    fg="yellow", bg="black", font="Helvetica 16 bold italic").grid(
        row=2, column=4)
    eso = Label(frame, text=str(round(datito, 2)) + " segs.",
                 fg="yellow", bg="black", font="Helvetica 16 bold italic").grid(
        row=3, column=4)
    newvalue = np.random.randint(low_r,hi_r)
    cnvs.itemconfig(id_text,text = str(newvalue) + " %")
    # Rescale value to angle range (0%=120deg, 100%=30 deg)
    angle = 120 * (hi_r - newvalue)/(hi_r - low_r) + 30
    cnvs.itemconfig(id_needle,start = angle)
    ventana.after(1000, update_gauge)

Label(frame, text="Presion promedio:",
        fg="yellow", bg="black", font="Helvetica 16 bold italic"
        ).grid(row=0, column=3)
Label(frame, text="Presion maxima: ",
        fg="yellow", bg="black", font="Helvetica 16 bold italic"
        ).grid(row=1, column=3)
Label(frame, text="Volumen bajo la curva: ",
        fg="yellow", bg="black", font="Helvetica 16 bold italic"
        ).grid(row=2, column=3)

Label(frame, text="Tiempo de resp.: ",
        fg="yellow", bg="black", font="Helvetica 16 bold italic"
        ).grid(row=3, column=3)

coord = 10, 50, 350, 350  # define the size of the gauge
low_r = 0  # chart low range
hi_r = 100  # chart hi range

# Create a background arc with a number of range lines
numpies = 8
for i in range(numpies):
    cnvs.create_arc(coord, start=(i * (120 / numpies) + 30), extent=(120 / numpies), fill="white", width=1)

# add hi/low bands
cnvs.create_arc(coord, start=30, extent=120, outline="red", style="arc", width=40)
cnvs.create_arc(coord, start=30, extent=20, outline="green", style="arc", width=40)
cnvs.create_arc(coord, start=50, extent=20, outline="yellow", style="arc", width=40)
# add needle/value pointer
id_needle = cnvs.create_arc(coord, start=119, extent=1, width=7, outline = "blue")

# Add some labels
cnvs.create_text(180, 15, font="Times 20 italic bold", text="Niveles de oxígeno", fill="white")
cnvs.create_text(25, 140, font="Times 12 bold", text=low_r, fill="white")
cnvs.create_text(330, 140, font="Times 12 bold", text=hi_r,fill="white")
id_text = cnvs.create_text(170, 210, font="Times 15 bold")

#ventana.after(1000, update_gauge)

""""
boton_inicio=Button(frame,text ='Grafica Datos',width ='15',bg = 'purple4',fg = 'white',command = iniciar).pack(
    pady = 5, side = 'left', expand = 1
)
boton_pausa = Button(frame, text ='Pausar', width ='15', bg = 'salmon', fg = 'white',command=pausar).pack(
    pady = 5, side = 'left', expand = 1
)
boton_reanudar = Button(frame, text ='Reanudar', width ='15', bg = 'green', fg = 'white',command=reanudar).pack(
    pady = 5, side = 'left', expand = 1
)
#boton_reanudar['state'] = tkinter.DISABLED
"""
ventana.mainloop()
""""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl
import math
import tkinter

fields, volts = [0,0], [0,0]
X,Y = [],[]
key = True
a = 0
index = iter(range(20))
from numpy import random

def animate(i):
    global fields, volts, X, Y
    global key, a
    #a +=1
    volts.append(random.randint(-50, 50))
    #volts.append(math.sin(2*math.pi*a/90))
    fields = range(0, len(volts))
    if volts[-1]< volts[-2] and key == True:
        X.append(fields[-2])
        Y.append(volts[-2])
        key = False
    elif volts[-1] > volts[-2]:
        key = True

    plt.cla()
    plt.plot(fields, volts, c='c')
    plt.scatter(X,Y, c = 'r')

    if volts[-1] < 0:
        fig.patch.set_facecolor('blue')
    else:
        fig.patch.set_facecolor('purple')
    if len(volts)> 90:
        volts.pop(0)
        X = [i - 1 for i in X if i > 0]
        Y = Y[len(Y)-len(X):len(Y)]


fig = plt.figure(figsize=(8, 4))
plt.grid(True)
ax = fig.add_subplot(111)
ani = animation.FuncAnimation(fig, animate, frames=20, interval=100)
plt.show()
"""

"""
#mpl.rcParams['toolbar'] = 'None'
fig, ax = plt.subplots()

x = np.arange(0, 2*np.pi, .01)
line, = ax.plot(x, np.sin(x), color = 'yellow')


plt.grid(True)
#fig.patch.set_color('black')

ax.set_facecolor('black')
fig.set_facecolor('black')

plt.tick_params(left = True, right = False , labelleft = True ,
                labelbottom = False, bottom = True)

#cambian el nombre y tamaño de las etiquetas de los ejes
plt.xlabel("Eje x", size=16)
plt.ylabel("Eje y", size=10)

#cambian el color de las etiquetas de elos ejes
ax.xaxis.label.set_color('yellow')
ax.yaxis.label.set_color('blue')

#Estas cambian el color de los divisores
ax.tick_params(axis='x', colors='red')
ax.tick_params(axis='y', colors='red')

#Las funciones ax.spines cambian el color del marco
ax.spines['left'].set_color('white')
ax.spines['right'].set_color('white')
ax.spines['top'].set_color('white')
ax.spines['bottom'].set_color('white')

def animate(i):
    line.set_ydata(np.sin(x+i / 100))  # update the data.
    line.set_xdata(x)
    return line,


#plt.xlim(i-10,i+10)

#y = math.sin(x[-1] + i / 50)

    if y < 0:
        fig.patch.set_facecolor('blue')
    else:
        fig.patch.set_facecolor('white')
    

ani = animation.FuncAnimation(
    fig, animate, interval=20, blit=True, save_count=0)

# To save the animation, use e.g.
#
# ani.save("movie.mp4")
#
# or
#
# writer = animation.FFMpegWriter(
#     fps=15, metadata=dict(artist='Me'), bitrate=1800)
# ani.save("movie.mp4", writer=writer)

plt.show()
 """""