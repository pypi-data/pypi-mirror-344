import asyncio
import os
from collections.abc import Sequence
from contextlib import AsyncExitStack

from aiobotocore.session import AioSession


class AsyncSpeechSynthesisManager:
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

    async def __aenter__(self) -> "AsyncSpeechSynthesisManager":
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
        :returns: The audio file URI.
        :rtype: :py:obj:`str`

        """
        response = await self._polly_client.start_speech_synthesis_task(
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
        print(f"{response = }")
        return response.get("SynthesisTask", {}).get("OutputUri", "")

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
        :returns: A list of audio file URIs.
        :rtype: :py:obj:`list`

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


async def main() -> None:
    async with AsyncSpeechSynthesisManager() as manager:
        uri = await manager.synthesize_speech(
            "Oh yeah, I'm creating another test audio file."
        )
        print(f"{uri = }")


if __name__ == "__main__":
    asyncio.run(main())
