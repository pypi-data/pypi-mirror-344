<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-ciku

_✨ NoneBot 插件描述 ✨_

这是一个 onebot.v11的词库语言插件
</div>

## 📖 介绍

词库插件方面：

面向小白的词库语言插件,目的是减少编写代码的时间和难度 特点:语言精简（应该） 无需重启nb和reload即可实
现功能热重载 缺点:目前仅能实现一些简单的逻辑运行,但随着更新肯定会慢慢削减

支持导入自定义解析规则（自定义的优先级较低，请注意是否与默认规则冲突）

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot_plugin_ciku

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot_plugin_ciku
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_ciku"]

</details>

## ⚙️ 说明

词库文件(dicpro.ck)和自定义拓展文件夹都会在初次使用时自动创建

项目还在持续优化，暂时不开放env配置相关

# ⚙️ webui

为方便用户使用，本插件自带webui
具体路径为 你nonebot的ws链接地址:端口/ck_webui
例如:http://127.0.0.1:8090/ck_webui
后续会将变量大全等教程转移到webui里面

<details open>
<summary>变量大全</summary>
目前支持的变量(\是md转译问题，忽略就行):

| 变量 | 说明 |
|:-----:|:----:|
| %QQ% | 用户id |
| %群号% | 群号 |
| %BotQQ% | 机器人自己的QQ |
| %括号n% | 从0开始匹配正则，提取对应字段 |
| %ATn% | 从0开始，提取艾特对应的对象QQ号 |
| [[11*50]/6+5*[50+6-7*8]] | 如果被包裹的不是数组，优先被识别为计算式，如果不符合计算式，才是正常字符串 |
| \\$读 路径 键 默认值\\$ | 读文件 |
| \\$写 路径 键 值\\$ | 写文件 |
| \\$调用 名称\\$| 调用对应语块，若有消息字符串单独发出（例子见下，调用的语块前必须有[内部]） |
| \\$回调 名称\\$ | 调用对应语块，若有消息字符串则合并到对应位置一起发出（例子见下，调用的语块前必须有[内部]） |
| ±at QQ号± | 艾特用户 |
| ±img 路径/链接± | 发送图片 |
| ±reply 0± | 回复指令消息 |
| @%a%['data'] | 比如你前面写了a:{'data':1},那么为1 |

</details>

## 🎉 使用
### 词库格式
```bash
测试
路径:/词库项目/qrbot/src/plugins/词库v2/
name:['123']
a:$读 %路径%send.txt a 0$
b:$读 %路径%send.txt b 0$
c:$读 %路径%send.txt c 123$
d:±img bug.png±
$写 %路径%send.txt c 哈哈哈$
±reply 0±
%a%《隔断》%b%%c%\n±at %QQ%±\n456789
±img https://homdgcat.wiki/images/emote/Yunli/1.png±
%d%
如果:1 > 2
$读 %路径%send.txt c wdnmd$
如果:%a% == %a%
变量测试成功@%name%[0]
如果尾
如果尾
如果:%a% == %a%
缩进测试成功

测试访问
a:$访问 https://api.tangdouz.com/a/steam.php?return=json$ //默认get方法
$访问 url 请求头$
$访问 get url 请求头$
$访问 post url 请求头 json$   //请求头和json没有就填None
@%a%['store']


测试json
name:['123']
data:{'a':'123','b':'456'}
test:{'a':['123']}
@%name%[0]\n
@%data%['b']\n
@%test%['a'][0]

循环测试
测试:1
循环:%i% in 5
测试:[%测试% + %i%]
%测试%\n
循环尾
%测试%\n[1+5*%测试%]

(.*)测试正则(.*)
测试成功\n%括号0%

.*测试艾特
%AT1%\n%BotQQ%
$回调 测试调用$
$调用 测试调用$


[内部]测试调用
测试成功
```

### 自定义拓展

webui里找到拓展编辑，新建py文件，这里是示例

```bash
# example.py

from abc import ABC, abstractmethod

class ParseRule(ABC):
    @abstractmethod
    def match(self, line: str, event,tab_time:int,arg_list:list,async_def_list:list) -> bool:
        pass

    @abstractmethod
    def process(self, line: str, event,tab_time:int,arg_list:list,async_def_list:list) -> str:
        pass
import re

class EmojiRule(ParseRule):
    """示例第三方规则：替换表情符号"""
    
    def match(self, line, event,tab_time,arg_list,async_def_list) -> bool:
        return re.search(r'#\w+#', line) is not None
    
    def process(self, line, event,tab_time,arg_list,async_def_list) -> str:
        line = line.replace('#smile#', '😊')
        line = line.replace('#angry#', '😠')
        return f'{line}', tab_time

```