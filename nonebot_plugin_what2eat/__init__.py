from typing import Coroutine, Any
from nonebot import on_command, on_regex
from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import GROUP, GROUP_ADMIN, GROUP_OWNER, Message, MessageEvent, GroupMessageEvent
from nonebot.params import Depends, Arg, ArgStr, CommandArg, RegexMatched
from nonebot.matcher import Matcher
from nonebot.log import logger
from .data_source import eating_manager, Meals
from nonebot import require, get_bot

greeting_helper = require("nonebot_plugin_apscheduler").scheduler
eating_helper = require("nonebot_plugin_apscheduler").scheduler

__what2eat_version__ = "v0.3.0a1"
__what2eat_notes__ = f'''
今天吃什么？ {__what2eat_version__}
[xx吃xx]    问bot恰什么
[添加 xx]   添加菜品至群菜单
[移除 xx]   从菜单移除菜品
[加菜 xx]   添加菜品至基础菜单
[菜单]      查看群菜单
[基础菜单] 查看基础菜单
[开启/关闭小助手] 开启/关闭吃饭小助手
[添加/删除问候 问候语] 添加/删除吃饭小助手问候语'''.strip()

what2eat = on_regex(r"^(今天|[早中午晚][上饭餐午]|早上|夜宵|今晚)吃(什么|啥|点啥)(帮助)?$", priority=15)
group_add = on_command("添加", permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=15, block=True)
group_remove = on_command("移除", permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=15, block=True)
basic_add = on_command("加菜", permission=SUPERUSER, priority=15, block=True)
show_group_menu = on_command("菜单", aliases={"群菜单", "查看菜单"}, permission=GROUP, priority=15, block=True)
show_basic_menu = on_command("基础菜单", permission=GROUP, priority=15, block=True)

greeting_on = on_command("开启吃饭小助手", aliases={"启用吃饭小助手"}, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=15, block=True)
greeting_off = on_command("关闭吃饭小助手", aliases={"禁用吃饭小助手"}, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=15, block=True)
add_greeting = on_command("添加问候", aliases={"添加问候语"}, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=15, block=True)
remove_greeting = on_command("删除问候", aliases={"删除问候语", "移除问候", "移除问候语"}, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=15, block=True)

@what2eat.handle()
async def _(event: MessageEvent, args: str = RegexMatched()):
    # check here
    logger.info(f"Get args: {args}")
    if args[-2:] == "帮助":
        await what2eat.finish(__what2eat_notes__)
    
    msg = eating_manager.get2eat(event)
    await what2eat.finish(msg)

@group_add.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await group_add.finish("还没输入你要添加的菜品呢~")
    elif args and len(args) == 1:
        new_food = args[0]
    else:
        await group_add.finish("添加菜品参数错误~")
    
    msg = eating_manager.add_group_food(new_food, event)

    await group_add.finish(msg)

