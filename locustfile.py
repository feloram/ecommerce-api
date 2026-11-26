
from locust import HttpUser, between, task


class StoreUser(HttpUser):

    wait_time = between(1, 2)

    # Read-only test: no user, vendor or product creation.

    @task(4)
    def view_products(self):
        self.client.get(
            "/api/v1/products",
            name="GET /api/v1/products"
        )

    @task(2)
    def view_product_details(self):
        self.client.get(
            "/api/v1/products/1",
            name="GET /api/v1/products/{product_id}"
        )

    @task(1)
    def view_home(self):
        self.client.get(
            "/",
            name="GET /"
        )
