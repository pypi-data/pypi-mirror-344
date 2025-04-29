import os

table = {
    "string": "str",
    "double": "float",
    "decimal": "float",
    "long": "float",
}


def make(file):
    with open(file, "r") as f, open(file + ".py", "w") as f2:
        f2.write(
            """from __future__ import annotations
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from ..models import UidStructure, UidNameStructure, ValueDescriptor, SubjectDescriptor\n"""
        )
        for i in f.readlines():
            v = i.strip().split("\t")
            if len(v) == 1:
                f2.write("\nclass " + v[0] + "(BaseModel):\n")
                continue
            a = table.get(v[2], v[2])
            if a.startswith("List"):
                a = "list[" + table.get(a[5:-1], a[5:-1]) + "]"
            if v[1].endswith("AsString"):
                a = "datetime"
                v[1] = v[1].removesuffix("AsString")
            f2.write(
                f'    {v[1]}: Optional[{a}] = Field(alias="{v[0]}", frozen=True)\n'
            )
    os.system(f"py -m isort {file}.py")
    os.system(f"py -m black {file}.py")


make(
    R"C:\Users\vajkh\OneDrive\Desktop\e-kreta-hun0r-2.0\api\utils\mobile_models_source"
)
