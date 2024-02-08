# Discord.py チートシート

1. メッセージを送信
   await message.channel.send()

2. メッセージの送信主
   message.author.name

3. メッセージの内容
   message.content

4. 過去のメッセージを取得
   TextChannel.fetch_message(message_id)
   - TextChannel は client.get_channel(channel_id)から取得
   - message_id は message.id から取得
