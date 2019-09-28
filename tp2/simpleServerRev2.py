import random
import math
from tp2.Client import Client
from tp2.ClientController import ClientController

class simpleServerRev2:

    serverName = ""
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
    mean_interarrival = 0.0
    mean_service = 0.0
    time = 1
    time_arrival = []
    time_last_event = 0.0
    #time_next_event = []
    total_of_delays = 0.0

    #array_server_utilization = []
    #array_server_utilization_teorico = []
    array_departure_times = []

    array_delay_in_queue_by_client = []
    # array_number_in_queue_by_client = []

    externalArrivals = False


    def __init__(self):
        self.time_arrival = []
        self.time_next_event = []
        self.array_server_utilization = []
        self.array_server_utilization_teorico = []
        self.array_number_in_queue_by_client = []

    # Run the simulation
    def initialize(self, serverName, mean_interarrival, mean_service,  externalArrivals ):

        # Initialize the simulation clock.
        global time
        time = 1

        global array_number_in_queue_by_client
        global array_server_utilization
        global array_server_utilization_teorico

        array_number_in_queue_by_client = []
        array_server_utilization = []
        array_server_utilization_teorico = []

        self.serverName = serverName
        self.mean_interarrival = mean_interarrival
        self.mean_service = mean_service

        global num_events
        self.num_events = 2

        global num_delays_required
        self.num_delays_required = 1000

        self.externalArrivals = externalArrivals

        # Initialize the state variables.
        global server_status
        server_status = self.IDLE
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
        del self.time_next_event[:]
        self.time_next_event.append(0)
        self.time_next_event.append(0)
        self.time_next_event.append(0)

        self.time_next_event[self.EVENT_ARRIVE] = time + self.expon(self.mean_interarrival)

        self.time_next_event[self.EVENT_DEPART] = 1.0e+30

        if self.externalArrivals == True:
            self.time_next_event[self.EVENT_ARRIVE] = 1.0e+30

        return;

    def timing(self, myTime):

        global num_events
        global time_next_event
        global next_event_type
        global time

        self.min_time_next_event = 1.0e+29
        self.next_event_type = 0

        # Determine the event type of the next even to occur.
        for i in range(1, 3):
            if self.time_next_event[i] < self.min_time_next_event:
                self.min_time_next_event = self.time_next_event[i]
                self.next_event_type = i

        # Check to see whether the event list is empty.
        if self.next_event_type == 0 and self.externalArrive == False:
            # The event list is empty, so stop the simulation.
            print("The event list is empty at time:", self.time)
            exit()

        # The event list is not empty, so advance the simulation clock.
        if self.externalArrive == False:
            self.time = self.min_time_next_event
        else:
            self.time = myTime

        return

    def voidTimeNextEvent(self):
        if self.time_next_event[self.EVENT_ARRIVE] < self.time_next_event[self.EVENT_DEPART]:
            return self.time_next_event[self.EVENT_ARRIVE]
        else:
            return self.time_next_event[self.EVENT_DEPART]
        return

    def arrive(self):

        global time_next_event
        global time
        global mean_interarrival
        global server_status
        global total_of_delays
        global time_arrival
        global num_in_q
        global num_custs_delayed
        global externalArrivals
        global array_departure_times

        delay = 0.0
        # Schedule next arrival.
        # Arrivals are externals
        if self.externalArrivals == False:
            self.time_next_event[self.EVENT_ARRIVE] = self.time + self.expon(self.mean_interarrival)
        else:
            self.time_next_event[self.EVENT_ARRIVE] = 1.0e+28

        # Check to see whether server is busy.
        if self.server_status == self.BUSY:
            # Server is busy, so increment number of customers in queue.
            self.num_in_q = self.num_in_q + 1

            # Check to see whether an overflow condition exists.
            if self.num_in_q > self.Q_LIMIT:
                # The queue has overflowed, so stop the simulation.
                print("Overflow of the array time_arrival at time: ", self.time, "on server:", self.serverName)
                exit(2)

            # time_arrival[num_in_q] = time
            self.time_arrival.append(self.time)

        else:
            # Server is idle, so arriving customer has a delay of zero.
            # (The following two  statements are for program clarity and do not affect the results of the simulation).
            self.delay = 0.0
            self.total_of_delays += self.delay

            # Increment the number of customers delayed, and make server busy.
            self.num_custs_delayed = self.num_custs_delayed + 1
            self.server_status = self.BUSY

            # Schedule a departure(service completion).
            departureTime = self.time + self.expon(self.mean_service)
            self.time_next_event[self.EVENT_DEPART] = departureTime
            self.array_departure_times.append(departureTime)
            ClientController().registerSecondDepartureTime(self.time, departureTime, "a")

        return

    def externalArrive(self, timeArrival):
        self.time_next_event[self.EVENT_ARRIVE] = timeArrival
        self.time_arrival.append(timeArrival)

        return

    def doAction(self):

        global area_server_status
        global array_server_utilization
        global array_server_utilization_teorico
        global array_delay_in_queue_by_client
        global array_number_in_queue_by_client
        # self.timing()

        p = 1 / self.mean_service
        # Update time average statical accumulators
        self.update_time_avg_stats()

        if self.next_event_type == self.EVENT_ARRIVE:
            self.arrive()
        if self.next_event_type == self.EVENT_DEPART:
            self.depart()

            self.array_number_in_queue_by_client.append(round(self.area_num_in_q / self.time, 4))
            self.array_server_utilization.append(round(self.area_server_status / self.time, 4))
            self.array_server_utilization_teorico.append(p)

        return

    def depart(self):

        global num_custs_delayed
        global num_in_q
        global time_arrival
        global server_status
        global total_of_delays

        self.delay = 0.0

        # Check to see whether the queue is empty.

        if self.num_in_q == 0:
            # The queue is empty, make the server idle and eliminate the departure event from consideration
            self.server_status = self.IDLE
            self.time_next_event[self.EVENT_DEPART] = 1.0e+30
        else:
            # The queue is nonempty, so decrement the number of customers.
            self.num_in_q = self.num_in_q - 1

            # Compute the delay of the customer who is beginning service and update the total delay accumulator.
            self.delay = self.time - self.time_arrival[len(self.time_arrival) - 1]
            self.total_of_delays += self.delay

            # Increment the number of customers delayed, and schedule departure.
            self.num_custs_delayed = self.num_custs_delayed + 1

            departureTime = self.time + self.expon(self.mean_service)
            self.time_next_event[self.EVENT_DEPART] = departureTime
            self.array_departure_times.append(departureTime)

            ClientController().registerSecondDepartureTime(self.time_arrival[len(self.time_arrival) - 1], departureTime, "d")

            # Move  each customer in queue(if any) up one place.
            # for i in range(1, num_in_q+1):
            for i in range(0, len(self.time_arrival) - 1):
                self.time_arrival[i] = self.time_arrival[i + 1]

        return

    def report(self):
        # Compute and write estimates of desired measures of performance.
        print("Report for ", self.serverName, ":")
        print("Average delay in queue: ", round(self.total_of_delays / self.num_custs_delayed, 3), " minutes")
        print("Average number in queue: ", round(self.area_num_in_q / self.time, 3))
        print("Server utilization: ", round(self.area_server_status / self.time, 2))
        # print("Time simulation end", self.time)


        return

    def num_in_q_and_status(self):
        status_num = 1 if self.server_status == self.BUSY else 0
        return self.num_in_q + status_num

    def update_time_avg_stats(self):

        global time_last_event
        global time_since_last_event
        self.time_since_last_event = 0.0

        global area_num_in_q
        global area_server_status

        # Compute time since last event, and update last-event-time marker.
        self.time_since_last_event = self.time - self.time_last_event
        self.time_last_event = self.time

        # Update area under number - in -queue function.
        self.area_num_in_q += (self.num_in_q * self.time_since_last_event)

        # Update area under server-busy indicator function.
        self.area_server_status += (self.server_status * self.time_since_last_event)

        return

    def expon(self, mean):

        # Generate a U(0, 1) random variate.
        u = random.uniform(0, 1)

        # Return an exponential random variate with mean "mean"
        return -mean * math.log(u)

    def main(self):
        global array_delay_in_queue
        global array_number_in_queue

        global array_delay_in_queue_by_client
        global array_number_in_queue_by_client

        global array_server_utilization
        global array_server_utilization_teorico

        # Specify the number of events for the timing function.
        global num_events
        num_events = 2

        values = [2, 0.6]

        p = values[1] / values[0]  # ρ = λ/µ for single server queues: utilization of the server
        AVERAGE_CUSTOMERS_IN_QUEUE = (p ** 2) / (1 - p)
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

        mean_service_initial = mean_service

        # Write report heading and input parameters.
        print("Single-server queueing system")
        print("Mean interarrival time:", mean_interarrival, " minutes")
        print("Mean service time:", mean_service, "minutes")
        print("Number of customers:", num_delays_required)

        # Initialize the simulation.
        self.initialize()

        # Run the simulation while more delays are still needed.
        while num_custs_delayed < num_delays_required:
            # Determine the next event
            self.timing()

            # Update time average statical accumulators
            self.update_time_avg_stats()

            # Invoke the appropriate event function
            if next_event_type == self.EVENT_ARRIVE:
                self.arrive()
            if next_event_type == self.EVENT_DEPART:
                self.depart()

                array_delay_in_queue_by_client.append(round(total_of_delays / num_custs_delayed, 3))
                array_number_in_queue_by_client.append(round(area_num_in_q / time, 3))
                array_server_utilization.append(round(area_server_status / time, 4))

                array_delay_in_queue_teorico.append(AVERAGE_TIME_WAITING_IN_LINE)
                array_number_in_queue_teorico.append(AVERAGE_CUSTOMERS_IN_QUEUE)
                array_server_utilization_teorico.append(p)

        return