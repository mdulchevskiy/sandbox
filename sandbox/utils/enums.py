import pycountry

from django.utils.functional import SimpleLazyObject

from sandbox.utils.timezone import Timezone


class ChoiceEnum(object):
    """
    Base enum class. Use uppercase by convention.

    Sample of usage:
        class ApprovalStatesEnum(ChoiceEnum):
            NEW = 0
            APPROVED = 1
            DECLINED = 2
    """
    messages = {}

    @classmethod
    def for_choice(cls):
        return [(v, k) for k, v in cls.__dict__.items() if k.isupper()]

    @classmethod
    def values(cls):
        return [v for k, v in cls.__dict__.items() if k.isupper()]

    @classmethod
    def get_name(cls, value):
        values_dict = {v: k for k, v in cls.__dict__.items() if k.isupper()}
        try:
            return values_dict[value]

        except KeyError:
            raise ValueError('%s is not defined' % value)

    @classmethod
    def get_value(cls, name):
        names_dict = {k: v for k, v in cls.__dict__.items() if k.isupper()}
        try:
            return names_dict[name]

        except KeyError:
            raise ValueError('%s is not defined' % name)

    @classmethod
    def get_message(cls, value):
        return cls.messages.get(value)


class __CountryEnum(ChoiceEnum):
    def __init__(self):
        pycountry.countries._load()
        for country in pycountry.countries:
            setattr(self.__class__, country.alpha_2, int(country.numeric))

    @classmethod
    def get_full_name(cls, code):
        try:
            country_code = cls.get_name(int(code))
            return pycountry.countries.get(alpha_2=country_code).name

        except Exception:
            return ''


class __CountryDivisionEnum(ChoiceEnum):
    def __init__(self):
        for division in pycountry.subdivisions:
            setattr(self.__class__, division.code.replace('-', '_'), division.code)

    @staticmethod
    def get_full_name(code):
        return pycountry.subdivisions.get(code=code).name if code else ''


class __TimezoneEnum(ChoiceEnum):
    def __init__(self):
        for name in Timezone.objects.values_list('name', flat=True):
            setattr(self.__class__, name.upper().replace('/', '_'), name)


CountryEnum = SimpleLazyObject(lambda: __CountryEnum())
CountryDivisionEnum = SimpleLazyObject(lambda: __CountryDivisionEnum())
TimezoneEnum = SimpleLazyObject(lambda: __TimezoneEnum())
