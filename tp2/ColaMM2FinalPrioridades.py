import random
import math
import matplotlib.pyplot as plt
import time
from tkinter import *
from tp2.ClientController import ClientController
from tp2.simpleServerRev2 import simpleServerRev2

array_delay_in_queue_by_client = []
array_number_in_queue_by_client = []
array_time_in_system = []

Q_LIMIT = 100
BUSY = 1
IDLE = 0

EVENT_ARRIVE = 1
EVENT_DEPART_1 = 2
EVENT_DEPART_2 = 3

queue_type = 0

QUEUE_FIFO = 0
QUEUE_PRIORITIES = 1
QUEUE_LIFO = 2

next_event_type = 1
num_custs_delayed = 0
num_delays_required = 4
num_events = 0
num_in_q = 0
server_status_1 = 0
server_status_2 = 0

area_num_in_q = 0.0
area_server_status_1 = 0.0
area_server_status_2 = 0.0
mean_interarrival = 0.0
mean_service = 0.0
simulation_time = 0.0
time_arrival = []
time_last_event = 0.0
time_next_event = []
total_of_delays = 0.0

# Variables for the animation
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 250



DIAMETER = 12
MARGIN_X = 200
MARGIN_Y = 40

QUEUE_SPACING = 2

# Data for the second stage
miServer1 = simpleServerRev2()
miServer1.serverName = "1"
miServer1.initialize("1", 0, .6, True)

miServer2 = simpleServerRev2()
miServer2.serverName = "2"
miServer2.initialize("2", 0, .6, True)

miServer3 = simpleServerRev2()
miServer3.serverName = "3"
miServer3.initialize("3", 0, .6, True)

array_arrival_times = []

# Run the simulation
def initialize():

    # Initialize the simulation clock.
    global simulation_time
    simulation_time = 0.0

    # Initialize the state variables.
    global server_status_1
    server_status_1 = IDLE
    global server_status_2
    server_status_2 = IDLE

    global num_in_q
    num_in_q = 0
    global time_last_event
    time_last_event = 0.0

    # Initialize the statistical counters.
    global num_custs_delayed
    num_custs_delayed = 0
    global total_of_delays
    total_of_delays = 0.0
    global area_num_in_q
    area_num_in_q = 0.0
    global area_server_status_1
    area_server_status_1 = 0.0
    global area_server_status_2
    area_server_status_2 = 0.0


    # Initialize event list.
    # Since no customers are present, the departure(service completion) event is eliminated from consideration.
    global time_next_event
    del time_next_event[:]
    time_next_event.append(0)
    time_next_event.append(0)
    time_next_event.append(0)
    time_next_event.append(0)

    time_next_event[EVENT_ARRIVE] = simulation_time + expon(mean_interarrival)
    time_next_event[EVENT_DEPART_1] = 1.0e+30
    time_next_event[EVENT_DEPART_2] = 1.0e+30

    return;


def timing():

    global num_events
    global time_next_event
    global next_event_type
    global simulation_time

    min_time_next_event = 1.0e+29
    next_event_type = 0

    # Determine the event type of the next even to occur.
    for i in range(1, 4):
        if time_next_event[i] < min_time_next_event:
            min_time_next_event = time_next_event[i]
            next_event_type = i

    # Check to see whether the event list is empty.
    if next_event_type == 0:
        # The event list is empty, so stop the simulation.
        print("The event list is empty at time:", simulation_time)
        exit()

    # The event list is not empty, so advance the simulation clock.
    simulation_time = min_time_next_event

    return


