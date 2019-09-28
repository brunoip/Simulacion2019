from tp2.simpleServer import simpleServer

miServer = simpleServer()
miServer.serverName = "1"
miServer.initialize("1", 2, .6, False)


while miServer.num_custs_delayed < miServer.num_delays_required:
    # Determine the next event
    miServer.timing()

    # Update time average statical accumulators
    miServer.update_time_avg_stats()

    # Invoke the action
    miServer.doAction()

miServer.report()
