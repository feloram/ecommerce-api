
import csv
import random
from pathlib import Path
from locust import HttpUser, between, task


CSV_FILE = Path(__file__).parent / "locust_login_users.csv"

with open(CSV_FILE, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    LOGIN_USERS = list(reader)

if not LOGIN_USERS:
    raise ValueError("No login users found in CSV file")


class LoginUser(HttpUser):

    wait_time = between(2, 3)

    def on_start(self):
        self.credentials = random.choice(LOGIN_USERS)

    @task
    def login(self):

        with self.client.post(
            "/api/v1/auth/login",
            json=self.credentials,
            name="POST /api/v1/auth/login",
            catch_response=True
        ) as response:

            if response.status_code != 200:
                response.failure(
                    f"Unexpected status code: {response.status_code}"
                )
                return

            try:
                data = response.json()
            except ValueError:
                response.failure("Response is not valid JSON")
                return

            if not data.get("access_token"):
                response.failure("Access token not found")
                return

            response.success()
