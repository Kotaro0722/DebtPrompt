# 【ユーザ用仕様】

## 1. 借金の登録

- 債権者がチャンネルに **【債務者】【金額】【詳細】** の順で記入する。(詳細は被らない内容)(間には必ず空白を入れる)

## 2. 借金の確認

- ~~債務者から検索~~

  - ~~専用のチャンネルに「@借金催促 @債務者」と記入する。~~

  ~~また、@はメンションを示す。~~

  - ~~ボットが「債権者:金額」を債権者の分だけ改行して表示する。~~
  - ~~また、同様のチャンネルに「@借金催促 @債務者　?」と記入すると、すべての債務を表示する。~~

- 債権者から検索
  - 専用のチャンネルに ~~「@借金催促 !@債権者」~~ **「@借金催促」** と記入する。  
    また、@はメンションを示す。  
    ユーザは自分に債権のある借金しか確認できない。
  - ボットが「債務者:金額」を債務者の分だけ改行して表示する。
  - また、同様のチャンネルに ~~「@借金催促 !@債権者　?」と記入すると、すべての債権を表示する。~~  
    **「@借金催促 @債務者」** と記入すると、メンションをした債務者の借金のみを表示する。

## 3. 借金の返済

- 借金の登録で書いたメッセージに ✅ をリアクションとしてつける。
- 今までの借金をすべて返済するときは bot の送ったメッセージに ✅ をリアクションとしてつける。
  - 借金の登録で書いたメッセージに bot が ✅ をつけるため、これにユーザが追加でリアクションを付ける。

## 4. トラブルに関して

- 借金の登録の不備は債権者の責任。
- 借金の返済の不備は債務者の責任。

---

# 【開発者仕様】

## 1. 借金の登録

- ユーザがユーザ用仕様の通りに入力する。
- メンションに反応し、以下の処理を実行する。
- メッセージの送信者を【債権者】、メッセージを空白で分割し【債務者】【金額】【詳細】を取得する。
- データベースにこれらの情報を登録する。

## 2. 借金の確認

- ~~債務者からの検索~~

- ~~ユーザがユーザ用仕様通りに入力する。~~
- ~~メンションに反応し、以下の処理を実行する。~~
- ~~メッセージを分割する。~~
- ~~関数 showDebt()を呼び出し、引数 debtor に分割されたメッセージの二番目を与える。~~
- ~~showDebt()の結果を関数 arrangeDebt()の引数に与える。~~
- ~~arrangeDebt()の結果を 関数 splitDebt()の引数に与える。~~
- ~~splitCredit の結果をそれぞれ改行しながら表示する。~~
- ~~詳細を表示させる場合、関数 showDebt()の結果を表示する。~~

- 債務者からの検索

  - ユーザがユーザ用仕様通りに入力する。
  - メンションに反応し、以下の処理を実行する。
  - メッセージを分割する。
  - 関数 showCredit()を呼び出し、引数 creditor に分割されたメッセージの二番目を与える。
  - showCredit()の結果を関数 arrangeCredit()の引数に与える。
  - arrangeCredit()の結果を 関数 splitCredit()の引数に与える。
  - splitCredit の結果をそれぞれ改行しながら表示する。
  - 詳細を表示させる場合、関数 showCredit()の結果を表示する。

## 3. 借金の返済

- ユーザがユーザ用仕様の通りに入力する。
- リアクションされたメッセージを特定する。
- その後関数 RepayDebt()を呼び出し、引数に【債権者】【債務者】【金額】【詳細】を与える。

- ユーザが bot の送信したメッセージにリアクションを付ける。
- 該当する借金のメッセージにリアクションを付ける。
- ユーザがリアクションを付けたら bot がつけたリアクションを削除する

---

# 【データベースの仕様】

| id | debtor | creditor | amount | isRepay |

- MySQL で実装する
- id は【メッセージ id】を使用する
- debtor,creditor,amount,detail,isRepay は【債務者】【債権者】【金額】【返済済み】と表記する。

---

# 【関数の仕様】

## 1. registerToDB()

- 引数：メッセージの id,債権者の id,債務者の id,金額
- 戻り値：なし
- 処理：
  - MySQL にアクセスする
  - 引数をそれぞれ、id,creditor,debtor,amount とし、返済済みは必ず 0(false)としてデータベースに登録する。
  -

## 2. showDebt()

- 引数：債務者
- 戻り値：データベースに保存されているデータのうち【債務者】が引数と同じもの(List)
- 処理：
  - データベースに接続し、同データベースから「【債務者】=引数」「【返済済み=0】」となるレコードの【債権者】【金額】【詳細】を取得する。
  - 得られたデータを戻り値として与える。

## 3. showCredit()

- 引数：債権者
- 戻り値：データベースに保存されているデータのうち【債権者】が引数と同じもの(List)
- 処理：
  - データベースに接続し、同データベースから「【債権者】=引数」「【返済済み=0】」となるレコードの【債務者】【金額】【詳細】を取得する。
  - 得られたデータを戻り値として与える。

## 4. arrangeList()

- 引数：【債権者 or 債務者】【金額】【詳細】のデータのあるもの(List)
- 戻り値：【債権者 or 債務者】【金額】のデータ(List)
- 処理：
  - 引数のうち、詳細を削除する。
  - 残ったものを戻り値として与える。

## 5. splitList()

- 引数：【債務者 or 債権者】【金額】のデータのあるもの(List)
- 戻り値：債務者 or 債権者:金額の連想配列(object)
- 処理：
  - 引数のうち、債務者 or 債権者ごとに合計の金額を算出する。
  - 得られた連想配列を戻り値として与える。

## 6. searchCheck()

- 引数:メッセージ
- 戻り値:メッセージに"!"が含まれているか(bool)
- 処理：
  - メッセージの内容の文字列を一文字ずつ解析し、いずれかに"!"が含まれていたら True、いなかったら False を返す。

## 7. showHistory()

- 引数:債務者かどうか(bool)、、メッセージ、チャンネルに属している人のリスト
- 戻り値:なし
- 処理:
  - 債務者であった場合、showDebt 関数を呼び出しデータを得る
  - 債権者であった場合、showCredit 関数を呼び出しデータを得る
  - 得たデータを arrangeList 関数に通す。
  - さらに splitList 関数に通す。
  - データをディスコードに投稿する

## 8.getMemberList()

- 引数:メッセージ
- 戻り値:グループに含まれるメンバーのリスト
- 処理:
  - グループに含まれる bot 以外のメンバーを配列に入れ取得する。

## 9.getPatterIsRegister()

- 引数:メッセージ
- 戻り値:正規表現に使用するパターン文字列
- 処理:
  - getMember 関数からメッセージを送った人のグループに属する人のリストを取得する。
  - 取得したリストの値を正規表現の形に書き直す
    - (<@メンバー id>|<@メンバー id>) 金額円
  - 作成した正規表現パターンを返す
