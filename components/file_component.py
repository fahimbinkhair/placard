import os

from components.base_component import BaseComponent


class FileComponent(BaseComponent):
    __table = None

    def __init__(self):
        super().__init__()
        if not FileComponent.__table:
            FileComponent.__table = super()._db.Table('placard_file')

    def add_delete_s3_file_in_placard_file(self, lambda_event: dict) -> dict:
        try:
            event_name = lambda_event['Records'][0]['eventName']
            if event_name not in ['ObjectCreated:Put', 'ObjectCreated:Copy', 'ObjectRemoved:Delete']:
                raise Exception(f"Can not process unknown event: '{event_name}'")

            object_key = lambda_event['Records'][0]['s3']['object']['key']

            if event_name == 'ObjectCreated:Put' or event_name == 'ObjectCreated:Copy':
                file = self.__add_item_in_placard_file(object_key)
            else:
                file = self.__delete_item_from_placard_file(object_key)

            return {'event': event_name, 'file': file}
        except Exception as e:
            raise e

    def __add_item_in_placard_file(self, object_key: str) -> str:
        company_name, file_name, file_ext = self.__extract_s3_object_key(object_key)
        item = {
            'company_name': company_name,
            'file_name': file_name,
            'file_extension': file_ext,
            'image_url': f'https://rijki-placard.s3.eu-west-1.amazonaws.com/{object_key}'
        }
        self.__table.put_item(Item=item)
        return f'{company_name}/{file_name}'

    def __delete_item_from_placard_file(self, object_key: str) -> str:
        company_name, file_name, _ = self.__extract_s3_object_key(object_key)
        key = {
            'company_name': company_name,
            'file_name': file_name
        }
        self.__table.delete_item(Key=key)
        return f'{company_name}/{file_name}'

    @staticmethod
    def __extract_s3_object_key(object_key: str) -> list:
        _, company_name = os.path.dirname(object_key).split('/')
        file_name = file_name_with_ext = os.path.basename(object_key)
        content, file_ext = os.path.splitext(file_name_with_ext)
        supported_file_ext = ['.jpg', '.jpeg', '.gif', '.png']
        if file_ext.lower() not in supported_file_ext:
            raise Exception(f"Can not process file type: '{file_ext}', please upload {supported_file_ext}")

        return [company_name, file_name, file_ext[1:].lower()]

    def get_files(self, company_name: str) -> dict:
        statement = self.__table.query(
            KeyConditionExpression="company_name = :company_name",
            ExpressionAttributeValues={":company_name": company_name}
        )

        files = statement.get('Items')
        if len(files) == 0:
            return {}

        return files
