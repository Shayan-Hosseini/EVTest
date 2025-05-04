#import psycopg

class UserCarsModel:
    def __init__(self, conn):
        self.conn = conn

    def add_user_car(self, brand, model):
        cursor = self.conn.cursor()
        query = "INSERT INTO user_cars (brand, model) VALUES (%s, %s)"
        cursor.execute(query, (brand, model))
        self.conn.commit()

    def get_user_cars(self):
        cursor = self.conn.cursor()
        query = "SELECT id, brand, model FROM user_cars"
        cursor.execute(query)
        return cursor.fetchall()

    def delete_user_car(self, car_id):
        cursor = self.conn.cursor()
        query = "DELETE FROM user_cars WHERE id = %s"
        cursor.execute(query, (car_id,))
        self.conn.commit()