import json
from faker import Faker

from type_provider import SwaggerProvider


fake = Faker()
fake.add_provider(SwaggerProvider)


class SwaggerParser:
    def __init__(self, swagger_json: dict):
        self.swagger = swagger_json

    def parse(self):
        result = []
        # TODO: Add implementation for query params and body
        # TODO: Refactor this code to reduce loops and use Builder pattern
        for path, method_data in self.swagger["paths"].items():
            for method, data in method_data.items():
                if method == "parameters":
                    for param in data:
                        # TODO: Remove this duplication with refactoring
                        if "path" == param.get("in"):
                            path = path.replace(f'{{{param["name"]}}}', str(getattr(fake, param.get("type"))()))
                    continue
                for param in data.get("parameters", []):
                    if "path" == param.get("in"):
                        path = path.replace(f'{{{param["name"]}}}', str(getattr(fake, param.get("type"))()))
                result.append(
                    {
                        "path": path,
                        "method": method
                    }
                )
        return result


if __name__ == "__main__":
    from pprint import pprint
    with open("./petstore.json", "r") as file:
    # with open("./wallarm.json", "r") as file:
        swagger_json = json.load(file)
        parser = SwaggerParser(swagger_json)
        pprint(parser.parse())