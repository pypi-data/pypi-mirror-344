from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class ValidationResult:
    success: bool
    field_name: str
    note: str
    duplications: Optional[Dict] = None


class ValidationStrategyInterface:

    VALIDATION_OBJECT = None

    @classmethod
    def check_calculation(cls, calculation, calculation_uuid):
        pass

    @classmethod
    def calculate(cls, calculation, field_name, field_value, **kwargs):
        pass

    @classmethod
    def validate(cls, field_name, field_value, **kwargs):
        pass
