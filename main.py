import tkinter as tk
import psycopg

from user_cars_model import UserCarsModel
from car_model import CarModel
from user_cars_controller import UserCarsController
from car_controller import CarController
from user_cars_view import UserCarsView
from car_view import CarView

def main():
    try:
        conn = psycopg.connect(dbname="final", user="postgres", password="CS330UNR", host="localhost", port="5432")
    except psycopg.OperationalError as e:
        raise ConnectionError(
            "Failed to connect to the PostgreSQL database. Ensure the database is running and credentials are correct."
        ) from e

    # Setup Models With Psycopg
    user_cars_model = UserCarsModel(conn)
    car_model = CarModel(conn)

    # Setup Controllers connection to models
    user_cars_controller = UserCarsController(user_cars_model)
    car_controller = CarController(car_model)

    # Setup Tkinter
    root = tk.Tk()
    root.title("EV Finder")

    # Setup CarView then UserCarsView
    car_view = CarView(root, car_controller)
    user_cars_view = UserCarsView(root, user_cars_controller, car_controller, car_view)

    root.mainloop()

    # Close psycopg
    conn.close()

if __name__ == "__main__":
    main()
