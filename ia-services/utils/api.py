import requests

class APIClient:
    def __init__(self, base_url, headers=None, timeout=10):
        self.base_url = base_url.rstrip('/')
        self.headers = headers or {}
        self.timeout = timeout

    def get(self, endpoint, params=None, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout, **kwargs)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data=None, json=None, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.post(url, headers=self.headers, data=data, json=json, timeout=self.timeout, **kwargs)
        response.raise_for_status()
        return response.json()

    def update(self, endpoint, data=None, json=None, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.put(url, headers=self.headers, data=data, json=json, timeout=self.timeout, **kwargs)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.delete(url, headers=self.headers, timeout=self.timeout, **kwargs)
        response.raise_for_status()
        return response.json()

# Ejemplo de uso:
# api = APIClient("https://api.example.com", headers={"Authorization": "Bearer TOKEN"})
# response = api.get("users/1")