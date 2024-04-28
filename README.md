# 借金管理

## 【ユーザ用仕様】

### 1. 借金の登録

- 債権者がチャンネルに **【債務者】【金額】【詳細】** の順で記入する。(詳細は被らない内容)(間には必ず空白を入れる)

### 2. 借金の確認

- 債権者から検索
  - 専用のチャンネルに ~~「@借金催促 !@債権者」~~ **「@借金催促」** と記入する。  
    また、@はメンションを示す。  
    ユーザは自分に債権のある借金しか確認できない。
  - ボットが「債務者:金額」を債務者の分だけ改行して表示する。
  - また、同様のチャンネルに ~~「@借金催促 !@債権者　?」と記入すると、すべての債権を表示する。~~  
    **「@借金催促 @債務者」** と記入すると、メンションをした債務者の借金のみを表示する。
- 詳細の確認
  - Bot が送信したメッセージに ❔ のリアクションを付けると詳細が表示される
    - その合計を計算するのに使用したメッセージへのリンクを作成し表示する
    - 表示するメッセージは「その 1」「その 2」などの連番で行う

### 3. 借金の返済

- 借金の登録で書いたメッセージに ✅ をリアクションとしてつける。
- 今までの借金をすべて返済するときは bot の送ったメッセージに ✅ をリアクションとしてつける。
  - 借金の登録で書いたメッセージに bot が ✅ をつけるため、これにユーザが追加でリアクションを付ける。

### 4. トラブルに関して

- 借金の登録の不備は債権者の責任。
- 借金の返済の不備は債務者の責任。

---

## 【開発者仕様】

### 1. 借金の登録

- ユーザがユーザ用仕様の通りに入力する。
- メンションに反応し、以下の処理を実行する。
- メッセージの送信者を【債権者】、メッセージを空白で分割し【債務者】【金額】【詳細】を取得する。
- データベースにこれらの情報を登録する。

### 2. 借金の確認

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

### 3. 借金の返済

- ユーザがユーザ用仕様の通りに入力する。
- リアクションされたメッセージを特定する。
- その後関数 RepayDebt()を呼び出し、引数に【債権者】【債務者】【金額】【詳細】を与える。

- ユーザが bot の送信したメッセージにリアクションを付ける。
- 該当する借金のメッセージにリアクションを付ける。
- ユーザがリアクションを付けたら bot がつけたリアクションを削除する

---

## 【データベースの仕様】

| id | debtor | creditor | amount | isRepay |

- MySQL で実装する
- id は【メッセージ id】を使用する
- debtor,creditor,amount,detail,isRepay は【債務者】【債権者】【金額】【返済済み】と表記する。

| id |

- sum\_{メッセージの id} で複数用意する

---

## 【関数の仕様】

### 1. registerToDB()

- 引数：メッセージの id,債権者の id,債務者の id,金額
- 戻り値：なし
- 処理：
  - MySQL にアクセスする
  - 引数をそれぞれ、id,creditor,debtor,amount とし、返済済みは必ず 0(false)としてデータベースに登録する。
  -

### 2. showAllCredit()

- 引数:債権者の id,メッセージ
- 戻り値:なし
- 処理:
  - データベースから引数の債権者の債権で未返済のものを取得する
  - 債務者ごとに合計を算出する
  - 債務者ごとに得られた値を表示する
  - 【債務者】が債務者の id、【債権者】が上の債務者、【返済済み】が 0 のものを取得し、createNewTable に渡す

### 3. showOneCredit()

- 引数:債権者の id,債務者の id,メッセージ
- 戻り値:なし
- 処理:
  - データベースからから引数の債務者の債権のうち、引数の債務者で未返済のものを取得する
  - 合計を算出する
  - 得られた値を表示する
  - 【債務者】が債務者の id、【債権者】が上の債務者、【返済済み】が 0 のものを取得し、createNewTable に渡す

### 4. createNewTable()

- 引数:メッセージの id,借金のメッセージの id
- 戻り値:なし
- 処理:
  - sum\_【メッセージの id】の名前でテーブルを作成する
  - このテーブルに【借金のメッセージの id】を追加する

### 5.getMemberList()

- 引数:メッセージ
- 戻り値:グループに含まれるメンバーのリスト
- 処理:
  - グループに含まれる bot 以外のメンバーを配列に入れ取得する。

### 6.getDebtor()

- 引数:メッセージ
- 戻り値:債務者を取得する用の正規表現
- 処理:
  - getMemberList()を呼び出し、リストを取得する
  - 得られたリストを用いて(<@メンバー id>|<@メンバー id>|)の正規表現パターンを生成する

### 7.getPatterIsRegister()

- 引数:メッセージ
- 戻り値:正規表現に使用するパターン文字列
- 処理:
  - getMember 関数からメッセージを送った人のグループに属する人のリストを取得する。
  - 取得したリストの値を正規表現の形に書き直す
    - (<@メンバー id>|<@メンバー id>) 金額円
  - 作成した正規表現パターンを返す

### 8.payOneDebt()

- 引数:メッセージの id
- 戻り値:なし
- 処理:
  - id がメッセージの id のデータの ispay を 1 にする

### 9.payAllDebt()

- 引数:メッセージの id,チャンネル
- 戻り値:なし
- 処理:
  - sum\_【メッセージの id】テーブルからすべてのデータを取得する
  - それぞれの値を payOneDebt()に渡す
  - それぞれの Discord 上のメッセージに ✅ を付ける

### 10.cancelOnePayDebt()

- 引数:メッセージの id
- 戻り値:なし
- 処理:
  - id がメッセージの id のデータの ispay を 0 にする

### 11.cancelAllPayDebt()

- 引数:メッセージの id,チャンネル
- 戻り値:なし
- 処理:
  - sum\_【メッセージの id】テーブルからすべてのデータを取得する
  - それぞれの値を cancelOnePayDebt()に渡す
  - それぞれの Discord 上のメッセージから ✅ を外す

#　課題管理

## 【ユーザ仕様】

### 1.課題期日の登録

- 【タイトル】【期日】のフォーマットで記入する

### 2.課題提出の登録

- 登録したメッセージに ✅ を付ける

### 3.課題未提出のリマインド

- 【期日】の 1 日前に ✅ がついていないスレッドメンバーにメンションする

## 【データベース仕様】

### タスク登録リスト

| message_id | thread_id | deadline |
