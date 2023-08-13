class DictionaryHelper:
    @staticmethod
    def get_dict_value_by_dot_notation(haystack: dict, needle: str) -> any:
        """
        Retrieve a value from a nested dictionary using dot notation.

        Example:
            haystack = {'body': {'message': 'Found 500 records'}}
            needle = 'body.message'
            value = get_dict_value_by_notation(haystack, needle)
            print(value)  # Output: Found 500 records
        """
        keys = needle.split('.')
        current = haystack
        for key in keys:
            if isinstance(current, dict):
                current = current.get(key)
            elif isinstance(current, list) and key.isdigit():
                index = int(key)
                if 0 <= index < len(current):
                    current = current[index]
                else:
                    return None
            else:
                return None
        return current
