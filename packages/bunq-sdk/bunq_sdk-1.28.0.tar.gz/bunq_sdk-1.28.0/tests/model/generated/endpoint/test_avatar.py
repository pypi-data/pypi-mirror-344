from typing import AnyStr

from bunq.sdk.http.api_client import ApiClient
from bunq.sdk.model.generated.endpoint import AttachmentPublicApiObject
from bunq.sdk.model.generated.endpoint import AttachmentPublicContentApiObject
from bunq.sdk.model.generated.endpoint import AvatarApiObject
from tests.bunq_test import BunqSdkTestCase


class TestAvatar(BunqSdkTestCase):
    """
    Tests:
        AvatarApiObject
        AttachmentPublicApiObject
        AttachmentPublicContentApiObject
    """

    def test_avatar_creation(self):
        """
        Tests the creation of an avatar by uploading a picture via
        AttachmentPublicApiObject and setting it as avatar via the uuid
        """

        custom_header = {
            ApiClient.HEADER_ATTACHMENT_DESCRIPTION:
                self._ATTACHMENT_DESCRIPTION,
            ApiClient.HEADER_CONTENT_TYPE: self._CONTENT_TYPE
        }
        attachment_public_uuid = AttachmentPublicApiObject.create(self.attachment_contents, custom_header).value
        avatar_uuid = AvatarApiObject.create(attachment_public_uuid).value
        attachment_uuid_after = AvatarApiObject.get(avatar_uuid).value.image[self._FIRST_INDEX].attachment_public_uuid
        file_contents_received = AttachmentPublicContentApiObject.list(attachment_uuid_after).value

        self.assertEqual(self.attachment_contents, file_contents_received)

    @property
    def attachment_contents(self) -> AnyStr:
        with open(self._PATH_ATTACHMENT + self._ATTACHMENT_PATH_IN, self._READ_BYTES) as file:
            return file.read()
