import uuid
from calcrule_validations.config import CLASS_RULE_PARAM_VALIDATION, DESCRIPTION_CONTRIBUTION_VALUATION, FROM_TO
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType

from calcrule_validations.strategies import (
    ValidationStrategyStorage
)
from core.abs_calculation_rule import AbsStrategy
from core.signals import *
from core import datetime


class ValidationsCalculationRule(AbsStrategy):
    version = 1
    uuid = "4362f958-5894-435b-9bda-df6cadf88352"
    calculation_rule_name = "Calculation rule: validations"
    description = DESCRIPTION_CONTRIBUTION_VALUATION
    impacted_class_parameter = CLASS_RULE_PARAM_VALIDATION
    date_valid_from = datetime.datetime(2000, 1, 1)
    date_valid_to = None
    status = "pasive"
    from_to = FROM_TO
    type = "validations"
    sub_type = "individual"
    CLASS_NAME_CHECK = ['Individual', 'Beneficiary', 'BenefitPlan']

    signal_get_rule_name = Signal([])
    signal_get_rule_details = Signal([])
    signal_get_param = Signal([])
    signal_get_linked_class = Signal([])
    signal_calculate_event = Signal([])
    signal_convert_from_to = Signal([])

    @classmethod
    def ready(cls):
        now = datetime.datetime.now()
        condition_is_valid = (now >= cls.date_valid_from and now <= cls.date_valid_to) \
            if cls.date_valid_to else (now >= cls.date_valid_from and cls.date_valid_to is None)
        if condition_is_valid:
            if cls.status == "active":
                # register signals getParameter to getParameter signal and getLinkedClass ot getLinkedClass signal
                cls.signal_get_rule_name.connect(cls.get_rule_name, dispatch_uid="on_get_rule_name_signal")
                cls.signal_get_rule_details.connect(cls.get_rule_details, dispatch_uid="on_get_rule_details_signal")
                cls.signal_get_param.connect(cls.get_parameters, dispatch_uid="on_get_param_signal")
                cls.signal_get_linked_class.connect(cls.get_linked_class, dispatch_uid="on_get_linked_class_signal")
                cls.signal_calculate_event.connect(cls.run_calculation_rules, dispatch_uid="on_calculate_event_signal")
                cls.signal_convert_from_to.connect(cls.run_convert, dispatch_uid="on_convert_from_to")

    @classmethod
    def run_calculation_rules(
        cls, sender, instance,
        user, context, **kwargs
    ):
        field_name = kwargs.pop('field_name', None)
        field_value = kwargs.pop('field_value', None)
        return cls.calculate_if_active_for_object(
            instance,
            field_name=field_name,
            field_value=field_value,
            **kwargs
        )

    @classmethod
    def calculate_if_active_for_object(
        cls, instance, calculation_uuid=None, **kwargs
    ):
        if not calculation_uuid:
            return False
        field_name = kwargs.pop('field_name', None)
        field_value = kwargs.pop('field_value', None)
        if cls.active_for_object(instance, calculation_uuid):
            return cls.calculate(instance, field_name, field_value, **kwargs)

    @classmethod
    def active_for_object(cls, instance, calculation_uuid=None):
        if not calculation_uuid:
            return False
        return cls.check_calculation(instance, calculation_uuid)

    @classmethod
    def get_linked_class(cls, sender, class_name, **kwargs):
        return ["Calculation"]

    @classmethod
    def check_calculation(cls, instance, calculation_uuid=None, **kwargs):
        if not calculation_uuid:
            return False
        return ValidationStrategyStorage.choose_strategy(instance).check_calculation(cls, calculation_uuid)

    @classmethod
    def calculate(cls, instance, field_name=None, field_value=None, **kwargs):
        if not field_name:
            return False
        return ValidationStrategyStorage.choose_strategy(instance)\
            .calculate(cls, field_name, field_value, **kwargs)
