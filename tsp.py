import csv, copy, threading, sys

lock = threading.Lock()

class Route:
	totalRevenue = 0
	destination = ""

	def __init__(self, destination, totalRevenue, row):
		self.destination = destination
		self.totalRevenue = int(float(totalRevenue))
		self.trips = 1
		self.row = row

	def add(self, revenue):
		self.totalRevenue += revenue
		self.trips += 1

	def averageRevenue(self):
		return self.totalRevenue / self.trips

	def __eq__(self, other):
		return self.destination == other.destination

	def __ne__(self, other):
		return not self.__eq__(other)

	def __str__(self):
		return self.destination + "-$" + str(self.averageRevenue()) + "-" + str(self.trips)

	def __repr__(self):
		return self.__str__()

def betterRoute(routes, route):
	for r in routes:
		if r == route:
			r.add(route.totalRevenue)


def add(routes, route, size, capacity):
	#print("Capacity: " + str(capacity) + " Size: " + str(size))
	if route not in routes:
		#print("Appending route: " + str(route))
		routes.append(route)
	else:
		#print("Checking if route is more optimal: " + str(route))
		betterRoute(routes, route)

def getRoutes(startCity, allRoutes):
	receiverCityIndex = 2
	totalRevenueIndex = 3
	startCityIndex = 4
	possibleRoutes = 10 
	routes = []
	for row in allRoutes:
		possibleStartCity = row[startCityIndex]
		if startCity == possibleStartCity:
			destination = row[receiverCityIndex]
			totalRevenue = row[totalRevenueIndex]
			r = Route(destination, totalRevenue, row)
			add(routes, r, len(routes), possibleRoutes)
	return routes

def displayRoutes(routes):
	for route in routes:
		print(route)

def getRouteInfo(routes, city):
	for route in routes:
		if route.destination == city:
			return route

def threadWrapper(log, depth, allRoutes, thread_num, thread_log):
	output = recursiveRoute(log, depth, allRoutes, thread_num, thread_log)
	with lock:
		print("Thread[" + str(thread_num) + "] output")
		for itenerary in output:
			print(itenerary)

def recursiveRoute(log, depth, allRoutes, thread_num, thread_log):
	thread_log.append(str(log))
	if depth < 2:
		for city in log:
			lastCity = city
		routes = getRoutes(lastCity, allRoutes)
		newDepth = depth + 1
		for route in routes:
			newLog = copy.deepcopy(log)
			newLog.append(route.destination)
			recursiveRoute(newLog, newDepth, allRoutes, thread_num, thread_log)
	return thread_log

def threadPool(threads):
	concurent = 25
	if len(threads) < concurent:
		concurent = len(threads)

	print("The thread pool contains " + str(len(threads)))
	print("Running " + str(concurent) + " threads")

	count = 0
	for t in reversed(threads):
		t.start()
		count += 1
		if count == concurent:
			break
	
	count = 0
	for t in reversed(threads):
		t.join()
		count += 1
		if count == concurent:
			break

	for i in range(concurent):
		threads.pop()

	if threads:
		threadPool(threads)


if __name__ == "__main__":
	allRoutes = []
	print("Loading routes into memory")
	header = True
	headings = []
	log = []
	with open('processedData.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			if header:
				headings = row
				header = False
			else:
				allRoutes.append(row)

	city = raw_input("Enter a city to start your route: ")
	city = city.upper()
	log.append(city)
	routes = getRoutes(city, allRoutes)
	thread_num = 0
	threads = []
	for route in routes:
		newLog = copy.deepcopy(log)
		newLog.append(route.destination)
		thread_log = []
		threads.append(threading.Thread(target=threadWrapper, args=(newLog, 1, allRoutes, thread_num, thread_log)))
		thread_num += 1
	print("Number of threads: " + str(len(threads)))
	threadPool(threads)
	print("The Travelling Salesman Problem")