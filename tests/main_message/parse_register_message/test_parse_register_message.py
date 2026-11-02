import asyncio
import re
from unittest.mock import AsyncMock, patch

import pytest

from main_message import get_register_pattern, parse_register_message


# No.1 正常系:正の金額
def test_positive_amount():
    assert parse_register_message("<@123> 500円 詳細") == ("123", 500)


# No.2 正常系:マイナスの金額は一部返済として負の整数で返る
def test_negative_amount():
    assert parse_register_message("<@123> -500円 返済") == ("123", -500)


# No.3 正常系:メンションと金額の間に空白が無くても解析できる
def test_without_space():
    assert parse_register_message("<@123>-500円") == ("123", -500)


# No.4 正常系:詳細に含まれる数字は金額として扱われない
def test_numbers_in_detail_are_ignored():
    assert parse_register_message("<@123> -500円 3月分") == ("123", -500)


# No.5 正常系:登録パターンに一致するメッセージは必ず解析できる
@pytest.mark.parametrize(
    "content, expected",
    [
        ("<@123> 500円", ("123", 500)),
        ("<@123> -500円", ("123", -500)),
        ("<@123>-500円 一部返済", ("123", -500)),
    ],
)
@patch("main_message.get_member_list", new_callable=AsyncMock, return_value=[123])
def test_consistent_with_register_pattern(mock_get_member_list, content, expected):
    pattern = asyncio.run(get_register_pattern(message=None))

    assert re.fullmatch(pattern, content)
    assert parse_register_message(content) == expected
