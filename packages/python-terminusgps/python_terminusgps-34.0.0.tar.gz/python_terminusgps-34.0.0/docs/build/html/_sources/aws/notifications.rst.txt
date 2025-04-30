Notifications
=============

.. autoclass:: terminusgps.aws.notifications.AsyncNotificationManager
    :members:
    :special-members:
    :autoclasstoc:

=====
Usage
=====

.. code:: python

    import asyncio
    import uuid

    from terminusgps.aws.notifications import AsyncNotificationManager

    async def main() -> None:
        # Manager requires a group_id
        group_id: str = str(uuid.uuid4())
        message: str = "We know where ours are... do you?"
        async with AsyncNotificationManager(group_id) as manager:
            # Some methods require a message id
            message_id: str = str(uuid.uuid4())

            # Send an sms to one phone number
            # Phone numbers must be in E.164 format
            to_number: str = "+17135555555"
            await manager.send_sms(
                to_number=to_number, message=message, message_id=message_id
            )

            # Send an sms to multiple phone numbers (message ids are automatically generated)
            to_numbers: list[str] = ["+17135555555", "+12815555555", "+18325555555"]
            await manager.send_sms_batch(to_numbers=to_numbers, message=message)

            # Send a push notification to an AWS resource
            target_arn: str = "arn:aws:sns:us-east-1:555555555555:MyAWSResource"
            await manager.send_push(
                target_arn=target_arn, message=message, message_id=message_id
            )

    if __name__ == "__main__":
        asyncio.run(main())