def arrive():

    global time_next_event
    global simulation_time
    global mean_interarrival
    global server_status_1
    global server_status_2

    global total_of_delays
    global time_arrival
    global num_in_q
    global num_custs_delayed
    delay = 0.0

    # Schedule next arrival. Un arribo genera otro arribo
    arriavalTime = simulation_time + expon(mean_interarrival)
    time_next_event[EVENT_ARRIVE] = arriavalTime
    array_arrival_times.append(arriavalTime)
    ClientController().registerArrival(arriavalTime)

    # Check to see whether server is busy.
    if (server_status_1 == BUSY and server_status_2 == BUSY):
        # Both servers are busy, so increment number of customers in queue.
        num_in_q = num_in_q+1

        # Check to see whether an overflow condition exists.
        if num_in_q > Q_LIMIT:
            # The queue has overflowed, so stop the simulation.
            print("Overflow of the array time_arrival at ", simulation_time, " time")
            exit(2)

        # There is still room in the queue,
        # so store the time of arrival of the arriving customer at the(new) end of time_arrival.

        # time_arrival[num_in_q] = simulation_time
        time_arrival.append(simulation_time)
    else:

        # One of the servers or both are idle, so arriving customer has a delay of zero.
        # (The following two statements are for program clarity and do not affect the results of the simulation).
        delay = 0.0
        total_of_delays += delay

        # Increment the number of customers delayed, and make server busy.
        num_custs_delayed = num_custs_delayed + 1
        departureTime = simulation_time + expon(mean_service)
        ClientController().registerFirstDepartureTime(simulation_time, departureTime, "a")

        if server_status_1 == IDLE and server_status_2 == BUSY:
            server_status_1 = BUSY
            # Schedule a departure(service completion).
            time_next_event[EVENT_DEPART_1] = departureTime

        if server_status_1 == BUSY and server_status_2 == IDLE:
            server_status_2 = BUSY
            # Schedule a departure(service completion).
            time_next_event[EVENT_DEPART_2] = departureTime

        if server_status_1 == IDLE and server_status_2 == IDLE:
            # Both servers are free, flip a coin to see who take the customer
            if bool(random.getrandbits(1)):
                server_status_1 = BUSY
                # Schedule a departure(service completion).
                time_next_event[EVENT_DEPART_1] = departureTime
            else:
                server_status_2 = BUSY
                # Schedule a departure(service completion).
                time_next_event[EVENT_DEPART_2] = departureTime
    return


def depart_1():

    global num_custs_delayed
    global num_in_q
    global time_arrival
    global server_status_1
    global total_of_delays

    delay = 0.0

    # send The customer to the second stage
    sendCustomerToSecondStage(simulation_time + expon(mean_service))

    # Check to see whether the queue is empty.
    if num_in_q == 0:
        # The queue is empty, make the server idle and eliminate the departure event from consideration
        server_status_1 = IDLE
        time_next_event[2] = 1.0e+30
    else:
        # The queue is nonempty, so decrement the number of customers.
        num_in_q = num_in_q - 1

        # Compute the delay of the customer who is beginning service and update the total delay accumulator.
        delay = simulation_time - time_arrival[len(time_arrival)-1]
        total_of_delays += delay

        # Increment the number of customers delayed, and schedule departure.
        num_custs_delayed = num_custs_delayed + 1

        departure_time = simulation_time + expon(mean_service)
        time_next_event[EVENT_DEPART_1] = departure_time
        ClientController().registerFirstDepartureTime(time_arrival[len(time_arrival)-1], departure_time, "d")

        # Move  each customer in queue(if any) up one place.
        # for i in range(1, num_in_q+1):
        sortQueue()

    return

def depart_2():

    global num_custs_delayed
    global num_in_q
    global time_arrival
    global server_status_2
    global total_of_delays

    delay = 0.0

    # send The customer to the second stage
    sendCustomerToSecondStage(simulation_time)

    # Check to see whether the queue is empty.
    if num_in_q == 0:
        # The queue is empty, make the server idle and eliminate the departure event from consideration
        server_status_2 = IDLE
        time_next_event[3] = 1.0e+30
    else:
        # The queue is nonempty, so decrement the number of customers.
        num_in_q = num_in_q - 1

        # Compute the delay of the customer who is beginning service and update the total delay accumulator.
        delay = simulation_time - time_arrival[len(time_arrival)-1]
        total_of_delays += delay

        # Increment the number of customers delayed, and schedule departure.
        num_custs_delayed = num_custs_delayed + 1

        departure_time = simulation_time + expon(mean_service)
        time_next_event[EVENT_DEPART_1] = departure_time
        ClientController().registerFirstDepartureTime(time_arrival[len(time_arrival) - 1], departure_time, "d")

        # Move  each customer in queue(if any) up one place.
        # for i in range(1, num_in_q+1):
        sortQueue()

    return


