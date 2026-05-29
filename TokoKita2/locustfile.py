from locust import HttpUser, task, between

class FlashSaleUser(HttpUser):
    wait_time = between(1, 3)

    @task(8)
    def view_catalogue(self):
        self.client.get("/catalogue")

    @task(2)
    def checkout(self):
        self.client.post("/checkout")