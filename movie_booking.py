"""This module is to enable movie booking through an automation script"""
import re  # For regular expressions
movie_list = {"Superman": 250, "Avengers": 300, "Hulk": 200, "Ironman": 400}
ADM_PSW = "password"


class Movie:  # Class movie for movie related functions
    """This class deals with adding a movie & searching a movie"""
    def __init__(self, name=None, price=0):
        self.name = name
        self.price = price

    def movie_add(self):
        """Adds an admin specified movie to the list of movies"""
        self.name = input("Enter the movie you want to add: ")
        while True:
            try:
                self.price = int(input("Enter the ticket price: "))
                break
            except ValueError:  # Exception handling for ValueError
                print("Invalid input")
        if self.name not in movie_list:
            movie_list[self.name] = self.price
            print("Movie added successfully")
        else:
            print("\nMovie already exists")

    @staticmethod
    def movie_view():
        """To view the list of available movies"""
        print("Movies running now")
        cnt = 1
        for i in movie_list:
            print(cnt, "\tMovie Name:", i.ljust(15), "\tPrice", movie_list[i])
            cnt = cnt+1

    def movie_search(self):
        """To search a particular user specified movie"""
        if self.name in movie_list:
            print(self.name, "is currently running")
            print("The ticket price is", movie_list[self.name], "\n")
        else:
            print("\nMovie not available\n")


class Customer(Movie):  # Class customer inherits from class movie -> Single-level inheritances
    """This class is responsible for operation specific to the user that is booking a movie"""
    adm_val = 0

    def __init__(self, c_name=None):
        super().__init__(self)
        self.c_name = c_name

    @classmethod  # This is a class method
    def adm_set(cls):
        """Class method to set the class variable"""
        cls.adm_val = 1

    @classmethod  # This is a class method
    def adm_unset(cls):
        """Class method to unset the class variable"""
        cls.adm_val = 0

    def book_movie(self):
        """To book a particular movie according to the inputs given by the user/admin"""
        movie = input("Choose the movie you wish to watch: ")
        while True:
            try:
                total_ticket = int(input("Enter the total number of seats: "))
                break
            except ValueError:
                print("Invalid input")
        while True:
            if re.match(r'[2-9]', str(total_ticket)):  # Regular expressions
                break
            print("Invalid ticket number")
            while True:
                try:
                    total_ticket = int(input("Re-enter: "))
                    break
                except ValueError:
                    print("Invalid input")
        if movie in movie_list:
            price = movie_list[movie]
            cost = (price.__mul__(total_ticket))  # using magic method mul
            if Customer.adm_val == 1:
                print("Congrats!!!You received admin discount")
                self.c_name = input("Enter your name")
                cost = cost.__sub__(100)  # using magic method sub
            print("Movie booked successfully")
            print("Amount to be paid: ", cost, "\n")
            with open("info.txt", "a") as dat_out:
                dat_out.write("Customer name: "+self.c_name+"\t")
                dat_out.write("Movie booked: "+movie+"\t")
                dat_out.write("Tickets booked: "+str(total_ticket)+"\t")
                dat_out.write("Total cost: "+str(cost)+"\n")
        else:
            print("\nMovie not available")


class Admin(Customer):  # Class admin inherits from Customer -> Multi-level inheritance
    """This class deals with operations that is specific to the admin"""
    @staticmethod  # This is a static method
    def log_in():
        """Static method that handles log-in functionality for the admin"""
        passwd = input("Enter the password for admin log-in: ")
        if passwd == ADM_PSW:
            return 1
        return 0

    @staticmethod
    def view_orders():
        """To view all the movie bookings done till that time"""
        with open("info.txt", "r") as dat_out:
            print(dat_out.read())
            dat_out.close()


def menu():  # This acts as the home screen
    """This acts as the home screen/menu"""
    while True:
        print("Welcome to the home screen\n")
        print("Enter 1 to add a movie")
        print("Enter 2 to view all movies")
        print("Enter 3 to search a movie")
        print("Enter 4 to book tickets")
        print("Enter 5 to view bookings")
        print("Enter any other key to exit\n")
        choice = int(input())
        if choice == 1:
            if Admin.log_in():
                adm = Admin()
                adm.movie_add()
                continue
            print("Wrong admin password")
        elif choice == 2:
            mov = Movie()
            mov.movie_view()
        elif choice == 3:
            movie = input("Enter the movie you want to search: ")
            mov = Movie(movie)
            mov.movie_search()
        elif choice == 4:
            print("Want to view movies as admin or customer")
            opt = int(input("Enter 1 for admin\nEnter 2 for customer"))
            if opt == 1:
                adm = Admin()
                if Admin.log_in():
                    Customer.adm_set()
                    adm.book_movie()
                    Customer.adm_unset()
            elif opt == 2:
                person = input("Enter your name: ")
                cus = Customer(person)
                cus.book_movie()
        elif choice == 5:
            adm = Admin()
            if Admin.log_in():
                adm.view_orders()
                continue
            print("Wrong admin password")
        else:
            break


menu()
