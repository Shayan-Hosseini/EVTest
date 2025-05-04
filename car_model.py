class CarModel:
    def __init__(self, conn):
        self.conn = conn

    def search_car(self, brand=None, model=None):
        cursor = self.conn.cursor()
        if brand and model:
            query = """
                SELECT id, brand, model, bodystyle, seat, priceeuro
                FROM car
                WHERE brand ILIKE %s AND model ILIKE %s
            """
            cursor.execute(query, (f'%{brand}%', f'%{model}%'))
        elif brand:
            query = """
                SELECT id, brand, model, bodystyle, seat, priceeuro
                FROM car
                WHERE brand ILIKE %s
            """
            cursor.execute(query, (f'%{brand}%',))
        elif model:
            query = """
                SELECT id, brand, model, bodystyle, seat, priceeuro
                FROM car
                WHERE model ILIKE %s
            """
            cursor.execute(query, (f'%{model}%',))
        else:
            return []
        return cursor.fetchall()

    def get_performance_info(self, car_id):
        cursor = self.conn.cursor()
        query = """
            SELECT brand, model, accelsec, topspeed_kmh
            FROM car JOIN performance ON performance.id = car.performance_id
            WHERE car.id = %s
        """
        cursor.execute(query, (car_id,))
        return cursor.fetchall()

    def get_battery_info(self, car_id):
        cursor = self.conn.cursor()
        query = """
            SELECT brand, model, fastcharge_kmh, rapidcharge, plugtype, range_id
            FROM car JOIN battery ON battery.id = car.battery_id
            WHERE car.id = %s
        """
        cursor.execute(query, (car_id,))
        return cursor.fetchall()

    def get_range_info(self, range_id):
        cursor = self.conn.cursor()
        query = """
            SELECT brand, model, fastcharge_kmh, rapidcharge, plugtype, powertrain, range_km, efficiency_whkm
            FROM car 
            JOIN battery ON battery.id = car.battery_id
            JOIN carrange ON battery.range_id = carrange.id
            WHERE range_id = %s
        """
        cursor.execute(query, (range_id,))
        return cursor.fetchall()