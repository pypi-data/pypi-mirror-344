from __future__ import annotations

from pydantic import BaseModel, Field


class UidNameStructure(BaseModel):
    name: str = Field(alias="Nev", frozen=True)
    uid: str = Field(alias="Uid", frozen=True)


class UidStructure(BaseModel):
    uid: str = Field(alias="Uid", frozen=True)


class ValueDescriptor(BaseModel):
    description: str = Field(alias="Leiras", frozen=True)
    name: str = Field(alias="Nev", frozen=True)
    uid: str = Field(alias="Uid", frozen=True)


class SubjectDescriptor(BaseModel):
    name: str = Field(alias="Nev", frozen=True)
    subjectCategory: ValueDescriptor = Field(alias="Kategoria", frozen=True)
    uid: str = Field(alias="Uid", frozen=True)
