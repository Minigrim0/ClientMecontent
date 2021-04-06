async def send_error_message(decorator_kwargs, error_msg: str):
    if type(decorator_kwargs) is dict:
        channel = decorator_kwargs["command"].channel
    else:
        print(decorator_kwargs)
        print(type(decorator_kwargs))
        channel = decorator_kwargs["args"]["channel"]

    await channel.send(error_msg)
