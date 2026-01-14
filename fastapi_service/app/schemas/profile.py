from pydantic import BaseModel

class Profile(BaseModel):
    name: str
    phone: str
    address: str
