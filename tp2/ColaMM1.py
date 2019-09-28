import random
import math
import matplotlib.pyplot as plt

Q_LIMIT = 100
BUSY = 1
IDLE = 0

EVENT_ARRIVE = 1
EVENT_DEPART = 2

next_event_type = 1
num_custs_delayed = 0
num_delays_required = 4
num_events = 0
num_in_q = 0
server_status = 0

area_num_in_q = 0.0
area_server_status = 0.0
area_server_status = 0.0
mean_interarrival = 0.0
mean_service = 0.0
time = 0.0
time_arrival = []
time_last_event = 0.0
time_next_event = []
total_of_delays = 0.0

array_delay_in_queue = []
array_number_in_queue = []

array_delay_in_queue_by_client = []
array_number_in_queue_by_client = []


# Run the simulation
def initialize():

    # Initialize the simulation clock.
    global time
    time = 0.0

    # Initialize the state variables.
    global server_status
    server_status = IDLE
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
    global area_server_status
    area_server_status = 0.0

    # Initialize event list.
    # Since no customers are present, the departure(service completion) event is eliminated from consideration.
    global time_next_event
    del time_next_event[:]
    time_next_event.append(0)
    time_next_event.append(0)
    time_next_event.append(0)

    time_next_event[EVENT_ARRIVE] = time + expon(mean_interarrival)
    time_next_event[EVENT_DEPART] = 1.0e+30
    return;


def timing():

    global num_events
    global time_next_event
    global next_event_type
    global time

    min_time_next_event = 1.0e+29
    next_event_type = 0

    # Determine the event type of the next even to occur.
    for i in range(1, 3):
        if time_next_event[i] < min_time_next_event:
            min_time_next_event = time_next_event[i]
            next_event_type = i

    # Check to see whether the event list is empty.
    if next_event_type == 0:
        # The event list is empty, so stop the simulation.
        print("The event list is empty at time:", time)
        exit()

    # The event list is not empty, so advance the simulation clock.
    time = min_time_next_event

    return


def arrive():

    global time_next_event
    global time
    global mean_interarrival
    global server_status
    global total_of_delays
    global time_arrival
    global num_in_q
    global num_custs_delayed
    delay = 0.0
    # Schedule next arrival.
    time_next_event[EVENT_ARRIVE] = time + expon(mean_interarrival)

    # Check to see whether server is busy.
    if server_status == BUSY:
        # Server is busy, so increment number of customers in queue.
        num_in_q = num_in_q+1

        # Check to see whether an overflow condition exists.
        if num_in_q > Q_LIMIT:
            # The queue has overflowed, so stop the simulation.
            print("Overflow of the array time_arrival at ", time, " time")
            exit(2)

        # There is still room in the queue,
        # so store the time of arrival of the arriving customer at the(new) end of time_arrival.

        # time_arrival[num_in_q] = time
        time_arrival.append(time)
    else:
        # Server is idle, so arriving customer has a delay of zero.
        # (The following two  statements are for program clarity and do not affect the results of the simulation).
        delay = 0.0
        total_of_delays += delay

        # Increment the number of customers delayed, and make server busy.
        num_custs_delayed = num_custs_delayed+1
        server_status = BUSY
        # Schedule a departure(service completion).
        time_next_event[EVENT_DEPART] = time + expon(mean_service)

    return


def depart():

    global num_custs_delayed
    global num_in_q
    global time_arrival
    global server_status
    global total_of_delays

    delay = 0.0

    # Check to see whether the queue is empty.

    if num_in_q == 0:
        # The queue is empty, make the server idle and eliminate the departure event from consideration
        server_status = IDLE
        time_next_event[2] = 1.0e+30
    else:
        # The queue is nonempty, so decrement the number of customers.
        num_in_q = num_in_q - 1

        # Compute the delay of the customer who is beginning service and update the total delay accumulator.
        delay = time - time_arrival[len(time_arrival)-1]
        total_of_delays += delay

        # Increment the number of customers delayed, and schedule departure.
        num_custs_delayed = num_custs_delayed + 1
        time_next_event[EVENT_DEPART] = time + expon(mean_service)

        # Move  each customer in queue(if any) up one place.
        # for i in range(1, num_in_q+1):
        for i in range(0, len(time_arrival)-1):
            time_arrival[i] = time_arrival[i + 1]

    return


