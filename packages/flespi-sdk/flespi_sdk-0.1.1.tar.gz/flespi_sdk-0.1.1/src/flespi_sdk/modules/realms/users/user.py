from aiohttp import ClientSession
from flespi_sdk.modules.item_with_metadata import ItemWithMetadata


class User(ItemWithMetadata):
    def __init__(
        self,
        realm_id: int,
        user_id: int,
        session: ClientSession,
        cid: int | None = None,
    ):
        """
        Initializes the RealmUsers class with a client instance.

        :param client: The client instance used to make API requests.
        """
        item_path = f"platform/realms/{realm_id}/users/{user_id}"
        super().__init__(
            parent_id=realm_id,
            id=user_id,
            item_path=item_path,
            session=session,
            cid=cid,
        )
