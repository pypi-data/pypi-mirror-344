class HolidaysTemplatesResource:

    def __init__(self, client, root_path):
            self._client = client
            self.root_path = root_path + "/holidays"
            self.version = "2023-03-25"
            self.headers = {"X-version": self.version,
                            "Content-Type": "application/json"}
            
    async def get(self, template_id: str):
        """
        Retrieves a specific holiday template by its ID.

        Args:
            template_id (str): The ID of the holiday template to retrieve.

        Returns:
            dict: The API response containing the details of the requested holiday template.

        Example:
            >>> template = await client.calendars.holidays_templates.get("template_id")
        """
        return await self._client._request("GET", self.root_path + "/" + template_id, headers=self.headers)
            
    async def list(self):
        """
        Retrieves a list of holiday templates.

        Returns:
            dict: The API response containing the list of holiday templates.

        Example:
            >>> templates = await client.calendars.holidays_templates.list()
        """
        return await self._client._request("GET", self.root_path, headers=self.headers)