def sortQueue():
    global time_arrival

    # Move  each customer in queue(if any) up one place.
    # for i in range(1, num_in_q+1):

    clientes_en_cola = len(time_arrival)

    for i in range(0, clientes_en_cola - 1):
        time_arrival[i] = time_arrival[i + 1]

    if queue_type == QUEUE_PRIORITIES:
        for i in range(0, clientes_en_cola - 1):
            miCliente = ClientController().getCliente(time_arrival[i])
            if miCliente.arrivalTime != 0:
                if miCliente.withPriority:
                    # print( "Este cliente tiene prioridad")
                    time_arrival.insert(0, time_arrival.pop(time_arrival.index(miCliente.arrivalTime)))

    if queue_type == QUEUE_LIFO:
        time_arrival.sort(reverse = True)
    return


def sendCustomerToSecondStage(timeArriveToSecondStage):
    if miServer1.num_in_q_and_status() < miServer2.num_in_q_and_status() and miServer1.num_in_q_and_status() < miServer3.num_in_q_and_status():
        miServer1.externalArrive(timeArriveToSecondStage)
        return

    if miServer2.num_in_q_and_status() < miServer1.num_in_q_and_status() and miServer2.num_in_q_and_status() < miServer3.num_in_q_and_status():
        miServer2.externalArrive(timeArriveToSecondStage)
        return

    if miServer3.num_in_q_and_status() < miServer1.num_in_q_and_status() and miServer3.num_in_q_and_status() < miServer2.num_in_q_and_status():
        miServer3.externalArrive(timeArriveToSecondStage)
        return

    if miServer1.num_in_q_and_status() == miServer2.num_in_q_and_status() and miServer1.num_in_q_and_status() == miServer3.num_in_q_and_status():
        server_number = random.randint(1, 3)
        if server_number == 1:
            miServer2.externalArrive(timeArriveToSecondStage)
        if server_number == 2:
            miServer3.externalArrive(timeArriveToSecondStage)
        if server_number == 3:
            miServer1.externalArrive(timeArriveToSecondStage)

    if miServer1.num_in_q_and_status() == miServer2.num_in_q_and_status() and miServer1.num_in_q_and_status() < miServer3.num_in_q_and_status():
        server_number = random.randint(1, 2)
        if server_number == 1:
            miServer2.externalArrive(timeArriveToSecondStage)
        if server_number == 2:
            miServer1.externalArrive(timeArriveToSecondStage)
        return

    if miServer2.num_in_q_and_status() == miServer3.num_in_q_and_status() and miServer2.num_in_q_and_status() < miServer1.num_in_q_and_status():
        server_number = random.randint(1, 2)
        if server_number == 1:
            miServer2.externalArrive(timeArriveToSecondStage)
        if server_number == 2:
            miServer3.externalArrive(timeArriveToSecondStage)
        return

    if miServer1.num_in_q_and_status() == miServer3.num_in_q_and_status() and miServer3.num_in_q_and_status() < miServer2.num_in_q_and_status():
        server_number = random.randint(1, 2)
        if server_number == 1:
            miServer1.externalArrive(timeArriveToSecondStage)
        if server_number == 2:
            miServer1.externalArrive(timeArriveToSecondStage)
        return

    return

def voidTimeNextEvent():
    if time_next_event[1] <= time_next_event[2] and time_next_event[1] <= time_next_event[3]:
        return time_next_event[1]
    if time_next_event[2] <= time_next_event[1] and time_next_event[2] <= time_next_event[3]:
        return time_next_event[2]
    if time_next_event[3] <= time_next_event[1] and time_next_event[3] <= time_next_event[2]:
        return time_next_event[3]
    return


