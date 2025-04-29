import asyncio
import uuid
from contextlib import AsyncExitStack

from aiobotocore.session import AioSession

from terminusgps.django.validators import validate_e164_phone_number


class AWSNotifier:
    def __init__(self, region: str = "us-east-1") -> None:
        self._client = None
        self._region = region
        self._exit_stack = AsyncExitStack()

    async def __aenter__(self):
        session = AioSession()
        self._client = await self._exit_stack.enter_async_context(
            session.create_client("sns")
        )

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._exit_stack.__aexit__(exc_type, exc_val, exc_tb)

    async def send_sms(
        self, phone_number: str, message: str, message_id: str, group_id: str
    ) -> dict:
        validate_e164_phone_number(phone_number)
        await self._client.publish(
            **{
                "PhoneNumber": phone_number,
                "Message": message,
                "MessageDeduplicationId": message_id,
                "MessageGroupId": group_id,
            }
        )


async def main() -> None:
    notifier = AWSNotifier()
    message_id = str(uuid.uuid4())
    await notifier.send_sms(
        "+17133049421", "This is a test message", message_id, "message-group"
    )
    return


if __name__ == "__main__":
    asyncio.run(main())
