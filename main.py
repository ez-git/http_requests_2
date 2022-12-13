import requests
from os import path


class YaUploader:
    def __init__(self, token: str):
        self.token = token
        self.host = 'https://cloud-api.yandex.net:443'

    def get_file_name(self, file_path: str):
        return path.basename(file_path)

    def create_upload_link(self, file_name):
        uri = '/v1/disk/resources/upload'
        headers = {'Authorization': f'OAuth {self.token}'}
        response = requests.get(self.host + uri + '?path=' + file_name, headers=headers)
        json_response = response.json()
        if response.status_code == 200:
            return [response.status_code, json_response['href']]
        else:
            return [response.status_code, json_response['message']]

    def upload_file(self, upload_link, file_path):
        with open(file_path, 'rb') as file_data:
            return requests.put(upload_link, file_data)

    def upload(self, file_path: str):
        file_name = self.get_file_name(file_path)
        upload_link_response = self.create_upload_link(file_name)
        if upload_link_response[0] == 200:
            self.upload_file(upload_link_response[1], file_path)
        else:
            print(upload_link_response[1])


if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    path_to_file = r'D:\image.png'
    token = 'y0_AgAAAAAH2mLYAADLWwAAAADWlCWcN2c_iTa1S-ahghdFUGRcyhpgubk'
    uploader = YaUploader(token)
    uploader.upload(path_to_file)
