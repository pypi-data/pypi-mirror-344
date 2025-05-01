from io import BytesIO
from clovers import Event as CloversEvent, Result, Plugin


class Event:
    def __init__(self, event: CloversEvent):
        self.event: CloversEvent = event

    @property
    def command(self) -> str:
        return self.event.raw_command

    @property
    def user_id(self) -> str:
        return self.event.properties["user_id"]

    @property
    def group_id(self) -> str:
        return self.event.properties["group_id"]

    async def send(self, message):
        result = build_result(message)
        if result:
            await self.event.call(result.send_method, result.data)


def build_result(result):
    if isinstance(result, Result):
        return result
    if isinstance(result, str):
        return Result("text", result)
    if isinstance(result, BytesIO):
        return Result("image", result)
    if isinstance(result, list):
        return Result("list", [build_result(seg) for seg in result if seg])


plugin = Plugin(build_event=lambda event: Event(event), build_result=build_result, priority=10)
