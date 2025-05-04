class CarController:
    def __init__(self, model):
        self.model = model

    def search_ev_by_brand_and_model(self, brand, model):
        return self.model.search_car(brand=brand, model=model)

    def search_ev_by_brand(self, brand):
        return self.model.search_car(brand=brand)

    def search_ev_by_model(self, model):
        return self.model.search_car(model=model)

    def get_performance_info(self, car_id):
        return self.model.get_performance_info(car_id)

    def get_battery_info(self, car_id):
        return self.model.get_battery_info(car_id)

    def get_range_info(self, range_id):
        return self.model.get_range_info(range_id)

    def get_car_details(self, car_id):
        return self.model.get_car_details(car_id)