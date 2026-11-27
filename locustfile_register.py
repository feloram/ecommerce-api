
import os
import uuid

from locust import HttpUser, between, task


RUN_ID = os.getenv("REGISTER_RUN_ID", "r01")


class RegisterUser(HttpUser):
    wait_time = between(2, 3)

    @task
    def register(self):
        unique_email = (
            f"locust_{RUN_ID}_{uuid.uuid4().hex}@example.com"
        )

        payload = {
            "full_name": "Locust Test User",
            "email": unique_email,
            "password": "TestPassword123"
        }

        with self.client.post(
            "/api/v1/auth/register",
            json=payload,
            name="POST /api/v1/auth/register",
            catch_response=True
        ) as response:

            if response.status_code == 201:
                response.success()
            else:
                response.failure(
                    f"Unexpected status code: {response.status_code}"
                )
