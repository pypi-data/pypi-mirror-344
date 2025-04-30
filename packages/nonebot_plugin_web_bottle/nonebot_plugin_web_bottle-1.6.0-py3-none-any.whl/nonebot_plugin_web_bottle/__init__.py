from datetime import datetime
import re
import json
from nonebot.adapters.onebot.v11 import Message, GroupMessageEvent, Bot
from nonebot.adapters.onebot.v11.helpers import Cooldown
from nonebot.plugin import PluginMetadata
from nonebot.params import CommandArg
from nonebot import on_command
import nonebot
import base64
from .web_bottle import Bottle, id_add, serialize_message
from .to_msg import botte_routing
from .config import Config
from . import data_deal

driver = nonebot.get_driver()
global_config = driver.config
config = Config.parse_obj(global_config)
bottle_msg_split = config.bottle_msg_split
max_bottle_liens = config.max_bottle_liens
max_bottle_word = config.max_bottle_word
max_bottle_pic = config.max_bottle_pic
embedded_help = config.embedded_help
coll_time = config.cooling_time
Config = config

__plugin_meta__ = PluginMetadata(
    name="漂流瓶",
    description="一个基于nonebot2与onebotv11 使用fastapi驱动的漂流瓶插件，有一个简单的web用于审核用户提交的漂流瓶",
    usage="""
    扔瓶子 [图片/文本]
    捡瓶子
    评论漂流瓶 [编号] [文本]
    点赞漂流瓶 [编号]
    """,
    type="application",
    # 发布必填，当前有效类型有：`library`（为其他插件编写提供功能），`application`（向机器人用户提供功能）。
    homepage="https://github.com/luosheng520qaq/nonebot-plugin-web-bottle",
    # 发布必填。
    config=Config,
    supported_adapters={"~onebot.v11"},
    # 支持的适配器集合，其中 `~` 在此处代表前缀 `nonebot.adapters.`，其余适配器亦按此格式填写。
    # 若插件可以保证兼容所有适配器（即仅使用基本适配器功能）可不填写，否则应该列出插件支持的适配器。
)

bottle_help_text = __plugin_meta__.usage

throw = on_command("丢瓶子", aliases={"扔瓶子"}, priority=1, block=True)
get_bottle = on_command("捡瓶子", aliases={"捡漂流瓶"}, priority=1, block=True)
up_bottle = on_command("点赞漂流瓶", priority=1, block=True)
comment = on_command("评论漂流瓶", priority=1, block=True)
read_bottle = on_command("查看漂流瓶", priority=1, block=True)
bottle_help = on_command("漂流瓶", aliases={"漂流瓶菜单"}, priority=1, block=True)


@bottle_help.handle()
async def _():
    await bottle_help.finish(
        "\n漂流瓶使用帮助" + bottle_help_text
    )


@read_bottle.handle()
async def _(bot: Bot, foo: Message = CommandArg()):
    try:
        a = int(foo.extract_plain_text())
    except ValueError:
        await read_bottle.finish("请输入正确的漂流瓶id")
    bottle = Bottle(data_deal.conn_bottle)
    bottle_data = await bottle.get_approved_bottle_by_id(a)
    if bottle_data is None:
        cursor = data_deal.conn_bottle.cursor()
        query = """
            SELECT state
            FROM pending
            WHERE id = ?
        """
        # 执行查询
        cursor.execute(query, (a,))
        # 获取查询结果
        result = cursor.fetchone()
        # 关闭游标
        cursor.close()
        # 返回查询结果，如果没有找到则返回None
        c = result[0]
        if c == 100:  # noqa: PLR2004
            await read_bottle.finish("漂流瓶已拒绝无法查看！")
        elif c == 0:
            await read_bottle.finish("漂流瓶未审核")
        else:
            await read_bottle.finish("发生未知错误！")

    # 处理消息
    messages = await botte_routing(bot, bottle_data, bottle)

    # 发送消息
    for message in messages:
        await read_bottle.send(message)
    await read_bottle.finish()


