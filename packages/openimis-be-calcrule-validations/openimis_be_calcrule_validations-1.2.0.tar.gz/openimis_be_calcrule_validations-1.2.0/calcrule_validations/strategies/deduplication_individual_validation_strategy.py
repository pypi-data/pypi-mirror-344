from dataclasses import asdict
from django.db.models import F

from calcrule_validations.strategies.base_strategy import BaseValidationsStrategy
from calcrule_validations.strategies.validation_strategy_interface import ValidationResult
from individual.models import Individual


class DeduplicationIndividualValidationStrategy(BaseValidationsStrategy):
    VALIDATION_CLASS = "DeduplicationIndividualValidationStrategy"

    @classmethod
    def validate(cls, field_name, field_value, **kwargs):
        incoming_data = kwargs.get('incoming_data', None)
        existing_individuals = (
            Individual.objects.filter(is_deleted=False).annotate(
                json_value=F('json_ext__' + field_name)).filter(json_value=field_value)
        )

        duplicates = [
            {
                'id': individual.id,
                'first_name': individual.first_name,
                'last_name': individual.last_name,
                'dob': individual.dob,
                **individual.json_ext  # Unpack all fields from json_ext
            }
            for individual in existing_individuals
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
