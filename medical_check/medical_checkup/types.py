from dataclasses import dataclass
from typing import NewType

import employee.types


@dataclass
class MedicalCheckUp:
    id: int
    employee: employee.types.Employee
    target_year: int
    conducted_year: int
    conducted_month: int
    need_reexamination: bool