def report():
    # Compute and write estimates of desired measures of performance.

    print("Average delay in queue: ",  round(total_of_delays / num_custs_delayed, 3), " minutes")
    print("Average number in queue: ", round(area_num_in_q / simulation_time, 3))
    print("Average time spent in system: ", round(report_time_in_system(), 3), " minutes")

    print("Server utilization 1: ", round(area_server_status_1 / simulation_time, 2))
    print("Server utilization 2: ", round(area_server_status_2 / simulation_time, 2))

    report_time_in_system()

    print("Time simulation end", round(simulation_time, 2))

    return

def report_time_in_system():

    global array_time_in_system

    clientesConTiempo = []
    average_time_spent_in_system = 0

    for cliente in ClientController().clientList:
        if (cliente.arrivalTime != 0 and cliente.firstDepartureTime != 0 and cliente.secondDepartureTime != 0):
            clientesConTiempo.append(cliente)
        if(1 == 19):
            print("Test client")
            print("Arribo:", cliente.arrivalTime)
            print("Partida 1:", cliente.firstDepartureTime, " - ", cliente.fromEvent1)
            print("Partida 2:", cliente.secondDepartureTime, " - ", cliente.fromEvent2)

    for timeClient in clientesConTiempo:
        average_time_spent_in_system += timeClient.secondDepartureTime - timeClient.arrivalTime

    return_value = 0
    if(len(clientesConTiempo)>0):
        return_value = average_time_spent_in_system / len(clientesConTiempo)
    array_time_in_system.append(return_value)
    return return_value


def update_time_avg_stats():

    global time_last_event
    global time_since_last_event
    time_since_last_event = 0.0

    global area_num_in_q
    global area_server_status_1
    global area_server_status_2

    # Compute time since last event, and update last-event-time marker.
    time_since_last_event = simulation_time - time_last_event
    time_last_event = simulation_time

    # Update area under number in queue function.
    area_num_in_q += (num_in_q * time_since_last_event)*3

    # Update area under server-busy indicator function.
    area_server_status_1 += (server_status_1 * time_since_last_event)
    area_server_status_2 += (server_status_2 * time_since_last_event)

    return


def expon(mean):

    # Generate a U(0, 1) random variate.
    u = random.uniform(0, 1)

    # Return an exponential random variate with mean "mean"
    return -mean * math.log(u)


