from components.base_component import BaseComponent
from helpers.dictionary_helper import DictionaryHelper


class CompanyComponent(BaseComponent):
    __table = None

    def __init__(self):
        super().__init__()
        if not CompanyComponent.__table:
            CompanyComponent.__table = super()._db.Table('placard_company')

    def check_is_valid_company(self, company_name: str) -> tuple:
        company_info = self.__table.query(
            KeyConditionExpression="company_name = :company_name",
            ExpressionAttributeValues={":company_name": company_name}
        )

        items = company_info.get('Items')
        if len(items) != 1:
            return False, f"The company '{company_name}' seems to be invalid"

        if DictionaryHelper.get_dict_value_by_dot_notation(items, '0.is_active') != 'yes':
            return False, f"The company '{company_name}' seems to be disabled"

        return True, ''