@comment.handle()
async def _(event: GroupMessageEvent, foo: Message = CommandArg()):
    try:
        a = str(foo).split(maxsplit=1)
        bottle_id = int(a[0])
        text = str(foo)[len(a[0]):].strip()
    except ValueError:
        await comment.finish("请输入正确的漂流瓶id和评论内容")
    except IndexError:
        await comment.finish("请输入评论内容")
    bottle = Bottle(data_deal.conn_bottle)
    a = await bottle.add_comment_if_approved(bottle_id, text, str(event.user_id))
    if not a:
        await comment.send("评论失败，漂流瓶不存在")
    else:
        await comment.send("评论成功！")
    botid = event.self_id
    if str(botid) != '102050518':
        await comment.finish()
    else:
        md = {"keyboard": {"id": "102050518_1725470003"}}
        json1 = json.dumps(md)
        bytes = json1.encode('utf-8')
        data = base64.b64encode(bytes).decode('utf-8')
        await comment.finish(Message(f"[CQ:markdown,data=base64://{data}]"))

@up_bottle.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    try:
        bid = int(args.extract_plain_text())
    except ValueError:
        await up_bottle.finish("请输入正确的漂流瓶id")
    bottle = Bottle(data_deal.conn_bottle)
    a, num = await bottle.up_bottle(bid, str(event.user_id))
    if not a:
        await up_bottle.send("点赞失败，漂流瓶不存在或你已经点赞过了")
    else:
        await up_bottle.send(f"点赞成功,现在有{num}个赞！")
    botid = event.self_id
    if str(botid) != '102050518':
        await up_bottle.finish()
    else:
        md = {"keyboard": {"id": "102050518_1725470003"}}
        json1 = json.dumps(md)
        bytes = json1.encode('utf-8')
        data = base64.b64encode(bytes).decode('utf-8')
        await up_bottle.finish(Message(f"[CQ:markdown,data=base64://{data}]"))

@get_bottle.handle(parameterless=[Cooldown(cooldown=coll_time)])
async def _(bot: Bot,event: GroupMessageEvent):
    bottle = Bottle(data_deal.conn_bottle)
    bottle_data = await bottle.random_get_approves_bottle()
    if not bottle_data:
        await get_bottle.finish("捞瓶子失败，没有漂流瓶~")

    # 处理消息
    messages = await botte_routing(bot, bottle_data, bottle)

    # 发送消息
    for message in messages:
        await get_bottle.send(message)
    botid = event.self_id
    if str(botid) != '102050518':
        await get_bottle.finish()
    else:
        md = {"keyboard": {"id": "102050518_1725470003"}}
        json1 = json.dumps(md)
        bytes = json1.encode('utf-8')
        data = base64.b64encode(bytes).decode('utf-8')
        await get_bottle.finish(Message(f"[CQ:markdown,data=base64://{data}]"))
    await get_bottle.finish()


@throw.handle(parameterless=[Cooldown(cooldown=coll_time)])
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    if not args:
        if embedded_help:
            await throw.finish(f"您还没有写好瓶子的内容哦~\n漂流瓶食用方法：{bottle_help_text}")
        await throw.finish("您还没有写好瓶子的内容哦~")
    else:
        content = args.extract_plain_text().strip()
        if len(content) > max_bottle_word:
            await throw.finish(f"丢瓶子失败啦，请不要超过{max_bottle_word}字符哦~")
        # 匹配 \n, \r\n 和 \r
        newline_pattern = r"[\r\n]+"
        msg = event.get_message()
        if len(re.findall(newline_pattern, content)) > max_bottle_liens:
            await throw.finish(f"丢瓶子失败啦，请不要超过{max_bottle_liens}行内容哦~")
        if sum(1 for seg in msg if seg.type == "image") > max_bottle_pic:
            await throw.finish(f"丢瓶子失败啦，请不要超过{max_bottle_pic}张图片哦~")
        bid = await id_add()
        conn = data_deal.conn_bottle
        await serialize_message(event.get_message(), bid)
        bottle = Bottle(conn)
        time_info = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # TODO)): 统一规定时区 # noqa: DTZ005
        if await bottle.add_pending_bottle(bid, content, str(event.user_id), str(event.group_id), time_info):
            await throw.finish(f"丢瓶子成功！瓶子ID是:{bid}，将在神秘存在审核通过后出现在大海中~")
        else:
            await throw.finish(f"丢瓶子失败啦，出现未知异常")
