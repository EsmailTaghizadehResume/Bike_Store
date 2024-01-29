import sqlite3

class Database:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()
        self.create_tables()
    
    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bikes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                serial_number TEXT,
                is_rented INTEGER,
                user_id INTEGER,
                type_bike TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        self.connection.commit()
    
    def close(self):
        self.cursor.close()
        self.connection.close()
    
    def add_user(self, username):
        self.cursor.execute('INSERT INTO users (username) VALUES (?)', (username,))
        self.connection.commit()
    
    def add_bike(self, serial_number, type_bike):
        self.cursor.execute('INSERT INTO bikes (serial_number, is_rented, user_id, type_bike) VALUES (?, 0, NULL, ?)', (serial_number,type_bike))
        self.connection.commit()
    
    def rent_bike(self, bike_id, user_id):
        self.cursor.execute('UPDATE bikes SET is_rented = 1, user_id = ? WHERE id = ?', (user_id, bike_id))
        self.connection.commit()
        return f"user with ID : {user_id} rented bike with ID : {bike_id}"
    
    def return_bike(self, bike_id):
        self.cursor.execute('UPDATE bikes SET is_rented = 0, user_id = NULL WHERE id = ?', (bike_id,))
        self.connection.commit()
        return f"Bike with ID : {bike_id}"
    
    def get_available_bikes(self):
        self.cursor.execute('SELECT * FROM bikes WHERE is_rented = 0')
        return self.cursor.fetchall()
    
    def get_parked_bikes(self):
        self.cursor.execute('SELECT * FROM bikes WHERE is_rented = 1')
        return self.cursor.fetchall()
    
    def get_rented_bikes_by_user(self, user_id):
        self.cursor.execute('SELECT * FROM bikes WHERE is_rented = 1 AND user_id = ?', (user_id,))
        return self.cursor.fetchall()
    
    def get_all_users(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()
    
    def get_all_bikes(self):
        self.cursor.execute('SELECT * FROM bikes')
        return self.cursor.fetchall()
    
    # def load_data(self, user_data, bike_data):
    #     self.cursor.execute('SELECT * FROM users')
    #     self.cursor.execute('SELECT * FROM bikes')
        
    #     for user in user_data:
    #         self.add_user(user)
        
    #     for bike in bike_data:
    #         self.add_bike(bike)
        
    #     self.connection.commit()


class Bike:
    def __init__(self, serial_number):
        self.is_rented = False
        self.serial_number = serial_number

    def rent(self):
        if not self.is_rented:
            self.is_rented = True
            print("Bike rented successfully!")
        else:
            print("This bike is already rented.")

    def return_bike(self):
        if self.is_rented:
            self.is_rented = False
            print("Bike returned successfully!")
        else:
            print("This bike is not rented.")

    def save_bike(self, serrial_number, type_bike):
        data = Database("Bike_Store.db")
        data.add_bike(serrial_number, type_bike)
        return f"bike {serrial_number} added to data base"


class ElectricBike(Bike): 
    def __init__(self, serial_number):
        super().__init__(serial_number)
        self.charge = True

    def charge_bike(self):
        if self.charge:
            print("The bike is already charged.")
        else:
            self.charge = True
            print("The bike is now charged.")

    def discharge_bike(self):
        if not self.charge:
            print("The bike is already discharged.")
        else:
            self.charge = False
            print("The bike is now discharged.")


class RoadBike(Bike):
    def __init__(self, serial_number):
        super().__init__(serial_number)
        self.color = "Orange"

    def change_color(self, color):
        self.color = color
        print(f"The bike color is now {color}.")


class User:
    def __init__(self, username):
        self.username = username
        self.data = Database("Bike_Store.db")
        self.rental_list = []

    def rent_bike(self, bike, user):
        if len(self.rental_list) >= 3:
            print("You have reached the maximum limit of rented bikes (3 bikes).")
        elif bike.is_rented:
            print("This bike is already rented.")
        else:
            self.rental_list.append(bike)
            self.data.rent_bike(bike_id=bike, user_id=user)
            bike.rent()
            print(f"{self.username} has rented bike {bike.serial_number}.")

    def return_bike(self, bike):
        if bike in self.rental_list:
            self.rental_list.remove(bike)
            bike.return_bike()
            print(f"{self.username} has returned bike {bike.serial_number}.")
        else:
            print("This bike is not rented by you.")

    def save_user(self):
        self.data.add_user(self.username)
        return f"User {self.username} added to Database."


def menu():
    print("Menu -->")
    print("1. Available bikes")
    print("2. Parked bikes")
    print("3. Return bike")
    print("4. Rent a bike")
    print("5. Add bikes to inventory")
    print("6. Add new user")
    print("7. List bikes")
    print("8. List users")
    print("9. Exit")
    # print("10. Load Data")
    print("Enter the option: ")

def main():
    data = Database("Bike_Store.db")
    while True:
        menu()
        menu_option = int(input(">>>  "))
        if menu_option == 1:
            for i in data.get_available_bikes():
                print(f"<ID : {i[0]} - SERRISL : {i[1]} - TYPE : Electric Bike - RENT STATUS : {i[2]}>") if i[4] == "E" else print(f"<ID : {i[0]} - SERRISL : {i[1]} - TYPE : Road Bike - RENT STATUS : {i[2]}>") 

        elif menu_option == 2:
            all_Parked_bike = data.get_parked_bikes()
            print()
            for i in all_Parked_bike:
                print(i)
            print()
           
        elif menu_option == 3:
            bike_id = int(input("Enter Bike id : "))
            print(data.return_bike(bike_id=bike_id))

        elif menu_option == 4:
            user_id = int(input("Enter User ID :"))
            bike_id = int(input("Enter a Bike ID :"))
            print(data.rent_bike(user_id=user_id, bike_id=bike_id))

        elif menu_option == 5:
            serial = int(input("Serril of bike : "))
            bike_type = input("ElectricBike Enter E , RoadBike Enter R : ")
            if bike_type == 'E':
                bike_e = ElectricBike(serial)
                print(bike_e.save_bike(serrial_number=serial, type_bike=bike_type))

            elif bike_type == 'R':
                bike_r = RoadBike(serial)
                print(bike_r.save_bike(serrial_number=serial, type_bike=bike_type))

            else:
                print(f"bike type {bike_type} not available . ")

        elif menu_option == 6:
            user_name = input("Enter a user name : ")
            user = User(user_name)
            print(user.save_user())

        elif menu_option == 7:
            for i in data.get_all_bikes():
                print(f"<ID : {i[0]} - SERRISL : {i[1]} - TYPE : Electric Bike - RENT STATUS : {i[2]}>") if i[4] == "E" else print(f"<ID : {i[0]} - SERRISL : {i[1]} - TYPE : Road Bike - RENT STATUS : {i[2]}>") 

        elif menu_option == 8:
            for i in data.get_all_users():
                print(f"<ID : {i[0]} - NAME : {i[1]}>")

        elif menu_option == 9:
            data.close()
            print("Exiting the program...")
            exit()
            
        # elif menu_option == 10:
        #     data.load_data()

        else:
            print("Invalid option. Please enter a valid option.")

if __name__ == "__main__":
    main()
