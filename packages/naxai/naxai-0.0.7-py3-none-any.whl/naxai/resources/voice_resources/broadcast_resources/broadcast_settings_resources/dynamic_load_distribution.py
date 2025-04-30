from naxai.models.voice.create_dynamic_load_request import CreateDynamicLoadRequest


class DynamicLoadDistributionResource:
    """
    This class provides methods to interact with the dynamic load distribution settings for a voice broadcast.
    """
    
    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/dynamic-load"
        self.version = "2023-03-25"
        self.headers = {"X-version": self.version,
                        "Content-Type": "application/json"}
        
    def list(self):
        """
        List the dynamic load distribution settings.
        
        Returns:
            dict: The API response containing the dynamic load distributions.
            
        Example:
            >>> dynamic_load_distribution_result = client.voice.broadcasts.settings.dynamic_load_distribution.list()
        """

        return self._client._request("GET", self.root_path, headers=self.headers)
    
    def create(self, data: CreateDynamicLoadRequest):
        """
        Create dynamic load distribution settings.

        Args:
            create_dynamic_load_request (CreateDynamicLoadRequest): The request body containing the dynamic load distribution settings.

        Returns:
            dict: The API response containing the created dynamic load distribution settings.

        Example:
            >>> dynamic_load_distribution_result = client.voice.broadcasts.settings.dynamic_load_distribution.create(
            ...     create_dynamic_load_request=CreateDynamicLoadRequest(
            ...         name: (str)
            ...         maxRate: (int)
            ...     )
            ... )
        """

        return self._client._request("POST", self.root_path, json=data.model_dump(by_alias=True, exclude_none=True), headers=self.headers)

    def get(self, dynamic_load_name: str):
        """
        Get the dynamic load distribution settings by name.

        Args:
            dynamic_load_name (str): The name of the dynamic load distribution settings to get.

        Returns:
            dict: The API response containing the dynamic load distribution settings.

        Example:
            >>> dynamic_load_distribution_result = client.voice.broadcasts.settings.dynamic_load_distribution.get(
            ...     dynamic_load_name="XXXXXXXXX"
            ... )
        """

        return self._client._request("GET", self.root_path + "/" + dynamic_load_name, headers=self.headers)
    
    def update(self, dynamic_load_name: str, data: CreateDynamicLoadRequest):
        """
        Update the dynamic load distribution settings by name.

        Args:
            dynamic_load_name (str): The name of the dynamic load distribution settings to update.
            create_dynamic_load_request (CreateDynamicLoadRequest): The request body containing the updated dynamic load distribution settings.

        Returns:
            dict: The API response containing the updated dynamic load distribution settings.

        Example:
            >>> dynamic_load_distribution_result = client.voice.broadcasts.settings.dynamic_load_distribution.update(
            ...     dynamic_load_name="XXXXXXXXX",
            ...     data=CreateDynamicLoadRequest(
            ...         name: (str)
            ...         maxRate: (int)
            ...     )
            ... )
        """

        return self._client._request("PUT", self.root_path + "/" + dynamic_load_name, json=data.model_dump(by_alias=True, exclude_none=True), headers=self.headers)
    
    def delete(self, dynamic_load_name: str):
        """
        Delete the dynamic load distribution settings by name.

        Args:
            dynamic_load_name (str): The name of the dynamic load distribution settings to delete.

        Returns:
            dict: The API response confirming the deletion of the dynamic load distribution settings.

        Example:
            >>> dynamic_load_distribution_result = client.voice.broadcasts.settings.dynamic_load_distribution.delete(
            ...     dynamic_load_name="XXXXXXXXX"
            ... )
        """

        return self._client._request("DELETE", self.root_path + "/" + dynamic_load_name, headers=self.headers)