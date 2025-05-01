import asyncio
import io
from pprint import pprint as pp

from .api.image import get_image_history, get_image_index
from .api.mount import get_equipment_mount_info

from .client import Client
from .models.get_image_history_response_200 import GetImageHistoryResponse200
from .models.get_image_index_response_200 import GetImageIndexResponse200
from .models.get_image_index_bayer_pattern import GetImageIndexBayerPattern
from .models.mount_info import MountInfo
from .types import Response
import base64


# async with client as client:
class NinaAPI:
    def __init__(
        self,
        base_url,
    ):
        self._client = Client(base_url=base_url)

        return None

    async def get_mount_info(self):
        # mount_info: MountInfo = await get_equipment_mount_info.asyncio(client=client)
        response: Response[MountInfo] = await get_equipment_mount_info.asyncio(client=self._client)
        pp(response)

    async def get_latest_image(self):
        image_history: GetImageHistoryResponse200 = await get_image_history.asyncio(client=self._client, count=True)
        image_index_latest = image_history.response - 1
        pp(image_index_latest)

        image: GetImageIndexResponse200 = await get_image_index.asyncio(index=image_index_latest, client=self._client)
        # , debayer=True
        # )  # , bayer_pattern=GetImageIndexBayerPattern.RGGB)

        if image.success:
            decoded_data = base64.b64decode(image.response)

            with open("capture.png", "wb") as file:
                file.write(decoded_data)
