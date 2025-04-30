import re
from typing import Final

import pyperclip
from beni import bcolor, btask
from beni.bfunc import syncCall

app: Final = btask.app


@app.command()
@syncCall
async def take_asin():
    '从Markdown文档内容中获取所有 ASIN（使用剪切板传递数据）'
    content = pyperclip.paste()
    assert content, '剪切板没有内容'

    dataList: list[str] = re.findall(r'\[([0-9A-Z]+)\]', content)
    assert dataList, '没有找到 ASIN'

    # 去除重复的 ASIN，去重后保持原有顺序
    dataList = list(dict.fromkeys(dataList))

    for asin in dataList:
        print(asin)

    content = '  '.join(dataList)
    pyperclip.copy(content)
    bcolor.printGreen('已复制到剪贴板')
    bcolor.printGreen('OK')
