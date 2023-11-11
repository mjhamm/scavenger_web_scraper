from fractions import Fraction
import re
from decimal import Decimal
from boto3.dynamodb.types import TypeSerializer

# Checks if an ingredient contains a decimal to be changed to a fraction
def checkStringContainsDecimal(string):
    nums = re.findall(r"\d+\.\d+", string)
    return '.'.join(nums)

def doesStringContainDecimal(string):
    return len(re.findall(r"\d+\.\d+", string) != 0)

# converts the decimal to a fraction
def dec_to_proper_frac(dec):
    sign = "-" if dec < 0 else ""
    frac = Fraction(abs(dec))
    return (f"{sign}{frac.numerator // frac.denominator} "
            f"{frac.numerator % frac.denominator}/{frac.denominator}")

def python_obj_to_dynamo_obj(python_obj: dict) -> dict:
    serializer = TypeSerializer()
    return {
        k: serializer.serialize(v)
        for k, v in python_obj.items()
    }

def convert_decimals_to_fractions(input_string):
    def decimal_to_fraction(decimal_str):
        decimal_number = Decimal(decimal_str)
        fraction = Fraction(decimal_number).limit_denominator()

        # Convert to mixed number if the fraction is improper
        if fraction.numerator >= fraction.denominator:
            mixed_number = fraction.numerator // fraction.denominator
            new_numerator = fraction.numerator % fraction.denominator
            fraction_str = f"{mixed_number} {new_numerator}/{fraction.denominator}"
        else:
            fraction_str = str(fraction)

        return fraction_str

    words = input_string.split()
    result = []

    for word in words:
        if '.' in word:
            # Check if the word is a decimal
            try:
                fraction_str = decimal_to_fraction(word)
                result.append(fraction_str)
            except:
                # If conversion fails, keep the original word
                result.append(word)
        else:
            result.append(word)

    return ' '.join(result)
