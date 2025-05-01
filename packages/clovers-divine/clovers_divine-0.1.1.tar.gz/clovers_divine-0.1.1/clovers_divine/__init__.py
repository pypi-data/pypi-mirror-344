import asyncio
from clovers.logger import logger
from .config import config as fortune_config
from .clovers import plugin, Event, Result
from .daily_fortune import Manager as FortuneManager
from .tarot import Manager as TarotManager

fortune_manager = FortuneManager(
    data_path=fortune_config.daily_fortune_data,
    resource_path=fortune_config.daily_fortune_resorce,
    title_font=fortune_config.daily_fortune_title_font,
    text_font=fortune_config.daily_fortune_text_font,
)


@plugin.handle(["今日运势", "抽签", "运势"], ["group_id", "user_id"])
async def _(event: Event):
    group_id = event.group_id
    user_id = event.user_id
    if image := fortune_manager.cache(group_id, user_id):
        text = "你今天在本群已经抽过签了，再给你看一次哦🤗"
    elif result := fortune_manager.get_results(user_id):
        text = "你今天已经抽过签了，再给你看一次哦🤗"
        image = fortune_manager.draw(group_id, user_id, result)
    else:
        text = "✨今日运势✨"
        result = fortune_manager.divine(user_id)
        image = fortune_manager.draw(group_id, user_id, result)
    return [Result("at", user_id), text, image]


tarot_manager = TarotManager(resource_path=fortune_config.tarot_resource)


@plugin.handle(["塔罗牌"], ["user_id"])
async def _(event: Event):
    info, pic, flag = tarot_manager.tarot()
    theme = tarot_manager.random_theme()
    image = tarot_manager.draw(theme, pic, flag)
    return [Result("at", event.user_id), f"回应是{info}", image]


async def segmented_result(result_list: list[Result]):
    for result in result_list:
        yield result
        await asyncio.sleep(2)


def send_tarot_divine(result_list: list[Result]) -> Result: ...


if fortune_config.tarot_merge_forward:
    send_tarot_divine = lambda result_list: Result("merge_forward", result_list)
else:
    send_tarot_divine = lambda result_list: Result("segmented", segmented_result(result_list))


@plugin.handle(["占卜"], ["user_id"])
async def _(event: Event):
    tips, tarot_result_list = tarot_manager.divine()
    await event.send(f"启动{tips}，正在洗牌中...")
    theme = tarot_manager.random_theme()
    result_list = []
    for info, pic, flag in tarot_result_list:
        image = tarot_manager.draw(theme, pic, flag)
        if image:
            result_list.append(Result("list", [Result("text", info), Result("image", image)]))
        else:
            result_list.append(Result("text", info))
    return send_tarot_divine(result_list)


__plugin__ = plugin
