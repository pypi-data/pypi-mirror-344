import re
from dataclasses import asdict

from calcrule_validations.strategies.base_strategy import BaseValidationsStrategy
from calcrule_validations.strategies.validation_strategy_interface import ValidationResult


class PhoneNumberValidationStrategy(BaseValidationsStrategy):
    VALIDATION_CLASS = "PhoneNumberValidationStrategy"

    @classmethod
    def validate(cls, field_name, field_value, **kwargs) -> ValidationResult:
        if not isinstance(field_value, str):
            return asdict(ValidationResult(
                success=False,
                field_name=field_name,
                note="Field is not a valid phone number"
            ))
        pattern = r"^\+\d{2,3}\d+$"
        is_valid = bool(re.match(pattern, field_value))
        return asdict(ValidationResult(success=True, field_name=field_name, note="Ok")) \
            if is_valid else \
            asdict(ValidationResult(
                success=False,
                field_name=field_name,
                note="Field is not a valid phone number")
            )
