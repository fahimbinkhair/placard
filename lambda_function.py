import json
from typing import Union

from components.screen_component import ScreenComponent
from helpers.company_helper import CompanyHelper
from helpers.dictionary_helper import DictionaryHelper
from components.file_component import FileComponent
from views import json_view


def lambda_handler(event: dict, context: Union[object, None] = None) -> json:
    try:
        print(event)

        if DictionaryHelper.get_dict_value_by_dot_notation(event, 'Records.0.eventSource') == 'aws:s3':
            result = FileComponent().add_delete_s3_file_in_placard_file(event)
        elif DictionaryHelper.get_dict_value_by_dot_notation(event, 'queryStringParameters.action') == 'list-files':
            company = CompanyHelper.get_company_name_from_event(event)
            result = FileComponent().get_files(company)
        elif DictionaryHelper.get_dict_value_by_dot_notation(event, 'queryStringParameters.action') == 'list-screens':
            company = CompanyHelper.get_company_name_from_event(event)
            result = ScreenComponent().get_screens(company)
        else:
            raise ValueError("Unknown action!!!")

        return json_view(status_code=200, message='Process completed successfully', data=result)
    except Exception as e:
        print(f"Error: {str(e)}")
        return json_view(status_code=500, message=str(e))