@basic_add.handle()
async def _(args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await basic_add.finish("还没输入你要添加的菜品呢~")
    elif args and len(args) == 1:
        new_food = args[0]
    else:
        await basic_add.finish("添加菜品参数错误~")

    msg = eating_manager.add_basic_food(new_food)

    await basic_add.finish(msg)

@group_remove.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await group_remove.finish("还没输入你要移除的菜品呢~")
    elif args and len(args) == 1:
        food_to_remove = args[0]
    else:
        await group_remove.finish("移除菜品参数错误~")

    msg = eating_manager.remove_food(event, food_to_remove)

    await group_remove.finish(msg)

@show_group_menu.handle()
async def _(event: GroupMessageEvent):
    gid = str(event.group_id)
    msg = eating_manager.show_group_menu(gid)
    await show_group_menu.finish(msg)

@show_basic_menu.handle()
async def _(matcher: Matcher):
    msg = eating_manager.show_basic_menu()
    await matcher.finish(msg)


# ------------------------- Greetings -------------------------
@greeting_on.handle()
async def _(event: GroupMessageEvent):
    gid = str(event.group_id)
    eating_manager.update_groups_on(gid, True)
    await greeting_on.finish("已开启吃饭小助手~")

@greeting_off.handle()
async def _(event: GroupMessageEvent):
    gid = str(event.group_id)
    eating_manager.update_groups_on(gid, False)
    await greeting_off.finish("已关闭吃饭小助手~")

def parse_greeting(key: str) -> None:
    '''
        Parser the greeting input from user then store in state["greeting"]
    '''
    def _greeting_parser(state: T_State, input_arg: Message = Arg(key)) -> None:
        state["greeting"] = input_arg
    
    return _greeting_parser

def parse_meal(key: str) -> Coroutine[Any, Any, None]:
    '''
        Parser the meal input from user then store in state["meal"]
        If illigal, reject it
    '''
    async def _meal_parser(matcher: Matcher, state: T_State, input_arg: Message = ArgStr(key)) -> None:
        res = eating_manager.which_meals(input_arg)
        if res is None:
            await matcher.reject_arg(key, "输入时段不合法")
        else:
            state["meal"] = res
    
    return _meal_parser

def parse_index(key: str) -> None:
    '''
        Parser the index of greeting to be removed input from user then store in state["index"]
    '''
    async def _index_parser(matcher: Matcher, state: T_State, input_arg: Message = ArgStr(key)) -> None:
        try:
            state["index"] = int(input_arg)
        except Exception:
            await matcher.reject_arg(key, "输入序号不合法")
    
    return _index_parser
        
@add_greeting.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if args and len(args) <= 2:
        res = eating_manager.which_meals(args[0])
        if isinstance(res, Meals):
            matcher.set_arg("meal", args[0])
            if len(args) == 2:
                matcher.set_arg("greeting", args[1])
    
@remove_greeting.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if args:
        res = eating_manager.which_meals(args[0])
        if isinstance(res, Meals):
            matcher.set_arg("meal", args[0])
            msg = eating_manager.show_greetings(res)
            await matcher.send(msg)
    
@add_greeting.got(
    "meal",
    prompt="请输入添加问候语的时段，可选：早餐/午餐/摸鱼/晚餐/夜宵",
    parameterless=[Depends(parse_meal("meal"))]
)
@add_greeting.got(
    "greeting",
    prompt="请输入添加的问候语",
    parameterless=[Depends(parse_greeting("greeting"))]
)
async def handle_add_greeting(matcher: Matcher, meal: Meals = ArgStr(), greeting: str = Arg()):
    msg = eating_manager.add_greeting(meal, greeting)
    await matcher.finish(msg)

@remove_greeting.got(
    "meal",
    prompt="请输入删除问候语的时段，可选：早餐/午餐/摸鱼/晚餐/夜宵",
    parameterless=[Depends(parse_meal("meal"))]
)
async def get_meal_show_greetings(matcher: Matcher, meal: Meals = ArgStr()):
    msg = eating_manager.show_greetings(meal)
    await matcher.send(msg)
    
@remove_greeting.got(
    "index",
    prompt="请输入删除的问候语序号",
    parameterless=[Depends(parse_index("index"))]
)
async def handle_remove_greeting(matcher: Matcher, meal: Meals = ArgStr(), index: int = ArgStr()):
    msg = eating_manager.remove_greeting(meal, index)
    await matcher.finish(msg)


# ------------------------- Schedulers -------------------------
# 重置吃什么次数，包括夜宵
@eating_helper.scheduled_job("cron", hour="6,11,17,22", minute=0, misfire_grace_time=60)
async def _():
    eating_manager.reset_count()
    logger.info("今天吃什么次数已刷新")

# 早餐提醒
@greeting_helper.scheduled_job("cron", hour=7, minute=0, misfire_grace_time=60)
async def time_for_breakfast():
    bot = get_bot()
    msg = eating_manager.get_greeting(Meals.BREAKFAST)
    if msg and len(eating_manager._greetings["groups_id"]) > 0:
        for gid in eating_manager._greetings["groups_id"]:
            if eating_manager._greetings["groups_id"].get(gid, False):
                await bot.send_group_msg(group_id=int(gid), message=msg)
        
        logger.info(f"已群发早餐提醒")

# 午餐提醒
@greeting_helper.scheduled_job("cron", hour=12, minute=0, misfire_grace_time=60)
async def time_for_lunch():
    bot = get_bot()
    msg = eating_manager.get_greeting(Meals.LUNCH)
    if msg and len(eating_manager._greetings["groups_id"]) > 0:
        for gid in eating_manager._greetings["groups_id"]:
            if eating_manager._greetings["groups_id"].get(gid, False):
                await bot.send_group_msg(group_id=int(gid), message=msg)
        
        logger.info(f"已群发午餐提醒")

# 下午茶/摸鱼提醒
@greeting_helper.scheduled_job("cron", hour=15, minute=0, misfire_grace_time=60)
async def time_for_snack():
    bot = get_bot()
    msg = eating_manager.get_greeting(Meals.SNACK)
    if msg and len(eating_manager._greetings["groups_id"]) > 0:
        for gid in eating_manager._greetings["groups_id"]:
            if eating_manager._greetings["groups_id"].get(gid, False):
                await bot.send_group_msg(group_id=int(gid), message=msg)
        
        logger.info(f"已群发摸鱼提醒")

# 晚餐提醒
@greeting_helper.scheduled_job("cron", hour=18, minute=0, misfire_grace_time=60)
async def time_for_dinner():
    bot = get_bot()
    msg = eating_manager.get_greeting(Meals.DINNER)
    if msg and len(eating_manager._greetings["groups_id"]) > 0:
        for gid in eating_manager._greetings["groups_id"]:
            if eating_manager._greetings["groups_id"].get(gid, False):
                await bot.send_group_msg(group_id=int(gid), message=msg)
        
        logger.info(f"已群发晚餐提醒")

# 夜宵提醒
@greeting_helper.scheduled_job("cron", hour=22, minute=0, misfire_grace_time=60)
async def time_for_midnight():
    bot = get_bot()
    msg = eating_manager.get_greeting(Meals.MIDNIGHT)
    if msg and len(eating_manager._greetings["groups_id"]) > 0:
        for gid in eating_manager._greetings["groups_id"]:
            if eating_manager._greetings["groups_id"].get(gid, False):
                await bot.send_group_msg(group_id=int(gid), message=msg)
        
        logger.info(f"已群发夜宵提醒")