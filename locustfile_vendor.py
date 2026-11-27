import csv
import os
from pathlib import Path

from locust import HttpUser, between, task
from locust.exception import StopUser


CSV_FILE = Path(__file__).parent / "locust_vendor_users.csv"

USER_OFFSET = int(os.getenv("VENDOR_USER_OFFSET", "0"))

with open(CSV_FILE, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    ALL_USERS = list(reader)

if not ALL_USERS:
    raise ValueError("CSV file has no users")

if "email" not in ALL_USERS[0] or "password" not in ALL_USERS[0]:
    raise ValueError("CSV must contain email and password columns")


TEST_USERS = ALL_USERS[USER_OFFSET:]


USER_ITERATOR = iter(TEST_USERS)


class VendorUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        try:
            self.credentials = next(USER_ITERATOR)
        except StopIteration:
            self.stop()
            return

        with self.client.post(
            "/api/v1/auth/login",
            json={
                "email": self.credentials["email"],
                "password": self.credentials["password"],
            },
            name="POST /api/v1/auth/login [setup]",
            catch_response=True,
        ) as response:

            if response.status_code != 200:
                response.failure(
                    f"Login failed: HTTP {response.status_code}"
                )
                self.stop()
                return

            try:
                data = response.json()
            except ValueError:
                response.failure("Login response is not valid JSON")
                self.stop()
                return

            token = data.get("access_token")

            if not token:
                response.failure("access_token not found")
                self.stop()
                return

            self.token = token

            response.success()

        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }

        self.vendor_done = False

    @task
    def create_vendor(self):
        if self.vendor_done:
            return

        self.vendor_done = True

        unique_name = f"Locust Vendor {self.credentials['email']}"

        with self.client.post(
            "/api/v1/vendors",
            json={
                "name": unique_name,
                "description": "Vendor created for load testing",
            },
            headers=self.headers,
            name="POST /api/v1/vendors",
            catch_response=True,
        ) as response:

            if response.status_code != 201:
                response.failure(
                    f"Vendor creation failed: HTTP {response.status_code}"
                )
                self.stop()
                return

            try:
                data = response.json()
            except ValueError:
                response.failure("Vendor response is not valid JSON")
                self.stop()
                return

            vendor_id = data.get("id")

            if not vendor_id:
                response.failure("Vendor ID not found")
                self.stop()
                return

            self.vendor_id = vendor_id

            response.success()
