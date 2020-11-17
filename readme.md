# connpassのイベントのキャンセル人数を粗く見積もるスクリプト

## 必要なpythonパッケージのインストール
- `$ pip install -r requirements.txt`

## 使い方
- `$ python estimate_number_of_cancellation.py <event_url>`
    - event_url: connpassのイベントページのURL

## 出力
```
イベントに参加予定のユーザIDリスト
['user1', 'user2']

全2ユーザー分の参加確率を算出中...
ユーザID: user1, 参加確率: 1.0, 参加回数: 119, イベント申し込み数: 119
ユーザID: user2, 参加確率: 0.8080808080808081, 参加回数: 80, イベント申し込み数: 99

見積もったキャンセル人数: 0.19191919191919204, 現在の参加登録人数: 2, 現在の参加人数の期待値:1.808080808080808
```

## 注意点
- **[重要]処理結果が返ってくるまでにとても時間がかかります。**
    - ユーザのイベント参加ページの取得時1秒のスリープを入れています。そして、1ページあたりのユーザのイベント参加情報は10つまでしか表示されません。したがって`(ユーザ数 * ユーザの過去のイベント参加数)/10`秒時間がかかります。
- イベントの参加予定者の数が100人を超えている場合は不具合が起きますので、処理を中断しています。申し訳ございません。
    - [issse#11](https://github.com/meow-noisy/connpass_estimate_number_of_cancellation/issues/11)に挙げています。

## 解説記事
- connpassの開催前イベントのキャンセル人数を粗く見積もる方法 - meowの覚え書き
    - https://meow-memow.hatenablog.com/entry/2020/11/02/222557
