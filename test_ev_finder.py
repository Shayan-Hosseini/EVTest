import unittest
from unittest.mock import patch, MagicMock
from user_cars_model import UserCarsModel
from user_cars_controller import UserCarsController
from car_model import CarModel
from car_controller import CarController

class TestEVFinder(unittest.TestCase):

    def setUp(self):
        # Setup mock objects and initial configurations
        self.mock_db_connection = MagicMock()
        self.user_cars_model = UserCarsModel(self.mock_db_connection)
        self.user_cars_controller = UserCarsController(self.user_cars_model)
        self.car_model = CarModel(self.mock_db_connection)
        self.car_controller = CarController(self.car_model)

    # Unit Tests for UserCarsModel
    @patch('psycopg.connect')
    def test_add_user_car(self, mock_connect):
        mock_connect.return_value = self.mock_db_connection
        self.user_cars_model.add_user_car('Tesla', 'Model S')
        self.mock_db_connection.cursor().execute.assert_called_once()

    @patch('psycopg.connect')
    def test_delete_user_car(self, mock_connect):
        mock_connect.return_value = self.mock_db_connection
        self.user_cars_model.delete_user_car(1)
        self.mock_db_connection.cursor().execute.assert_called_once()

    @patch('psycopg.connect')
    def test_get_user_cars(self, mock_connect):
        mock_connect.return_value = self.mock_db_connection
        self.user_cars_model.get_user_cars()
        self.mock_db_connection.cursor().execute.assert_called_once_with('SELECT id, brand, model FROM user_cars')

    # Unit Tests for UserCarsController
    def test_get_user_evs(self):
        self.user_cars_model.get_user_cars = MagicMock(return_value=[{'id': 1, 'brand': 'Tesla', 'model': 'Model 3'}])
        result = self.user_cars_controller.get_user_evs()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['brand'], 'Tesla')

    # Unit Tests for CarModel
    @patch('psycopg.connect')
    def test_search_car(self, mock_connect):
        mock_connect.return_value = self.mock_db_connection
        self.car_model.search_car(brand='Tesla')
        self.mock_db_connection.cursor().execute.assert_called_once()

    # Integration Tests
    def test_user_cars_controller_integration(self):
        self.user_cars_model.add_user_car = MagicMock()
        self.user_cars_controller.log_ev('Tesla', 'Model X')
        self.user_cars_model.add_user_car.assert_called_once_with('Tesla', 'Model X')

    def test_car_controller_integration(self):
        self.car_model.search_car = MagicMock(return_value=[{'brand': 'Nissan', 'model': 'Leaf'}])
        result = self.car_controller.search_ev_by_brand('Nissan')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['brand'], 'Nissan')

    def test_user_cars_controller_delete_integration(self):
        self.user_cars_model.delete_user_car = MagicMock()
        self.user_cars_controller.delete_ev(1)
        self.user_cars_model.delete_user_car.assert_called_once_with(1)

    def test_car_controller_get_details_integration(self):
        self.car_model.get_car_details = MagicMock(return_value={'id': 1, 'brand': 'Tesla', 'model': 'Model S'})
        result = self.car_controller.get_car_details(1)
        self.assertEqual(result['brand'], 'Tesla')
        self.assertEqual(result['model'], 'Model S')

    # Additional Unit Tests for CarController
    def test_search_ev_by_brand_and_model(self):
        self.car_model.search_car = MagicMock(return_value=[{'brand': 'Tesla', 'model': 'Model S'}])
        result = self.car_controller.search_ev_by_brand_and_model('Tesla', 'Model S')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['brand'], 'Tesla')
        self.assertEqual(result[0]['model'], 'Model S')

    def test_search_ev_by_model(self):
        self.car_model.search_car = MagicMock(return_value=[{'brand': 'Tesla', 'model': 'Model 3'}])
        result = self.car_controller.search_ev_by_model('Model 3')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['model'], 'Model 3')

    def test_get_performance_info(self):
        self.car_model.get_performance_info = MagicMock(return_value=[{'accelsec': 4.6, 'topspeed_kmh': 233}])
        result = self.car_controller.get_performance_info(1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['accelsec'], 4.6)

    def test_get_battery_info(self):
        self.car_model.get_battery_info = MagicMock(return_value=[{'fastcharge_kmh': 940, 'plugtype': 'Type 2 CCS'}])
        result = self.car_controller.get_battery_info(1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['fastcharge_kmh'], 940)

    def test_get_range_info(self):
        self.car_model.get_range_info = MagicMock(return_value=[{'range_km': 450, 'efficiency_whkm': 161}])
        result = self.car_controller.get_range_info(5)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['range_km'], 450)

    # Additional Unit Tests for UserCarsController
    def test_log_ev(self):
        self.user_cars_model.add_user_car = MagicMock()
        result = self.user_cars_controller.log_ev('Tesla', 'Model Y')
        self.user_cars_model.add_user_car.assert_called_once_with('Tesla', 'Model Y')
        self.assertEqual(result, "Electric vehicle logged successfully.")

    def test_delete_user_ev(self):
        self.user_cars_model.delete_user_car = MagicMock()
        result = self.user_cars_controller.delete_user_ev(1)
        self.user_cars_model.delete_user_car.assert_called_once_with(1)
        self.assertEqual(result, "Entry deleted.")

if __name__ == '__main__':
    unittest.main()