def report():
    # Compute and write estimates of desired measures of performance.

    print("Average delay in queue: ",  round(total_of_delays / num_custs_delayed, 3), " minutes")
    print("Average number in queue: ", round(area_num_in_q / time, 3))
    print("Server utilization: ", round(area_server_status / time, 2))
    print("Time simulation end",  round(time, 2))

    return


def update_time_avg_stats():

    global time_last_event
    global time_since_last_event
    time_since_last_event = 0.0

    global area_num_in_q
    global area_server_status

    # Compute time since last event, and update last-event-time marker.
    time_since_last_event = time - time_last_event
    time_last_event = time

    # Update area under number - in -queue function.
    area_num_in_q += (num_in_q * time_since_last_event)

    # Update area under server-busy indicator function.
    area_server_status += (server_status * time_since_last_event)

    return


def expon(mean):

    # Generate a U(0, 1) random variate.
    u = random.uniform(0, 1)

    # Return an exponential random variate with mean "mean"
    return -mean * math.log(u)


def main():
    global array_delay_in_queue
    global array_number_in_queue

    global array_delay_in_queue_by_client
    global array_number_in_queue_by_client

    # Specify the number of events for the timing function.
    global num_events
    num_events = 2

    values = [2, 0.6]

    p = values[1]/values[0] # ρ = λ/µ for single server queues: utilization of the server
    AVERAGE_CUSTOMERS_IN_QUEUE = (p**2)/(1-p)
    AVERAGE_TIME_WAITING_IN_LINE = AVERAGE_CUSTOMERS_IN_QUEUE / values[1]

    array_server_utilization = []

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
    print("Single-server queueing system")
    print("Mean interarrival time:", mean_interarrival, " minutes")
    print("Mean service time:", mean_service, "minutes")
    print("Number of customers:", num_delays_required)


    for i in range(1):
        print(" ")
        # Initialize the simulation.
        initialize()

        # Run the simulation while more delays are still needed.
        while num_custs_delayed < num_delays_required:
            # Determine the next event
            timing()

            # Update time average statical accumulators
            update_time_avg_stats()

            # Invoke the appropriate event function
            if next_event_type == EVENT_ARRIVE:
                arrive()
            if next_event_type == EVENT_DEPART:
                depart()

                array_delay_in_queue_by_client.append(round(total_of_delays / num_custs_delayed, 3))
                array_number_in_queue_by_client.append(round(area_num_in_q / time, 3))
                array_server_utilization.append(round(area_server_status / time, 4))

                array_delay_in_queue_teorico.append(AVERAGE_TIME_WAITING_IN_LINE)
                array_number_in_queue_teorico.append(AVERAGE_CUSTOMERS_IN_QUEUE)
                array_server_utilization_teorico.append(p)

        report()

    plt.title("Server utilization")
    plt.plot(array_server_utilization, color='darkgreen', label="Valor muestral")
    plt.plot(array_server_utilization_teorico, color='darkcyan', label="Valor Teorico")

    #plt.title("Average number in queue")
    #plt.plot(array_number_in_queue_by_client, color='teal', label="Valor muestral")
    #plt.plot(array_number_in_queue_teorico, color='orange', label="Valor Teorico")

    # plt.title("Average delay in queue")
    # plt.plot(array_delay_in_queue_by_client, color='tomato', label="Valor muestral")
    # plt.plot(array_delay_in_queue_teorico, color='hotpink', label="Valor Teorico")

    plt.show()

    return


print("Cola MM1")
main()


