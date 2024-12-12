from pydantic import BaseModel


class HolderInterface(BaseModel):
    cpf: str
    name: str
    status: bool = True