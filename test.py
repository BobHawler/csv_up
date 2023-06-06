import unittest
import requests
import json
import os

class FlaskCSVTestCase(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://localhost:5000'
        self.registration_endpoint = '/registration'
        self.upload_endpoint = '/upload'
        self.files_endpoint = '/files'
        self.data_endpoint = '/data'

    def test_registration(self):
        valid_payload = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = requests.post(self.base_url + self.registration_endpoint, json=valid_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['username'], 'testuser')

        # Test registration with missing username
        missing_username_payload = {
            'password': 'testpassword'
        }
        response = requests.post(self.base_url + self.registration_endpoint, json=missing_username_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], 'Enter username and password')

        # Test registration with missing password
        missing_password_payload = {
            'username': 'testuser'
        }
        response = requests.post(self.base_url + self.registration_endpoint, json=missing_password_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], 'Enter username and password')

        # Test registration with an existing username
        existing_username_payload = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = requests.post(self.base_url + self.registration_endpoint, json=existing_username_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], 'This username is already exists')

    def test_upload(self):
        # Upload a file
        file_path = 'test_file.csv'
        with open(file_path, 'w') as file:
            file.write('col1,col2\nvalue1,value2\n')

        file = {'file': open(file_path, 'rb')}
        response = requests.post(self.base_url + self.upload_endpoint, files=file)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'File successfully uploaded')

        # Clean up the uploaded file
        os.remove(file_path)

    def test_get_files(self):
        response = requests.get(self.base_url + self.files_endpoint)
        self.assertEqual(response.status_code, 200)
        files = response.json()
        self.assertIsInstance(files, list)
        for file in files:
            self.assertIn('filename', file)
            self.assertIn('columns', file)

    def test_get_data(self):
        # Upload a file
        file_path = 'test_file.csv'
        with open(file_path, 'w') as file:
            file.write('col1,col2\nvalue1,value2\n')

        file = {'file': open(file_path, 'rb')}
        response = requests.post(self.base_url + self.upload_endpoint, files=file)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'File successfully uploaded')

        # Retrieve data from the uploaded file
        params = {
            'filename': file_path,
            'filter_col': 'col1',
            'filter_val': 'value1',
            'sort_cols': 'col2'
        }
        response = requests.get(self.base_url + self.data_endpoint, params=params)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['col1'], 'value1')
        self.assertEqual(data[0]['col2'], 'value2')

        # Clean up the uploaded file
        os.remove(file_path)


if __name__ == '__main__':
    unittest.main()




# import unittest
# import requests


# class CSVTest_Case(unittest.TestCase):
#     def setUp(self) -> None:
#         self.base_url = 'http://localhost:5000'
#         self.registration_endpoint = '/registration'
#         self.upload_endpoint = '/upload'
#         self.files_endpoint = '/files'
#         self.data_endpoint = '/data'

#     # def test_registration(self):
#     #     valid_payload = {
#     #         'username': 'testuser',
#     #         'password': 'testpassword'
#     #     }
#     #     response = requests.post(self.base_url + self.registration_endpoint, json=valid_payload)
#     #     self.assertEqual(response.status_code, 201)
#     #     self.assertEqual(response.json()['username'], 'testuser')
    
#     # def test_upload(self):
#     #     # Upload a file
#     #     file_path = 'test_file.csv'
#     #     with open(file_path, 'w') as file:
#     #         file.write('col1,col2\nvalue1,value2\n')

#     #     file = {'file': open(file_path, 'rb')}
#     #     response = requests.post(self.base_url + self.upload_endpoint, files=file)
#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertEqual(response.json()['message'], 'File successfully uploaded')

#     #     # Clean up the uploaded file
#     #     os.remove(file_path)
    
#     def test_file_upload(self):
#         # File uploading test
#         files = {'file': open('test_data.csv', 'rb')}
#         response = requests.post(self.base_url + self.upload_endpoint,
#                                  files=files)

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()['message'],
#                          'File successfully uploaded')

#     def test_get_files(self):
#         # Get the list of files test
#         response = requests.get(self.base_url + self.files_endpoint)

#         self.assertEqual(response.status_code, 200)
#         files = response.json()
#         self.assertIsInstance(files, list)
#         self.assertIn('test_data.csv',
#                       [file_info['filename'] for file_info in files])

#     def test_get_data(self):
#         # Get data from a specific file test
#         query_params = {
#             'filename': 'test_data.csv'
#         }
#         response = requests.get(self.base_url + self.data_endpoint,
#                                 params=query_params)

#         self.assertEqual(response.status_code, 200)
#         data = response.json()
#         self.assertIsInstance(data, list)


# if __name__ == '__main__':
#     unittest.main()
