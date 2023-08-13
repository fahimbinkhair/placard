from components.company_component import CompanyComponent
from helpers.dictionary_helper import DictionaryHelper


class CompanyHelper:
    @staticmethod
    def get_company_name_from_event(event: dict):
        """
        get the name of the company from the AWS event queryStringParameters
        """
        company = DictionaryHelper.get_dict_value_by_dot_notation(event, 'queryStringParameters.company')
        if company is None:
            raise Exception('Please name not provided')

        is_valid, message = CompanyComponent().check_is_valid_company(company)
        if not is_valid:
            raise Exception(message)

        return company

