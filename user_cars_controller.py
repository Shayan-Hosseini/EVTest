class UserCarsController:
    def __init__(self, model):
        self.model = model

    def log_ev(self, brand, model):
        self.model.add_user_car(brand, model)
        return "Electric vehicle logged successfully."

    def get_user_evs(self):
        return self.model.get_user_cars()

    def delete_user_ev(self, car_id):
        self.model.delete_user_car(car_id)
        return "Entry deleted."

    def delete_ev(self, car_id):
        return self.delete_user_ev(car_id)