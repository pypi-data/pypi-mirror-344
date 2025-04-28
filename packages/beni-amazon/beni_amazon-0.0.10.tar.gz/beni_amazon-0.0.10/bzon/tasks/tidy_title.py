from __future__ import annotations

from typing import Final

import pyperclip
from beni import btask, bcolor
from beni.bfunc import syncCall

app: Final = btask.app


@app.command()
@syncCall
async def tidy_title():
    '使用所有商品报告找出所有的标题，排序输出（使用粘贴板）'

    ary = pyperclip.paste().split('\n')
    ary = [x.strip() for x in ary]
    ary = list(filter(lambda x: x, ary))
    ary.pop(0)  # 第一行是列字段

    resultAry: list[str] = []
    for line in ary:
        resultAry.append(
            line.split('\t').pop(0)
        )
    resultAry.sort(key=lambda x: x.lower())

    for line in resultAry:
        print(line)

    content = '\n'.join(resultAry)
    pyperclip.copy(content)
    bcolor.printGreen('已复制到剪贴板')
    bcolor.printGreen('OK')
