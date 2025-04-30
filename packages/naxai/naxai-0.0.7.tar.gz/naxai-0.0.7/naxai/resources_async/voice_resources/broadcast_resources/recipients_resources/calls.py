class CallsResource:
    """
    This class represents the CallsResource, which provides methods to interact with the broadcast recipients calls API.
    """

    def __init__(self, client, root_path: str):
        self._client = client
        self.root_path = root_path
        self.version = "2023-03-25"
        self.headers = {"X-version": self.version,
                        "Content-Type": "application/json"}
        
    async def list(self, broadcast_id: str, recipient_id: str):
        """
        Get the recipient calls for a voice broadcast by broadcast id and recipient id.

        Args:
            broadcast_id (str): The unique identifier of the broadcast to cancel.
            recipients_id (str): The unique identifier of the recipient

        Returns:
            dict: The API response containing the calls.

        Example:
            >>> recipients_result = await client.voice.broadcasts.recipients.calls.list(
            ...     broadcast_id="XXXXXXXXX",
            ...     recipient_id="XXXXXXXXX"
            ... )
        """

        return await self._client._request("GET", self.root_path + "/" + broadcast_id + "/recipients/" + recipient_id + "/calls", headers=self.headers)