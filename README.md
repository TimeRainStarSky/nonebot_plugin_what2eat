<div align="center">

# What to Eat

<!-- prettier-ignore-start -->
<!-- markdownlint-disable-next-line MD036 -->
_🍔🌮🍜🍮🍣🍻🍩 今天吃什么 🍩🍻🍣🍮🍜🌮🍔_
<!-- prettier-ignore-end -->

</div>

<p align="center">
  
  <a href="https://github.com/MinatoAquaCrews/nonebot_plugin_what2eat/blob/beta/LICENSE">
    <img src="https://img.shields.io/github/license/MinatoAquaCrews/nonebot_plugin_what2eat?color=blue">
  </a>
  
  <a href="https://github.com/nonebot/nonebot2">
    <img src="https://img.shields.io/badge/nonebot2-2.0.0beta.2+-green">
  </a>
  
  <a href="https://github.com/MinatoAquaCrews/nonebot_plugin_what2eat/releases/tag/v0.3.0a1">
    <img src="https://img.shields.io/github/v/release/MinatoAquaCrews/nonebot_plugin_what2eat?color=orange">
  </a>

  <a href="https://www.codefactor.io/repository/github/MinatoAquaCrews/nonebot_plugin_what2eat">
    <img src="https://img.shields.io/codefactor/grade/github/MinatoAquaCrews/nonebot_plugin_what2eat/beta?color=red">
  </a>
  
</p>

</p>

## 版本

v0.3.0a1

⚠ 适配nonebot2-2.0.0beta.2+；

[更新日志](https://github.com/KafCoppelia/nonebot_plugin_what2eat/releases/tag/v0.3.0a1)

## 安装

1. 通过`pip`或`nb`安装；

2. 数据默认位于`./resource`下`eating.json`与`greetings.json`，可通过设置`env`下`WHAT2EAT_PATH`更改；基础菜单、群特色菜单及群友询问Bot次数会记录在该文件中：

    ```python
    WHAT2EAT_PATH="your-path-to-resource"
    ```

## 功能

1. 选择恐惧症？让Bot建议你今天吃什么！

2. ⚠ 插件配置：
   
    ``` python
    WHAT2EAT_PATH="your-path-to-resource"         # 资源路径
    USE_PRESET_MENU=true                          # 是否从repo中下载预置基础菜单，默认为True
    USE_PRESET_GREETINGS=true                     # 是否从repo中下载预置问候语，默认为True
    EATING_LIMIT=99                               # 每个时段吃什么的次数上限，默认5，每日6点、11点、17点、22点自动刷新
    GREETING_GROUPS_ID=["123456789", "987654321"] # 默认开启小助手群组，或{"123456789", "987654321"}
    SUPERUSERS={"12345678"}                       # 同nb超管配置
    ```

3. 群管理可自行添加或移除群特色菜单（`eating.json`下`[group_food][group_id]`）；超管可添加或移除基础菜单（`[basic_food]`）；

4. 各群特色菜单相互独立；各群每个时间段询问Bot建议次数独立；Bot会综合各群菜单+基础菜单给出建议；

5. 提醒吃饭小助手：每天7、12、15、18、22点群发问候语提醒群友按时吃饭/摸鱼，`GROUPS_ID`设置常开的群号列表（或集合），形如：

    ```python
    GREETING_GROUPS_ID=["123456789", "987654321"] # or {"123456789", "987654321"}
    ```

6. 初次使用该插件时，若不存在`eating.json`与`greetings.json`，设置`USE_PRESET_MENU`及`USE_PRESET_GREETINGS`可从仓库中尝试下载；当下载失败会写入初始键值。若存在`eating.json`与`greetings.json`，则对应参数不会生效。

    ```python
    USE_PRESET_MENU=true
    USE_PRESET_GREETINGS=true
    ```

## 命令

1. 吃什么：今天吃什么、中午吃啥、今晚吃啥、中午吃什么、晚上吃啥、晚上吃什么、夜宵吃啥……

2. [管理员或超管] 添加或移除群菜名：[添加/移除 菜名]；

3. 查看群菜单：[菜单/群菜单/查看菜单]；

4. [超管] 添加至基础菜单：[加菜 菜名]；

5. 查看基础菜单：[基础菜单]；

6. [管理员或超管] 开启/关闭吃饭小助手：[开启/启用/关闭/禁用吃饭小助手]；

7. [管理员或超管] 添加/删除吃饭小助手问候语：[添加/删除/移除问候 问候语]；

## 效果

1. 案例1：

    Q：今天吃什么

    A：建议肯德基

    （……吃什么*5）

    Q：今晚吃什么

    A：你今天已经吃得够多了！

    Q：群菜单

    A：

    ---群特色菜单---

    alpha

    beta

    gamma

2. 案例2：

    [群管] Q：添加 派蒙

    A：派蒙 已加入群特色菜单~

    [超管] Q：加菜 东方馅挂炒饭

    A：东方馅挂炒饭 已加入基础菜单~

    [群管] Q：移除 东方馅挂炒饭

    A：东方馅挂炒饭 在基础菜单中，非超管不可操作哦~

## 本插件改自：

[HoshinoBot-whattoeat](https://github.com/pcrbot/whattoeat)

部分菜名参考[程序员做饭指南](https://github.com/Anduin2017/HowToCook)