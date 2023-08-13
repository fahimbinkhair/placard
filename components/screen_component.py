from components.base_component import BaseComponent


class ScreenComponent(BaseComponent):
    __table = None

    def __init__(self):
        super().__init__()
        if not ScreenComponent.__table:
            ScreenComponent.__table = super()._db.Table('placard_screen')

    def get_screens(self, company_name: str) -> dict:
        statement = self.__table.query(
            KeyConditionExpression="company_name = :company_name",
            FilterExpression="is_active = :is_active",
            ExpressionAttributeValues={
                ':company_name': company_name,
                ':is_active': 'yes'
            }
        )

        screens = statement.get('Items')
        if len(screens) == 0:
            return {}

        return screens
