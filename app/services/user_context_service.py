

class UserContextService:
    """
    Service to manage user context.
    """
    def take_context_json(self, section, data_json):
        """
        Load the context from a JSON file.
        """
        return data_json.get(section, None)
