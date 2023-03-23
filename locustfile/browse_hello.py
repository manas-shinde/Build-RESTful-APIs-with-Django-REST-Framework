from locust import task, HttpUser
from random import randint


class WebsiteUser(HttpUser):
    @task
    def say_hello(self):
        self.client.get('/playground/hello/')

    @task
    def view_product(self):
        product_id = randint(1, 1000)
        self.client.get(
            f'/store/products/{product_id}',
            name='/store/products/:id')