def main():
    global server_status_1
    global server_status_2
    global array_delay_in_queue_by_client
    global array_number_in_queue_by_client
    # Specify the number of events for the timing function.

    global num_events
    num_events = 2

    # values = [2, 1]
    values = [.75, 1]

    n = 2  # number of servers
    p = values[1]/(n * values[0])  # ρ = λ/cµ
    AVERAGE_CUSTOMERS_IN_QUEUE = 1.06
    AVERAGE_TIME_WAITING_IN_LINE = 1.06

    array_server_utilization1 = []
    array_server_utilization2 = []

    array_delay_in_queue_teorico = []
    array_number_in_queue_teorico = []
    array_server_utilization_teorico = []

    # Read input parameters.
    global mean_interarrival
    mean_interarrival = values[0]
    global mean_service
    mean_service = values[1]
    global num_delays_required
    num_delays_required = 1000

    # Write report heading and input parameters.
    print("Mean interarrival time:", mean_interarrival, " minutes")
    print("Mean service time:", mean_service, "minutes")
    print("Number of customers:", num_delays_required)

    # Initialize the simulation.
    initialize()
    gui = Tk()
    gui.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
    gui.title("Python Test")
    c = Canvas(gui, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    c.pack()

    # Run the simulation while more delays are still needed.
    while num_custs_delayed < num_delays_required:
        # Determine the next event
        timing()

        miServer1.timing(simulation_time)
        miServer2.timing(simulation_time)
        miServer3.timing(simulation_time)

        # Update time average statical accumulators
        update_time_avg_stats()

        # Invoke the appropriate event function

        # print ("Time next even 0:", round(voidTimeNextEvent(), 3), "Time next even 1:", round(miServer1.voidTimeNextEvent(), 3), "Time next even 2:", round(miServer2.voidTimeNextEvent(), 3), "Time next even 3:", round(miServer3.voidTimeNextEvent(), 3))

        if(voidTimeNextEvent()<miServer1.voidTimeNextEvent() and voidTimeNextEvent()<miServer2.voidTimeNextEvent() and voidTimeNextEvent()<miServer3.voidTimeNextEvent()):
            if next_event_type == EVENT_ARRIVE:
                arrive()
            if next_event_type == EVENT_DEPART_1:
                depart_1()

                array_delay_in_queue_by_client.append(round(total_of_delays / num_custs_delayed, 3))
                array_number_in_queue_by_client.append(round(area_num_in_q / simulation_time, 3))
                array_server_utilization1.append(round(area_server_status_1 / simulation_time, 4))
                array_server_utilization2.append(round(area_server_status_2 / simulation_time, 4))

                array_delay_in_queue_teorico.append(AVERAGE_TIME_WAITING_IN_LINE)
                array_number_in_queue_teorico.append(AVERAGE_CUSTOMERS_IN_QUEUE)
                array_server_utilization_teorico.append(p)
                report_time_in_system()

            if next_event_type == EVENT_DEPART_2:
                depart_2()

                array_delay_in_queue_by_client.append(round(total_of_delays / num_custs_delayed, 3))
                array_number_in_queue_by_client.append(round(area_num_in_q / simulation_time, 3))
                array_server_utilization1.append(round(area_server_status_1 / simulation_time, 4))
                array_server_utilization2.append(round(area_server_status_2 / simulation_time, 4))

                array_delay_in_queue_teorico.append(AVERAGE_TIME_WAITING_IN_LINE)
                array_number_in_queue_teorico.append(AVERAGE_CUSTOMERS_IN_QUEUE)
                array_server_utilization_teorico.append(p)
                report_time_in_system()
        else:
            if ( miServer1.voidTimeNextEvent()<= miServer2.voidTimeNextEvent() and  miServer1.voidTimeNextEvent() <= miServer3.voidTimeNextEvent()):
                miServer1.doAction()
            if (miServer2.voidTimeNextEvent() <= miServer1.voidTimeNextEvent() and miServer2.voidTimeNextEvent() <= miServer3.voidTimeNextEvent()):
                miServer2.doAction()
            if (miServer3.voidTimeNextEvent() <= miServer1.voidTimeNextEvent() and miServer3.voidTimeNextEvent() <= miServer2.voidTimeNextEvent()):
                miServer3.doAction()

        if 1 == 1:



            # print ("Largo cola: ",num_in_q, "Estado server 1: ",server_status_1, "Estado server 2: ",server_status_2," Hora de la simulacion: ", round(simulation_time, 2))

            c.create_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, fill="white")
            c.create_text(20, 140, anchor=W, font="Purisa", text="Python M/M/2 Test")
            c.create_text(20, 160, anchor=W, font="Purisa", text="Bruno Pasquini")
            c.create_text(20, 180, anchor=W, font="Purisa", text="Clientes en cola: " + str(num_in_q))
            c.create_text(20, 200, anchor=W, font="Purisa", text="Clientes atendidos: " + str(num_custs_delayed))
            c.create_text(20, 220, anchor=W, font="Purisa", text="Tiempo transcurrido: " + str(round(simulation_time, 2)))

            server_color_1 = 'green' if server_status_1 == IDLE else 'red'
            c.create_oval(MARGIN_X - (DIAMETER + QUEUE_SPACING) * -1, MARGIN_Y - 5,
                          MARGIN_X + DIAMETER - (DIAMETER + QUEUE_SPACING) * -1, MARGIN_Y - 5 + DIAMETER, outline="black",
                          fill=server_color_1)
            c.create_rectangle(MARGIN_X - 4 - (DIAMETER + QUEUE_SPACING) * -1, MARGIN_Y + 2,
                               MARGIN_X + 4 + DIAMETER - (DIAMETER + QUEUE_SPACING) * -1, MARGIN_Y + DIAMETER,
                               outline="black", fill="brown")

            server_color_2 = 'green' if server_status_2 == IDLE else 'red'
            c.create_oval(MARGIN_X - (DIAMETER + QUEUE_SPACING) * -1, MARGIN_Y - 5 + 40,
                          MARGIN_X + DIAMETER - (DIAMETER + QUEUE_SPACING) * -1, MARGIN_Y - 5 + DIAMETER + 40,
                          outline="black",
                          fill=server_color_2)
            c.create_rectangle(MARGIN_X - 4 - (DIAMETER + QUEUE_SPACING) * -1, MARGIN_Y + 2 + 40,
                               MARGIN_X + 4 + DIAMETER - (DIAMETER + QUEUE_SPACING) * -1, MARGIN_Y + DIAMETER + 40,
                               outline="black",
                               fill="brown")

            # Primera cola compartida
            if num_in_q > 0:
                for i in range(num_in_q, 0, -1):
                    c.create_oval(MARGIN_X - (DIAMETER + QUEUE_SPACING) * i, MARGIN_Y + 20,
                                  MARGIN_X + DIAMETER - (DIAMETER + QUEUE_SPACING) * i, MARGIN_Y + DIAMETER + 20,
                                  outline="black", fill='blue')

            # Primer server con cola propia
            second_server_line_color_1 = 'green' if miServer1.server_status == IDLE else 'red'
            c.create_oval(MARGIN_X - (DIAMETER + QUEUE_SPACING) * -1 + 200, MARGIN_Y - 5 + -20,
                          MARGIN_X + DIAMETER - (DIAMETER + QUEUE_SPACING) * -1 + 200, MARGIN_Y - 5 + DIAMETER + -20,
                          outline="black",
                          fill=second_server_line_color_1)
            c.create_rectangle(MARGIN_X - 4 - (DIAMETER + QUEUE_SPACING) * -1 + 200, MARGIN_Y + 2 + -20,
                               MARGIN_X + 4 + DIAMETER - (DIAMETER + QUEUE_SPACING) * -1 + 200,
                               MARGIN_Y + DIAMETER + -20,
                               outline="black",
                               fill="brown")
            for i in range(miServer1.num_in_q, 0, -1):
                c.create_oval(MARGIN_X - (DIAMETER + QUEUE_SPACING) * i + 200, MARGIN_Y + -20,
                              MARGIN_X + DIAMETER - (DIAMETER + QUEUE_SPACING) * i + 200, MARGIN_Y + DIAMETER + -20,
                              outline="black", fill='blue')

            # Segundo server con cola propia
            second_server_line_color_2 = 'green' if miServer2.server_status == IDLE else 'red'
            c.create_oval(MARGIN_X - (DIAMETER + QUEUE_SPACING) * -1 + 200, MARGIN_Y - 5 + 20,
                          MARGIN_X + DIAMETER - (DIAMETER + QUEUE_SPACING) * -1 + 200, MARGIN_Y - 5 + DIAMETER + 20,
                          outline="black",
                          fill=second_server_line_color_2)
            c.create_rectangle(MARGIN_X - 4 - (DIAMETER + QUEUE_SPACING) * -1 + 200, MARGIN_Y + 2 + 20,
                               MARGIN_X + 4 + DIAMETER - (DIAMETER + QUEUE_SPACING) * -1 + 200,
                               MARGIN_Y + DIAMETER + 20,
                               outline="black",
                               fill="brown")

            for i in range(miServer2.num_in_q, 0, -1):
                c.create_oval(MARGIN_X - (DIAMETER + QUEUE_SPACING) * i + 200, MARGIN_Y + 20,
                              MARGIN_X + DIAMETER - (DIAMETER + QUEUE_SPACING) * i + 200, MARGIN_Y + DIAMETER + 20,
                              outline="black", fill='blue')

            # Terver server con cola propia
            second_server_line_color_3 = 'green' if miServer3.server_status == IDLE else 'red'
            c.create_oval(MARGIN_X - (DIAMETER + QUEUE_SPACING) * -1 + 200, MARGIN_Y - 5 + 60,
                          MARGIN_X + DIAMETER - (DIAMETER + QUEUE_SPACING) * -1 + 200, MARGIN_Y - 5 + DIAMETER + 60,
                          outline="black",
                          fill=second_server_line_color_3)
            c.create_rectangle(MARGIN_X - 4 - (DIAMETER + QUEUE_SPACING) * -1 + 200, MARGIN_Y + 2 + 60,
                               MARGIN_X + 4 + DIAMETER - (DIAMETER + QUEUE_SPACING) * -1 + 200,
                               MARGIN_Y + DIAMETER + 60,
                               outline="black",
                               fill="brown")
            for i in range(miServer3.num_in_q, 0, -1):
                c.create_oval(MARGIN_X - (DIAMETER + QUEUE_SPACING) * i + 200, MARGIN_Y + 60,
                              MARGIN_X + DIAMETER - (DIAMETER + QUEUE_SPACING) * i + 200, MARGIN_Y + DIAMETER + 60,
                              outline="black", fill='blue')

            gui.update()
            time.sleep(.5)

    print()
    report()
    print()
    miServer1.report()
    print()
    miServer2.report()
    print()
    miServer3.report()

    queue_type_string = "FIFO"
    if queue_type == 1:
        queue_type_string = "Priorities"
    if queue_type == 2:
        queue_type_string = "LIFO"

    #plt.title("Server utilization \n MM2 - Queue type:", queue_type_string)
    #plt.plot(array_server_utilization1, color='darkgreen', label="Valor muestral")
    #plt.plot(array_server_utilization2, color='indigo', label="Valor muestral")
    #plt.plot(array_server_utilization_teorico, color='darkcyan', label="Valor Teorico")

    #plt.title("Server utilization - Second stage \n MM2 - Queue type:", queue_type_string)
    #plt.plot(miServer1.array_server_utilization, color='darkgreen', label="Valor muestral")
    #plt.plot(miServer2.array_server_utilization, color='indigo', label="Valor muestral")
    #plt.plot(miServer3.array_server_utilization, color='firebrick', label="Valor muestral")


    #plt.title("Average number in queue \n MM2 - Queue type:", queue_type_string)
    #plt.plot(array_number_in_queue_by_client, color='teal', label="Valor muestral")
    #plt.plot(array_number_in_queue_teorico, color='orange', label="Valor Teorico")

    #plt.title("Average number in queue - Second stage \n MM2")
    #plt.plot(miServer1.array_number_in_queue_by_client, color='orchid', label="Valor muestral")
    #plt.plot(miServer2.array_number_in_queue_by_client, color='darkmagenta', label="Valor muestral")
    #plt.plot(miServer3.array_number_in_queue_by_client, color='indigo', label="Valor muestral")

    print("len 1:", len(miServer1.array_number_in_queue_by_client), "\nlen 2:", len(miServer2.array_number_in_queue_by_client), "\nlen 3:", len(miServer3.array_number_in_queue_by_client))

    # plt.title("Average time spent in system \n MM2 - Queue type: " + queue_type_string)
    # plt.plot(array_time_in_system, color='slategray', label="Valor muestral")


    #plt.show()

    return


print("Cola MM2 Final - Rev 2")

queue_type_string = "FIFO"
if queue_type == 1:
    queue_type_string = "Priorities"
if queue_type == 2:
    queue_type_string = "LIFO"

print("Queue type:", queue_type_string)

main()


