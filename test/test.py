# import re

# message = "@こたろ !@ひろ"
# pattern = "!"
# result = re.search(pattern, message)
# print(result)

import re
address3 = "東京都千代田区 123-7777, 東京都世田谷区 567-9999"
postCodeList = re.findall('[0-9]{3}-[0-9]{4}', address3)
if postCodeList:
    print(postCodeList)
