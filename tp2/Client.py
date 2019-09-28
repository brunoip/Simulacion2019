import random
import math

class Client:

    arrivalTime = 0
    firstDepartureTime = 0
    secondDepartureTime = 0
    clientList = []
    fromEvent1 = "n"
    fromEvent2 = "n"

    def __init__(self):
        self.arrivalTime = 0
        self.firstDepartureTime = 0
        self.secondDepartureTime = 0


    def registerArrival(self, time):
        global clientList
        miCliente = Client()
        miCliente.arrivalTime = time
        self.clientList.append(miCliente)

        return

    def registerFirstDepartureTime(self, timeArrival, timeDeparture, from1):
        global clientList
        for miCliente in self.clientList:
            if miCliente.arrivalTime == timeArrival:
                miCliente.firstDepartureTime = timeDeparture
                miCliente.fromEvent1 = from1
                return
        return

    def registerSecondDepartureTime(self, timeArrival, timeDeparture, from2):
        global clientList
        for miCliente in self.clientList:
            if miCliente.firstDepartureTime == timeArrival:
                miCliente.secondDepartureTime = timeDeparture
                miCliente.fromEvent2 = from2
                return

        return

