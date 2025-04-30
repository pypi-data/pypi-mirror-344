import importlib
import inspect

from calcrule_validations.strategies.base_strategy import BaseValidationsStrategy


class ValidationStrategyStorage:

    BASE_CLASS = BaseValidationsStrategy
    MODULE_NAME = "calcrule_validations.strategies"

    @classmethod
    def choose_strategy(cls, validation_class):
        module = importlib.import_module(cls.MODULE_NAME)
        for name, class_object in inspect.getmembers(module, inspect.isclass):
            if issubclass(class_object, cls.BASE_CLASS) and class_object != cls.BASE_CLASS:
                if validation_class == class_object.VALIDATION_CLASS:
                    return class_object
