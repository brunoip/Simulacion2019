import random
import math
import matplotlib.pyplot as plt
import time
from tkinter import *
from tp2.simpleServer import simpleServer
from tp2.testClass import testClass

Q_LIMIT = 100
BUSY = 1
IDLE = 0

EVENT_ARRIVE = 1
EVENT_DEPART_1 = 2
EVENT_DEPART_2 = 3

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
    time_next_event[EVENT_ARRIVE] = simulation_time + expon(mean_interarrival)

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
        # (The following two  statements are for program clarity and do not affect the results of the simulation).
        delay = 0.0
        total_of_delays += delay

        # Increment the number of customers delayed, and make server busy.
        num_custs_delayed = num_custs_delayed + 1

        if server_status_1 == IDLE and server_status_2 == BUSY:
            server_status_1 = BUSY
            # Schedule a departure(service completion).
            time_next_event[EVENT_DEPART_1] = simulation_time + expon(mean_service)

        if server_status_1 == BUSY and server_status_2 == IDLE:
            server_status_2 = BUSY
            # Schedule a departure(service completion).
            time_next_event[EVENT_DEPART_2] = simulation_time + expon(mean_service)

        if server_status_1 == IDLE and server_status_2 == IDLE:
            # Both servers are free, flip a coin to see who take the customer
            if bool(random.getrandbits(1)):
                server_status_1 = BUSY
                # Schedule a departure(service completion).
                time_next_event[EVENT_DEPART_1] = simulation_time + expon(mean_service)
            else:
                server_status_2 = BUSY
                # Schedule a departure(service completion).
                time_next_event[EVENT_DEPART_2] = simulation_time + expon(mean_service)
    return


def depart_1():

    global num_custs_delayed
    global num_in_q
    global time_arrival
    global server_status_1
    global total_of_delays

    delay = 0.0

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
        time_next_event[EVENT_DEPART_1] = simulation_time + expon(mean_service)

        # Move  each customer in queue(if any) up one place.
        # for i in range(1, num_in_q+1):
        for i in range(0, len(time_arrival)-1):
            time_arrival[i] = time_arrival[i + 1]

    return

def depart_2():

    global num_custs_delayed
    global num_in_q
    global time_arrival
    global server_status_2
    global total_of_delays

    delay = 0.0

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
        time_next_event[EVENT_DEPART_2] = simulation_time + expon(mean_service)

        # Move  each customer in queue(if any) up one place.
        # for i in range(1, num_in_q+1):
        for i in range(0, len(time_arrival)-1):
            time_arrival[i] = time_arrival[i + 1]

    return


def report():
    # Compute and write estimates of desired measures of performance.

    print("Average delay in queue: ",  round(total_of_delays / num_custs_delayed, 3), " minutes")
    print("Average number in queue: ", round(area_num_in_q / simulation_time, 3))
    print("Server utilization 1: ", round(area_server_status_1 / simulation_time, 2))
    print("Server utilization 2: ", round(area_server_status_2/ simulation_time, 2))
    print("Time simulation end", simulation_time)

    return


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

    # Update area under number - in -queue function.
    area_num_in_q += (num_in_q * time_since_last_event)

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
    # Specify the number of events for the timing function.

    global num_events
    num_events = 2

    # values = [2, 0.6, .21, .12]
    values = [7, 9, .21, .12]

    # Read input parameters.
    global mean_interarrival
    mean_interarrival = values[0]
    global mean_service
    mean_service = values[1]
    global num_delays_required
    num_delays_required = 1000

    mean_service_initial= mean_service

    # Write report heading and input parameters.
    print("Single-server queueing system")
    print("Mean interarrival time:", mean_interarrival, " minutes")
    print("Mean service time:", mean_service, "minutes")
    print("Number of customers:", num_delays_required)

    # Initialize the simulation.
    initialize()
    myobjectx = testClass()
    myobjectx.myPrint("hola","test")

    # Run the simulation while more delays are still needed.
    while num_custs_delayed < num_delays_required:
        # Determine the next event
        timing()

        # Update time average statical accumulators
        update_time_avg_stats()

        # Invoke the appropriate event function
        if next_event_type == EVENT_ARRIVE:
            arrive()
        if next_event_type == EVENT_DEPART_1:
            depart_1()
        if next_event_type == EVENT_DEPART_2:
            depart_2()

        if True == True:
            print ("Largo cola: ",num_in_q, "Estado server 1: ",server_status_1, "Estado server 2: ",server_status_2," Hora de la simulacion: ", round(simulation_time, 2))

            c.create_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, fill="white")
            c.create_text(20, 100, anchor=W, font="Purisa", text="Python M/M/2 Test")
            c.create_text(20, 120, anchor=W, font="Purisa", text="Bruno Pasquini")
            c.create_text(20, 140, anchor=W, font="Purisa", text="Clientes en cola: " + str(num_in_q))
            c.create_text(20, 160, anchor=W, font="Purisa", text="Clientes atendidos: " + str(num_custs_delayed))
            c.create_text(20, 180, anchor=W, font="Purisa", text="Tiempo transcurrido: " + str(round(simulation_time, 2)))

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

            if num_in_q > 0:
                for i in range(num_in_q, 0, -1):
                    c.create_oval(MARGIN_X - (DIAMETER + QUEUE_SPACING) * i, MARGIN_Y + 20,
                                  MARGIN_X + DIAMETER - (DIAMETER + QUEUE_SPACING) * i, MARGIN_Y + DIAMETER + 20,
                                  outline="black", fill='blue')

            gui.update()
            time.sleep(0.5)

    report()

    # plt.title("Average number in queue")
    # plt.plot(array_number_in_queue_teorico, label="Valor Teorico")
    # plt.plot(array_number_in_queue, label="Valor muestral")

    # plt.title("Average delay in queue")
    # plt.plot(array_delay_in_queue_teorico, label="Valor Teorico")
    # plt.plot(array_delay_in_queue, color='seagreen', label="Valor muestral")

    # plt.title("Server utilization")
    # plt.plot(array_server_utilization, color='purple')

    # plt.title("Average delay in queue")
    # plt.plot(array_number_in_queue_teorico, label="Valor Teorico")
    # plt.plot(array_number_in_queue_by_client, color='seagreen', label="Valor muestral")

    # plt.title("Average number in queue by client")
    # plt.plot(array_delay_in_queue_by_client, color='seagreen', label="Valor muestral")
    # plt.plot(array_delay_in_queue_teorico, label="Valor Teorico")

    plt.show()

    return


print("Cola MM2")
main()


