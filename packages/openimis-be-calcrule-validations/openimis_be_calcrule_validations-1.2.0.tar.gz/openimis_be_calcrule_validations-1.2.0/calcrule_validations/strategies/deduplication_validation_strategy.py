from dataclasses import asdict

from calcrule_validations.strategies.base_strategy import BaseValidationsStrategy
from calcrule_validations.strategies.validation_strategy_interface import ValidationResult
from social_protection.models import Beneficiary


class DeduplicationValidationStrategy(BaseValidationsStrategy):
    VALIDATION_CLASS = "DeduplicationValidationStrategy"

    @classmethod
    def validate(cls, field_name, field_value, **kwargs):
        benefit_plan = kwargs.get('benefit_plan', None)
        incoming_data = kwargs.get('incoming_data', None)
        # Query existing beneficiaries where is_deleted=False
        existing_beneficiaries = Beneficiary.objects.filter(benefit_plan__id=benefit_plan, is_deleted=False)
        # Check if the field value is duplicated among existing beneficiaries
        duplicates = [
            {
                'id': beneficiary.id,
                'first_name': beneficiary.individual.first_name,
                'last_name': beneficiary.individual.last_name,
                'dob': beneficiary.individual.dob,
                **beneficiary.json_ext  # Unpack all fields from json_ext
            }
            for beneficiary in existing_beneficiaries
            if beneficiary.json_ext.get(f'{field_name}') == field_value
        ]

        # Check for duplication within incoming data
        incoming_duplicates = incoming_data[incoming_data[field_name] == field_value].to_dict('records')
        incoming_duplicates = incoming_duplicates[1:]

        # Flag duplication if duplicates are found
        duplications = None
        if duplicates or len(incoming_duplicates) > 0:
            duplications = {
                'duplicated': True,
                'duplicates_amoung_database': duplicates,
                'incoming_duplicates': incoming_duplicates
            }
            return asdict(ValidationResult(
                duplications=duplications,
                success=False,
                field_name=field_name,
                note=f"'{field_name}' Field value '{field_value}' is duplicated"
            ))
        return asdict(ValidationResult(
            duplications=duplications,
            success=True,
            field_name=field_name,
            note=f"'{field_name}' Field value '{field_value}' is not duplicated"
        ))
