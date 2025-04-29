from typing import Type
from pydantic import BaseModel


class Attribute(BaseModel):
    value: BaseModel

    @classmethod
    def from_json(cls, json_data: dict, value_model: Type[BaseModel]):
        value = value_model(**json_data["value"]["state"])
        return cls(value=value)

    def to_json(self):
        return self.value.dict()
