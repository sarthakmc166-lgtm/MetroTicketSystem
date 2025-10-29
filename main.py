import csv
import uuid

name=input("Whats your name : ")
stations={}

class Stations:
    def  __init__(self,station_name):
        self.station_name=station_name
        self.connections=[]
    @staticmethod
    def load_stations():
        with open("stations.csv","r") as file:
            reader=csv.reader(file)
            for row in reader:
                stations[row[0]]=Stations(row[0])
        return stations
    def add_connection(self,joined_station):
        if joined_station not in self.connections:
            self.connections.append(joined_station)
    @staticmethod
    def load_connections():
        with open("connections.csv","r") as file:
            reader=csv.reader(file)
            for row in reader:
                s1=stations[row[0]]
                s2=stations[row[1]]
                s1.add_connection(s2)
                s2.add_connection(s1)
                #print(f"Connection added between {s1.station_name} and {s2.station_name}")

    @staticmethod
    def Station_loader():
        with open("stations.csv","r") as file:
            reader=csv.reader(file)
            for row in reader:
                print(row[0])

class Tickets(Stations):
    @staticmethod
    def ticket_id():
        ticketid=str(uuid.uuid4())[:8]
        return ticketid
    @staticmethod
    def tickets_loader():
        with open("tickets.csv","r") as file:
            reader=csv.reader(file)
            for row in reader:
                if row[0]==name:
                    print("""Username : {}
                    Ticket ID : {}
                    Origin : {}
                    Destination : {}
                    Price : {}""".format(row[0],row[1],row[2],row[3],row[4]))
    @staticmethod
    def path_finder(current_station,destination,path=[]):
        path = path + [current_station]
        paths=[]
        if current_station==destination:
            return path
        else:
            for neighbour in stations[current_station].connections:
                if neighbour.station_name not in path:
                    new_path=Tickets.path_finder(neighbour.station_name, destination, path)
                    if new_path:
                        paths.append(new_path)
        if paths:
            return min(paths, key=len)
    @staticmethod
    def tickets_writer(name,ticketid,origin,destination,fare):
        with open("tickets.csv","a",newline='') as file:
            writer=csv.writer(file)
            writer.writerow([name,ticketid,origin,destination,fare])
    @staticmethod
    def tickets_purchaser():
        var=int(input('''Press 1 for Viewing Stations\nPress 2 for Purchasing Tickets\nPress 3 for Viewing Tickets\nPress 4 for Exiting the system : '''))
        if var==1:
            Stations.Station_loader()
            Tickets.tickets_purchaser()
        elif var==2:
            current_station=input("Enter your Origin Station : ")
            destination=input("Enter your Destination Station : ")
            if current_station not in stations or destination not in stations:
                print("One or both stations are invalid. Please try again.")
                Tickets.tickets_purchaser()
            else:
                final_path=Tickets.path_finder(current_station,destination)
                print("The path from {} to {} is : {}".format(current_station,destination,final_path))
                with open("intersections.csv","r") as file:
                    reader=csv.reader(file)
                    for row in reader:
                        if row[0] in final_path and row[0]!=current_station and row[0]!=destination:
                            print("Intersection at {}".format(row[0]))
                fare=(len(final_path)-1)*5
                print("The total fare is : {}".format(fare))
                confirm=input("Do you want to proceed with the purchase ? (yes/no) : ")
                if confirm=="yes":
                    ticketid=Tickets.ticket_id()
                    Tickets.tickets_writer(name,ticketid,current_station,destination,fare)
                    print("Ticket Purchased Successfully")
                    Tickets.tickets_purchaser()
                else:
                    print("Purchase Cancelled")
                    Tickets.tickets_purchaser()
        elif var==3:
            Tickets.tickets_loader()
            Tickets.tickets_purchaser()
        elif var==4:
            print("Exiting system......")
            exit()
        else:
            print("Please enter a valid option")
Stations.load_stations()
Stations.load_connections() 
Tickets.tickets_purchaser()
