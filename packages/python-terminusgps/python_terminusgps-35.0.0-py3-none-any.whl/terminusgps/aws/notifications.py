import asyncio
import os
import uuid
from collections.abc import Sequence
from contextlib import AsyncExitStack

from aiobotocore.session import AioSession

from terminusgps.django.validators import validate_e164_phone_number


class AsyncPollyManager:
    def __init__(
        self, bucket_name: str | None = None, region_name: str = "us-east-1"
    ) -> None:
        self._exit_stack = AsyncExitStack()
        self._polly_client = None
        self._region_name = region_name
        self._bucket_name = bucket_name or os.getenv("AWS_POLLY_BUCKET_NAME", "")

    @property
    def region_name(self) -> str:
        """
        An AWS region name.

        :type: :py:obj:`str`

        """
        return self._region_name

    @property
    def bucket_name(self) -> str:
        """
        The AWS bucket that will host audio files.

        :type: :py:obj:`str`

        """
        return self._bucket_name

    async def __aenter__(self) -> "AsyncPollyManager":
        """
        Creates an asyncronous session and client.

        :returns: The polly manager.
        :rtype: :py:obj:`~terminusgps.aws.notifications.AsyncPollyManager`

        """
        session = AioSession()
        self._polly_client = await self._exit_stack.enter_async_context(
            session.create_client("polly", region_name=self.region_name)
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Destroys the asyncronous session.

        :param exc_type: Exception type.
        :param exc_val: Exception value.
        :param exc_tb: Exception traceback.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        await self._exit_stack.__aexit__(exc_type, exc_val, exc_tb)

    async def synthesize_speech(
        self,
        message: str,
        format: str = "ogg_vorbis",
        sample_rate: int = 22050,
        language_code: str = "en-US",
    ) -> None:
        """
        Synthesizes the message into an audio file and saves it to the S3 bucket.

        :param message: A message to be read aloud.
        :type message: :py:obj:`str`
        :param format: A file format. Default is ``"ogg_vorbis"``.
        :type format: :py:obj:`str`
        :param sample_rate: The audio frequency in Hz. Default is ``22050``.
        :type sample_rate: :py:obj:`int`
        :param language_code: The language to use in the synthesis. Default is ``"en-US"``.
        :type language_code: :py:obj:`str`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        await self._polly_client.start_speech_synthesis_task(
            **{
                "Engine": "standard",
                "LanguageCode": language_code,
                "OutputFormat": format,
                "OutputS3BucketName": self.bucket_name,
                "SampleRate": str(sample_rate),
                "Text": f"<speak>{message}</speak>",
                "TextType": "ssml",
                "VoiceId": "Joanna",
            }
        )

    async def synthesize_speech_batch(
        self,
        messages: Sequence[str],
        format: str = "ogg_vorbis",
        sample_rate: int = 22050,
        language_code: str = "en-US",
    ) -> None:
        """
        Synthesizes a sequence of messages into audio files and saves them to the S3 bucket.

        :param messages: A sequence of messages to be read aloud.
        :type messages: :py:obj:`Sequence`
        :param format: A file format. Default is ``"ogg_vorbis"``.
        :type format: :py:obj:`str`
        :param sample_rate: The audio frequency in Hz. Default is ``22050``.
        :type sample_rate: :py:obj:`int`
        :param language_code: The language to use in the synthesis. Default is ``"en-US"``.
        :type language_code: :py:obj:`str`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        await asyncio.gather(
            *[
                self.synthesize_speech(
                    message=message,
                    format=format,
                    sample_rate=sample_rate,
                    language_code=language_code,
                )
                for message in messages
            ]
        )


class AsyncNotificationManager:
    def __init__(
        self, group_id: str | None = None, region_name: str = "us-east-1"
    ) -> None:
        """
        Sets :py:attr:`group_id` and :py:attr:`region_name`.

        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self._exit_stack = AsyncExitStack()
        self._sns_client = None
        self._region_name = region_name
        self.group_id = group_id

    async def __aenter__(self) -> "AsyncNotificationManager":
        """
        Creates an asyncronous session and client.

        :returns: The notification manager.
        :rtype: :py:obj:`~terminusgps.aws.notifications.AsyncNotificationManager`

        """
        session = AioSession()
        self._sns_client = await self._exit_stack.enter_async_context(
            session.create_client("sns", region_name=self.region_name)
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Destroys the asyncronous session.

        :param exc_type: Exception type.
        :param exc_val: Exception value.
        :param exc_tb: Exception traceback.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        await self._exit_stack.__aexit__(exc_type, exc_val, exc_tb)

    @property
    def region_name(self) -> str:
        """
        An AWS region name.

        :type: :py:obj:`str`

        """
        return self._region_name

    @property
    def group_id(self) -> str:
        """
        A message group id.

        :type: :py:obj:`str`

        """
        return str(self._group_id)

    @group_id.setter
    def group_id(self, other: str | None) -> None:
        """
        Sets :py:attr:`group_id` to ``other``.

        If ``other`` isn't provided, instead set :py:attr:`group_id` to :py:func:`~uuid.uuid4`.

        :param other: A message group id.
        :type other: :py:obj:`str` | :py:obj:`None`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        if not other:
            other = str(uuid.uuid4())
        self._group_id = other

    async def send_sms(
        self, to_number: str, message: str, message_id: str | None = None
    ) -> None:
        """
        Sends an sms to ``to_number``.

        :param to_number: A destination phone number.
        :type to_number: :py:obj:`str`
        :param message: A message body.
        :type message: :py:obj:`str`
        :param message_id: A message deduplication id. :py:func:`~uuid.uuid4` is used if ``message_id`` was not provided.
        :type message_id: :py:obj:`str` | :py:obj:`None`
        :raises ValidationError: If ``to_number`` wasn't a valid E.164 formatted phone number.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        validate_e164_phone_number(to_number)

        if not message_id:
            message_id = str(uuid.uuid4())

        await self._sns_client.publish(
            **{
                "PhoneNumber": to_number,
                "Message": message,
                "MessageDeduplicationId": message_id,
                "MessageGroupId": self.group_id,
            }
        )

    async def send_push(
        self, target_arn: str, message: str, message_id: str | None = None
    ) -> None:
        """
        Sends a push notification to ``target_arn``.

        :param target_arn: An AWS resource ARN.
        :type target_arn: :py:obj:`str`
        :param message: A message body.
        :type message: :py:obj:`str`
        :param message_id: A message deduplication id. :py:func:`~uuid.uuid4` is used if ``message_id`` was not provided.
        :type message_id: :py:obj:`str` | :py:obj:`None`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        if not message_id:
            message_id = str(uuid.uuid4())

        await self._sns_client.publish(
            **{
                "TargetArn": target_arn,
                "Message": message,
                "MessageDeduplicationId": message_id,
                "MessageGroupId": self.group_id,
            }
        )

    async def send_sms_batch(self, to_numbers: Sequence[str], message: str) -> None:
        """
        Sends an sms message to each phone number in ``to_numbers``.

        :param to_numbers: A sequence of phone numbers.
        :type to_numbers: :py:obj:`~collections.abc.Sequence`
        :param message: A message body.
        :type message: :py:obj:`str`
        :raises ValidationError: If a ``to_number`` wasn't a valid E.164 formatted phone number.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        for to_number in to_numbers:
            validate_e164_phone_number(to_number)

        await asyncio.gather(
            *[self.send_sms(to_number=num, message=message) for num in to_numbers]
        )

    async def send_push_batch(self, target_arns: Sequence[str], message: str) -> None:
        """
        Sends a push notification to each AWS resource by ARN in ``target_arns``.

        :param target_arns: A sequence of AWS resource ARNs.
        :type target_arns: :py:obj:`~collections.abc.Sequence`
        :param message: A message body.
        :type message: :py:obj:`str`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        await asyncio.gather(
            *[self.send_push(target_arn=arn, message=message) for arn in target_arns]
        )
