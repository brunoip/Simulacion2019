from tkinter import *
import time
import random

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 200

gui = Tk()
gui.geometry(str(WINDOW_WIDTH)+"x"+str(WINDOW_HEIGHT))
gui.title("Python M/M/1 Test")
c = Canvas(gui, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
c.pack()

DIAMETER = 12
MARGIN_X = 200
MARGIN_Y = 40

QUEUE_SPACING = 2


#def key(event):
#    print "pressed", repr(event.char)


#print "Test animacion cola mm1"

largoLista = 3
tiempoTranscurrido = 0

while True:

    num= random.randint(1, 2)
    if num==2:
        largoLista=largoLista+1
    else:
        if largoLista>0:
            largoLista=largoLista-1

    tiempoTranscurrido = tiempoTranscurrido+1

    c.create_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, fill="white")

    c.create_text(20, 100, anchor=W, font="Purisa", text="Python M/M/1 Test")
    c.create_text(20, 120, anchor=W, font="Purisa", text="Bruno Pasquini")
    c.create_text(20, 140, anchor=W, font="Purisa", text="Clientes en cola: " + str(largoLista))
    c.create_text(20, 160, anchor=W, font="Purisa", text="Tiempo transcurrido: " + str(tiempoTranscurrido))

    c.create_oval(MARGIN_X - (DIAMETER + QUEUE_SPACING) * -1, MARGIN_Y-5,
                  MARGIN_X + DIAMETER - (DIAMETER + QUEUE_SPACING) * -1, MARGIN_Y-5 + DIAMETER, outline="black",
                  fill='green')
    c.create_rectangle(MARGIN_X-4 - (DIAMETER + QUEUE_SPACING) * -1, MARGIN_Y+2,
                       MARGIN_X+4 + DIAMETER - (DIAMETER + QUEUE_SPACING) * -1, MARGIN_Y + DIAMETER,outline="black", fill="brown")

    c.create_oval(MARGIN_X - (DIAMETER + QUEUE_SPACING) * -1, MARGIN_Y - 5+40,
                  MARGIN_X + DIAMETER - (DIAMETER + QUEUE_SPACING) * -1, MARGIN_Y - 5 + DIAMETER+40, outline="black",
                  fill='red')
    c.create_rectangle(MARGIN_X - 4 - (DIAMETER + QUEUE_SPACING) * -1, MARGIN_Y + 2+40,
                       MARGIN_X + 4 + DIAMETER - (DIAMETER + QUEUE_SPACING) * -1, MARGIN_Y + DIAMETER+40, outline="black",
                       fill="brown")

    if largoLista > 0:
        for i in range(largoLista, 0, -1):
            c.create_oval(MARGIN_X-(DIAMETER+QUEUE_SPACING)*i, MARGIN_Y+20, MARGIN_X+DIAMETER-(DIAMETER+QUEUE_SPACING)*i, MARGIN_Y+DIAMETER+20, outline="black", fill='blue')

    gui.update()
    time.sleep(0.5)

gui.title("First title")
gui.mainloop()