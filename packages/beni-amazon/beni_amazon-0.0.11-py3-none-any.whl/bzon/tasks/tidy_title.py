from __future__ import annotations

import re
from typing import Final

import pyperclip
import typer
from beni import bcolor, btask
from beni.bfunc import syncCall

app: Final = btask.app


@app.command()
@syncCall
async def tidy_title(
    keys: list[str] = typer.Argument(None, help='关键词')
):
    '使用所有商品报告找出所有的标题，排序输出（使用粘贴板）'
    keys = keys or []
    content = pyperclip.paste()
    lineAry = [(x.split('\t').pop(0), x.split('\t').pop(3)) for x in content.strip().split('\n')]
    # gmc|chevrolet|chevy
    if keys:
        pattern = re.compile(rf'\b({'|'.join(keys)})\b', re.IGNORECASE)
        lineAry = list(filter(lambda x: pattern.search(x[0]) and x[0].endswith(')'), lineAry))
    lineAry = [(re.sub(r'\s*\([^)]*\)$', '', x[0]), x[1]) for x in lineAry]

    lineDict: dict[str, tuple[str, str]] = {}
    for line in lineAry:
        lineDict[line[0]] = line
    lineAry = [x for x in lineDict.values()]
    lineAry.sort(key=lambda x: x[0])

    content = '\n'.join([f'{x[0]}\t\t{x[1]}' for x in lineAry])
    pyperclip.copy(content)
    print(content)
    bcolor.printGreen('OK')
