# uvx locust -f scripts/test_locust.py --host http://127.0.0.1:5000

import random
import string
from io import StringIO

from locust import HttpUser, task, between, events
from locust.exception import StopUser


class URLShortenerUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.user_id = None
        self.url_id = None
        self._create_user()
        if self.user_id:
            self._create_url()

    def _create_user(self):
        username = f"loadtest_{self._random_string(8)}"
        email = f"{username}@loadtest.io"
        with self.client.post(
            "/users",
            json={"username": username, "email": email},
            name="/users [create]",
            catch_response=True,
        ) as response:
            if response.status_code == 201:
                try:
                    self.user_id = response.json().get("id")
                    response.success()
                except Exception:
                    response.failure("Invalid JSON response")
            else:
                response.failure(
                    f"Failed to create user: {response.status_code}")

    def _create_url(self):
        if not self.user_id:
            return
        with self.client.post(
            "/urls",
            json={
                "user_id": self.user_id,
                "original_url": f"https://example.com/{self._random_string(10)}",
                "title": f"Load Test URL {self._random_string(6)}",
            },
            name="/urls [create]",
            catch_response=True,
        ) as response:
            if response.status_code == 201:
                try:
                    self.url_id = response.json().get("id")
                    response.success()
                except Exception:
                    response.failure("Invalid JSON response")
            else:
                response.failure(
                    f"Failed to create URL: {response.status_code}")

    @staticmethod
    def _random_string(length=8):
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))

    @task(3)
    def health_check(self):
        with self.client.get("/health", catch_response=True) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get("status") == "ok":
                        response.success()
                    else:
                        response.failure("Unexpected health status")
                except Exception:
                    response.failure("Invalid JSON response")
            else:
                response.failure(
                    f"Health check failed: {response.status_code}")

    @task(5)
    def list_users(self):
        page = random.randint(1, 5)
        per_page = random.choice([10, 20, 50])
        with self.client.get(
            f"/users?page={page}&per_page={per_page}",
            name="/users [list]",
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(
                    f"Failed to list users: {response.status_code}")

    @task(4)
    def get_user_by_id(self):
        if not self.user_id:
            return
        user_ids = [self.user_id] + [random.randint(1, 100) for _ in range(3)]
        target_id = random.choice(user_ids)
        with self.client.get(
            f"/users/{target_id}",
            name="/users/<id> [get]",
            catch_response=True,
        ) as response:
            if response.status_code in (200, 404):
                response.success()
            else:
                response.failure(f"Unexpected status: {response.status_code}")

    @task(3)
    def update_user(self):
        if not self.user_id:
            return
        with self.client.put(
            f"/users/{self.user_id}",
            json={"username": f"updated_{self._random_string(6)}"},
            name="/users/<id> [update]",
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(
                    f"Failed to update user: {response.status_code}")

    @task(6)
    def list_urls(self):
        params = ""
        if random.random() > 0.5 and self.user_id:
            params = f"?user_id={self.user_id}"
        with self.client.get(
            f"/urls{params}",
            name="/urls [list]",
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(
                    f"Failed to list URLs: {response.status_code}")

    @task(5)
    def get_url_by_id(self):
        if not self.url_id:
            return
        url_ids = [self.url_id] + [random.randint(1, 100) for _ in range(3)]
        target_id = random.choice(url_ids)
        with self.client.get(
            f"/urls/{target_id}",
            name="/urls/<id> [get]",
            catch_response=True,
        ) as response:
            if response.status_code in (200, 404):
                response.success()
            else:
                response.failure(f"Unexpected status: {response.status_code}")

    @task(4)
    def update_url(self):
        if not self.url_id:
            return
        with self.client.put(
            f"/urls/{self.url_id}",
            json={
                "title": f"Updated Title {self._random_string(5)}",
                "is_active": random.choice([True, False]),
            },
            name="/urls/<id> [update]",
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(
                    f"Failed to update URL: {response.status_code}")

    @task(2)
    def list_events(self):
        with self.client.get(
            "/events",
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(
                    f"Failed to list events: {response.status_code}")

    @task(1)
    def create_user_new(self):
        username = f"newuser_{self._random_string(8)}"
        email = f"{username}@test.io"
        with self.client.post(
            "/users",
            json={"username": username, "email": email},
            name="/users [create]",
            catch_response=True,
        ) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure(
                    f"Failed to create user: {response.status_code}")

    @task(2)
    def create_url_new(self):
        if not self.user_id:
            return
        with self.client.post(
            "/urls",
            json={
                "user_id": self.user_id,
                "original_url": f"https://example.com/{self._random_string(10)}",
                "title": f"Test URL {self._random_string(6)}",
            },
            name="/urls [create]",
            catch_response=True,
        ) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure(
                    f"Failed to create URL: {response.status_code}")
