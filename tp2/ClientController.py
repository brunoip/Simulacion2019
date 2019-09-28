import random
from tp2.SimpleClient import SimpleClient


class ClientController:

    clientList = []
    numero_cliente_con_prioridad = 0

    def __init__(self):
        numero_cliente_con_prioridad = 0

    def getCliente(self, timeArrival):
        global clientList
        for miCliente in self.clientList:
            if miCliente.arrivalTime == timeArrival:
                return miCliente
        return

    def registerArrival(self, time):
        global clientList
        miCliente = SimpleClient()
        miCliente.arrivalTime = time
        random_number = random.randint(1, 100)
        if random_number >= 95:
            miCliente.withPriority = True
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

