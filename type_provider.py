import random
from faker import Faker
from faker.providers import BaseProvider


class SwaggerProvider(BaseProvider):
    """
     Provider data based on type, described in Swagger file
    """

    def __init__(self, generator):
        super().__init__(generator)

    def integer(self) -> int:
        return random.randint(0, 2 ** 16)

    def string(self):
        return Faker().word()
