import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import discord
import pandas as pd

from main_pay import cancel_all_pay_debt, pay_all_debt


def _not_found():
    return discord.NotFound(MagicMock(status=404, reason="Not Found"), "Unknown Message")


# pay_all_debt No.6 / cancel_all_pay_debt No.7
# 1件目の登録メッセージが取得できなくても、全件のDBが更新され、残りのメッセージのリアクションも変更される
@patch("main_pay.client")
@patch("main_pay.cancel_one_pay_debt")
@patch("main_pay.pay_one_debt")
@patch("main_pay.my_select", return_value=pd.DataFrame({"id": [1, 2], "message_id": [9, 9], "debt_id": [111, 222]}))
def test_continue_when_fetch_fails(mock_my_select, mock_pay_one_debt, mock_cancel_one_pay_debt, mock_client):
    for func, mock_one, reaction in [
        (pay_all_debt, mock_pay_one_debt, "add_reaction"),
        (cancel_all_pay_debt, mock_cancel_one_pay_debt, "remove_reaction"),
    ]:
        second_message = MagicMock()
        setattr(second_message, reaction, AsyncMock())
        channel = MagicMock()
        channel.fetch_message = AsyncMock(side_effect=[_not_found(), second_message])

        asyncio.run(func(9, channel))

        assert [c.args[0] for c in mock_one.call_args_list] == [111, 222]
        getattr(second_message, reaction).assert_awaited_once()
