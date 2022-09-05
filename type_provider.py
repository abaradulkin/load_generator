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
        # TODO: add additional field to swagger.json to have possibility generate values more personally
        # As example, has next fields: id, hash, name and etc
        return random.randint(0, 2 ** 16)

    def string(self):
        return Faker().word()
