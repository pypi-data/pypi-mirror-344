# openIMIS Backend calcrule_validations reference module

## How we can configure strategy for validation?
* The schema within the `Benefit Plan/Programme` entity holds a crucial role in this process.
* For instance, `validationCalculation` in the schema triggers a specific validation strategy. Similarly, in the duplications section of the schema, 
setting `uniqueness: true` signifies the need for duplication checks based on the record's field value.
* Based on the provided schema below (from `programme/benefit plan`), it indicates that validations will run for the `email` 
field (`validationCalculation`), and duplication checks will be performed for `national_id` (`uniqueness: true`)
```
{
   "$id":"https://example.com/beneficiares.schema.json",
   "type":"object",
   "title":"Record of beneficiares",
   "$schema":"http://json-schema.org/draft-04/schema#",
   "properties":{
      "email":{
         "type":"string",
         "description":"email address to contact with beneficiary",
         "validationCalculation":{
            "name":"EmailValidationStrategy"
         }
      },
      "able_bodied":{
         "type":"boolean",
         "description":"Flag determining whether someone is able bodied or not"
      },
      "national_id":{
         "type":"string",
         "uniqueness":true,
         "description":"national id"
      },
      "educated_level":{
         "type":"string",
         "description":"The level of person when it comes to the school/education/studies"
      },
      "chronic_illness":{
         "type":"boolean",
         "description":"Flag determining whether someone has such kind of illness or not"
      },
      "national_id_type":{
         "type":"string",
         "description":"A type of national id"
      },
      "number_of_elderly":{
         "type":"integer",
         "description":"Number of elderly"
      },
      "number_of_children":{
         "type":"integer",
         "description":"Number of children"
      },
      "beneficiary_data_source":{
         "type":"string",
         "description":"The source from where such beneficiary comes"
      }
   },
   "description":"This document records the details beneficiares"
}
```
* In essence, to create a custom validation rule applicable to a schema field, 
you'll need to define a class in python file within the `strategies` folder 
(The filename should conclude with `_validation_strategy.py`). 
* The example of validation class implementation:
```
from dataclasses import asdict

from calcrule_validations.strategies.base_strategy import BaseValidationsStrategy
from calcrule_validations.strategies.validation_strategy_interface import ValidationResult


class YourCustomValidationStrategy(BaseValidationsStrategy):
    VALIDATION_CLASS = "YourCustomValidationStrategy"

    @classmethod
    def validate(cls, field_name, field_value, **kwargs):
        return asdict(ValidationResult(
            success=False,
            field_name=field_name,
            note="<YOUR VALIDATION NOTE>"
        ))

```
* The `VALIDATION_CLASS` property plays a significant role in defining the value for the `validationCalculation: name` 
property within the JSON schema of the schema for the `Benefit Plan/Programme` entity.
* The validation implementation needs to be executed within the `validate` method. 
It's expected to return a `ValidationResult` as a dictionary structured as follows:
```
    return asdict(ValidationResult(
        success=False,
        field_name=field_name,
        note="<YOUR VALIDATION NOTE>"
    ))
```
* For a valid condition, the expected return should resemble the following:
```
    return asdict(ValidationResult(
        success=True,
        field_name=field_name,
        note="Ok"
    ))
```
* The signature of `validate` method is `def validate(cls, field_name, field_value, **kwargs)`