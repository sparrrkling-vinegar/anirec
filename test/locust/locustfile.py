import random
from locust import HttpUser, task, between


def random_username(n: int):
    username = ''.join([chr(random.randint(ord('a'), ord('z'))) for _ in range(n)])
    return username


class WikiFetUser(HttpUser):
    wait_time = between(1, 2)
    username = 'user'

    @task
    def sign_up(self):
        self.username = random_username(20)
        self.client.post("/signup", data={
            "username": self.username,
            "password": "StrongPassword123!"
        })

    @task
    def sign_in(self):
        self.client.post("/signin", data={
            "username": self.username,
            "password": "StrongPassword123!"
        })
