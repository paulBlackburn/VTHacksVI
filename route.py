import csv

class Route:
	totalRevenue = 0
	destination = ""

	def __init__(self, destination, totalRevenue, row):
		self.destination = destination
		self.totalRevenue = int(float(totalRevenue))
		self.row = row

	def __eq__(self, other):
		return self.destination == other.destination

	def __ne__(self, other):
		return not self.__eq__(other)

	def __str__(self):
		return self.destination + "-$" + str(self.totalRevenue)

	def __repr__(self):
		return self.__str__()

def betterRoute(routes, route):
	minTotalRevenueIndex = 0
	minTotalRevenue = routes[0].totalRevenue
	better = False
	for i in range(len(routes)):
		r = routes[i]
		if r.totalRevenue < minTotalRevenue:
			minTotalRevenue = r.totalRevenue
			minTotalRevenueIndex = i
	if route.totalRevenue > minTotalRevenue:
		better = True
	
	if better:
		for r in routes:
			if route == r:
				if route.totalRevenue > r.totalRevenue:
					r.totalRevenue = route.totalRevenue
					routes.sort(key=lambda x: x.totalRevenue, reverse=True)
				return

		routes[minTotalRevenueIndex] = route
		routes.sort(key=lambda x: x.totalRevenue, reverse=True)

def add(routes, route, size, capacity):
	#print("Capacity: " + str(capacity) + " Size: " + str(size))
	if size < capacity and route not in routes:
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

def displayLog(log):
	start = True
	print("Start: " + log[0])
	log.pop(0)
	print("Jobs: " + str(log))
	bag = 0
	for city in log:
		bag += city.totalRevenue
	print("Total Pay: $" + str(bag))



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
	while len(log) < 5:
	    if routes:
	    	print("***Possible Routes***")
	    	displayRoutes(routes)
	    city = raw_input("City: ")
	    if not city:
	    	break
	    city = city.upper()
	    log.append(getRouteInfo(routes, city))
	    routes = getRoutes(city, allRoutes)
	print("***Itinerary***")
	displayLog(log)