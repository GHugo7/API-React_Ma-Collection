"""Schémas du format d'erreur."""

from pydantic import BaseModel

class ErrorDetail(BaseModel):
    code: int
    message: str

class ErrorOut(BaseModel):
    error: ErrorDetail