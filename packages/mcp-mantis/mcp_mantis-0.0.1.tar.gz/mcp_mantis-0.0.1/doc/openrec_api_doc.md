# OPENREC.tv API ドキュメント

## 目次
- [概要](#概要)
- [認証](#認証)
- [配信関連](#配信関連)
- [コメント関連](#コメント関連)
- [チャンネル関連](#チャンネル関連)
- [動画関連](#動画関連)
- [キャプチャ関連](#キャプチャ関連)
- [エール関連](#エール関連)
- [ユーザアカウント関連](#ユーザアカウント関連)
- [その他](#その他)
- [検索](#検索)

## 概要

OPENREC.tvが提供する公式APIです。配信情報の取得、コメントの取得・投稿、チャンネル情報の取得など、様々な機能を利用できます。

## 認証

一部のAPIは認証が必要です。認証が必要なAPIを利用する場合は、以下の手順で認証を行います。

### セッションの取得

```
メソッド: POST
エンドポイント: https://www.openrec.tv/api-tv/session
概要: 様々な機能で用いるcookie(uuid, token, random)を取得する
認証: 必要
```

### ログイン

```
メソッド: POST
エンドポイント: https://www.openrec.tv/viewapp/v4/mobile/user/login
概要: メールアドレスとパスワードを用いてログインする。このとき、cookieにuuid, token, randomを与える必要がある。また、レスポンスではaccess_tokenやuuid, token, randomがcookieにセットされる
認証: 必要
パラメータ:
  - mail (string): ログインするアカウントのメールアドレスを指定する
  - password (string): ログインするアカウントのパスワードを指定する
```

## 配信関連

### 配信一覧を取得

```
メソッド: GET
エンドポイント: https://public.openrec.tv/external/api/v5/movies
概要: 配信・動画一覧を取得する
認証: 不要
パラメータ:
  - is_live (bool): 取得するものを生配信に限定するか？
  - is_upload (bool): 取得するものを動画に限定するか？
  - onair_status (number): 0は予約枠、1は配信中、2はVOD
  - channel_ids (string): channel_idsを指定することで、特定のチャンネルのみに絞り込むことができる
  - page (number): ページ数を指定できる。デフォルトは1
  - sort (string): 取得するデータを並び変える。並び変えられる順番は次の通り。total_views | created_at | -created_at | schedule_at | onair_status | live_views | total_yells | -total_yells | popularity | published_at | -published_at
```

### 枠情報を取得

```
メソッド: GET
エンドポイント: https://public.openrec.tv/external/api/v5/movies/{M_ID}
概要: M_IDで指定した任意の動画の情報を取得する。このM_IDは配信のURLのもの。例えば"https://www.openrec.tv/live/n9ze3m2w184"のM_IDは"n9ze3m2w184"である
認証: 不要
```

### 動画ファイルのURLを含めた枠情報を取得

```
メソッド: GET
エンドポイント: https://public.openrec.tv/external/api/v5/movies/{M_ID}/detail
概要: M_IDで指定した任意の動画の情報を取得する。認証情報を渡すため、動画ファイルのURLを得ることができる
認証: 必要
```

### 通報

```
メソッド: POST
エンドポイント: https://apiv5.openrec.tv/api/v5/movies/{M_ID}/reports
概要: M_IDで指定した任意の動画を通報できる
認証: 必要
パラメータ:
  - reason_type (number): 配信や動画の不適切な点のジャンルを指定する。1はわいせつな表現、2は他者を誹謗中傷する表現、3は著作権の侵害、4はプライバシーの侵害、5は過激な暴力や自傷行為、6はなりすまし行為、7は出会いを誘導する行為、8はねずみ講やマルチ商法、9は誤解を招く配信設定、10はゲームの規制対象地域の配信、11は改造版・海賊版ソフトの配信、12は政治的・宗教的・人種的な内容、13はその他の問題
  - movie_id (string): URLで指定したM_IDと同じもの
  - message (string): 通報内容
```

## コメント関連

### コメントの取得

```
メソッド: GET
エンドポイント: https://public.openrec.tv/external/api/v5/movies/{M_ID}/chats
概要: M_IDで指定した任意の配信のコメントを取得する
認証: 不要
パラメータ:
  - from_created_at (ISO8601 DATETIME): ISO8601形式で指定した日時以降のコメントを取得する。例: 2023-03-20T12:48:47.265Z
  - to_created_at (ISO8601 DATETIME): ISO8601形式で指定した日時までのコメントを取得する。from_created_atと同時に使用できない
  - is_including_system_message (bool): システムメッセージを含めるか？
  - limit (bool): 取得するコメントの数。1-300
```

### コメントの投稿

```
メソッド: POST
エンドポイント: https://apiv5.openrec.tv/api/v5/movies/{M_ID}/chats
概要: M_IDで指定した任意の配信に対しコメントを投稿する
認証: 必要
パラメータ:
  - message (string): 送信するメッセージ内容。100字まで
  - quality_type (number): 0が低遅延、1が高画質を指す
  - league_key (?): 何に使用するか不明だが一応空文字列を送信する
  - to_user_id (?): 何に使用するか不明だが一応空文字列を送信する
  - consented_chat_terms (bool): 基本的にはfalseでよさそう
```

### チャットサーバに接続

```
メソッド: WebSocketでconnect
エンドポイント: wss://chat.openrec.tv/socket.io/
概要: 任意の配信のチャットやエールをリアルタイムで取得する。25秒ごとにping("2")を送る必要がある。※受信するメッセージはバックスラッシュでエスケープされたままだが`JSON.parse()`でうまく消せる。受信メッセージタイプ 0: コメント, 1: 同接, 3: 配信開始, 5: 配信終了, 6: ban追加, 7: ban解放, 8: モデ追加, 9: モデ解除, 11: タイトル変更などの情報, 12: テロップ追加, 13: テロップ削除, 29: アンケ開始, 30: アンケ途中結果, 31: アンケ結果, 43: ブンレク拡張機能
認証: 不要
パラメータ:
  - movieId (string): MOVIE_IDは"https://public.openrec.tv/external/api/v5/movies/{M_ID}"から取得できる
  - EIO (number): 3
  - transport (string): "websocket"
```

### 配信のアーカイブに付けられたコメントの取得

```
メソッド: GET
エンドポイント: https://public.openrec.tv/external/api/v5/movies/{M_ID}/comments
概要: M_IDで指定した任意の配信のアーカイブのコメントを取得する
認証: 不要
```

### 配信のアーカイブにコメントを投稿

```
メソッド: POST
エンドポイント: https://apiv5.openrec.tv/api/v5/movies/{M_ID}/comments
概要: M_IDで指定した任意の配信のアーカイブにコメントを投稿する
認証: 必要
パラメータ:
  - message (string): 送信するメッセージの内容。100字まで
  - league_key (?): 何に使用するか不明だが一応空文字列を送信する
```

### 配信のアーカイブのコメントに対し返信

```
メソッド: POST
エンドポイント: https://apiv5.openrec.tv/api/v5/movies/{M_ID}/comments/{COMMENT_ID}/replies
概要: M_IDで指定した任意の配信のアーカイブについたコメントに対し返信を投稿する。COMMENT_IDは"https://public.openrec.tv/external/api/v5/movies/{M_ID}/comments"から取得できる
認証: 必要
パラメータ:
  - message (string): 送信するメッセージの内容。100字まで
  - consented_comment_terms (bool): trueにしておく
```

## チャンネル関連

### チャンネルランキング

```
メソッド: GET
エンドポイント: https://public.openrec.tv/external/api/v5/channel-ranks
概要: 月間や週間のチャンネルランキングを取得する
認証: 不要
パラメータ:
  - period (string): ランキングの期間を指定する。hourly | daily | weekly | monthly
  - date (number): 月間ランキングの年月をYYYYMMの形式で指定する。指定しなかった場合、現在の月になる
  - tag (string): 不明
  - page (number): ページ数を指定する。デフォルトは1
```

### 人気チャンネル

```
メソッド: GET
エンドポイント: https://public.openrec.tv/external/api/v5/popular-channels
概要: 不明
認証: 不要
パラメータ:
  - page (number): ページ数を指定する。デフォルトは1
```

### チャンネル情報

```
メソッド: GET
エンドポイント: https://public.openrec.tv/external/api/v5/channels/{USER_ID}
概要: USER_IDで指定したユーザのチャンネルの情報を取得する
認証: 不要
```

### 毎日配信チャンネル

```
メソッド: GET
エンドポイント: https://public.openrec.tv/external/api/v5/stats/daily-channels
概要: 毎日配信しているチャンネルの一覧を取得する
認証: 不要
パラメータ:
  - group (string): よくわからん。continuous_live_user_top?
```

## 動画関連

### 動画一覧

```
メソッド: GET
エンドポイント: https://public.openrec.tv/external/api/v5/search-movies
概要: 任意のユーザの動画・VODの一覧を取得する
認証: 不要
パラメータ:
  - sort (string): 並び順を指定できる。登録が新しい順: "published_at", 登録が古い順: "-published_at", 視聴数順: "total_views"
  - include_deleted (bool): 削除されたものを含めるか？(機能してる？)
  - channel_ids (string): 検索対象の配信者のID。指定しなかった場合は、OPENREC全体から結果が得られる
  - from_published_at (string): ISO8601形式で指定した日時以降の動画一覧を取得する。例: 2020-03-20T12:48:47.265Z。指定しなかった場合は、2015年1月1日以降として扱われる
  - to_published_at (string): ISO8601形式で指定した日時までの動画一覧を取得する。指定しなかった場合は、現在の日付までとして扱われる
  - game_ids (string): ゲームIDを指定して検索をフィルタする
  - onair_status (number): 0が予約枠、1は配信中のもの、2がVODを指す
  - page (number): ページ数を指定する。デフォルトは1
  - include_live (bool): 配信を含めるか？
  - include_upload (bool): 投稿した動画を含めるか？
```

### 人気動画一覧

```
メソッド: GET
エンドポイント: https://public.openrec.tv/external/api/v5/popular-movies
概要: 動画一覧を取得
認証: 不要
パラメータ:
  - popular_type (string): 取得するタイプを指定できる。archive | upload | upload_archive
  - page (number): ページ数を指定する。デフォルトは1
```

## キャプチャ関連

### 人気のキャプチャの一覧を取得

```
メソッド: GET
エンドポイント: https://public.openrec.tv/external/api/v5/capture-ranks
概要: 人気のキャプチャの一覧を取得する
認証: 不要
パラメータ:
  - period (string): ランキングの期間を指定する。daily | weekly | monthly
  - date (number): 月間ランキングの年月をYYYYMMの形式で指定する。このパラメータを指定した場合、periodでdailyを指定したとしても月間ランキングとなる
  - is_channel_unique (bool): 各チャンネルにつきキャプチャを1つに制限するか？
  - page (number): ページ数を指定する。デフォルトは1
```

### キャプチャ一覧

```
メソッド: GET
エンドポイント: https://public.openrec.tv/external/api/v5/captures
概要: 特定のチャンネルや配信のキャプチャを取得する
認証: 不要
パラメータ:
  - channel_id (string): キャプチャの元の配信者のIDを指定することで、取得するキャプチャをその配信者だけに限定する
  - movie_id (string): キャプチャ元の配信を指定できる。{M_ID}
  - sort (string): 取得するデータを並び変える。並び変えられる順番は次の通り。views | public_at
  - sort_direction (string): 昇順か降順か指定する。ASC | DESC
  - page (number): ページ数を指定できる。デフォルトは1
```

### キャプチャの情報を取得

```
メソッド: GET
エンドポイント: https://public.openrec.tv/external/api/v5/captures/{CAPTURE_ID}
概要: CAPTURE_IDで指定した任意の動画の情報を取得する。このCAPTURE_IDはキャプチャページのURLのもの。例えば"https://www.openrec.tv/capture/w6dl8gJjq92"のCAPTURE_IDは"w6dl8gJjq92"である
認証: 不要
```

### キャプチャリアクションを送信

```
メソッド: POST
エンドポイント: https://apiv5.openrec.tv/everyone/api/v5/reactions
概要: 任意のキャプチャに対しリアクションをつける。ログインユーザであれば1つのキャプチャに5つまでリアクションをつけることができる。非ログインユーザでも1つだけリアクションをつけることができる
認証: 必要
パラメータ:
  - target_id (string): capture_id
  - target_type (string): "capture"
  - reaction_id (string): 送信するリアクションをここで指定する。指定できるリアクションは次の通り。arara | bikkuri | gg | hatena | kakke | kami | kansya | kawaii | kusa | music | nice | odoroki | sugo | tsuyo | umai | wakuwaku | wara | yaba
```

## エール関連

### 金額順エール

```
メソッド: GET
エンドポイント: https://public.openrec.tv/external/api/v5/yell-ranks
概要: 任意の配信や宛先配信者へのエールを金額の多い順のリストを取得する
認証: 不要
パラメータ:
  - movie_id (string): M_IDで指定した任意の配信のエールを取得する。M_IDは配信のURLのもの
  - user_id (string): エールの宛先を限定できる
  - month (number): 年月をYYYYMMの形式で指定する
  - page (number): ページ数を指定する。デフォルトは1
```

### 時系列順エール

```
メソッド: GET
エンドポイント: https://public.openrec.tv/external/api/v5/yell-logs
概要: 任意の配信へのエールを時系列順に取得する
認証: 不要
パラメータ:
  - movie_id (string): M_IDで指定した任意の配信のエールを取得する。M_IDは配信のURLのもの
  - page (number): ページ数を指定する。デフォルトは1
```

## ユーザアカウント関連

### ユーザ情報

```
メソッド: GET
エンドポイント: https://apiv5.openrec.tv/api/v5/users/me?include_hidden_channels=true
概要: ログイン中のユーザに関する情報を取得する
認証: 必要
パラメータ:
  - include_hidden_channels (bool): 不明
```

### タイムライン

```
メソッド: GET
エンドポイント: https://apiv5.openrec.tv/api/v5/users/me/timelines/movies
概要: 登録しているチャンネルの配信・VODの一覧を取得する
認証: 必要
パラメータ:
  - onair_status (number): 1が配信中のもの、2がVODを指す
  - limit (number): 取得数の上限を指定する
  - include_upload (bool): 不明
```

### 登録チャンネル予約枠

```
メソッド: GET
エンドポイント: https://apiv5.openrec.tv/api/v5/users/me/timeline-movies/comingups
概要: 登録チャンネルの予約枠の一覧を取得する
認証: 必要
パラメータ:
  - limit (number): 取得数の上限を指定する
  - offset (number): オフセット(トップからのずれ)を指定する
```

### 通知カウント

```
メソッド: GET
エンドポイント: https://apiv5.openrec.tv/api/v5/users/me/notifications/count
概要: ログイン中のユーザの通知数を取得する
認証: 必要
```

### 通知リスト

```
メソッド: GET
エンドポイント: https://apiv5.openrec.tv/api/v5/users/me/notifications
概要: ログイン中のユーザの通知の内容を取得する
認証: 必要
パラメータ:
  - offset (number): 取得する通知のオフセットを指定する
  - limit (number): 取得数の上限を指定する
  - notification_type (string): 通知のタイプを指定する。normal | important
```

### チャット設定を更新

```
メソッド: PUT
エンドポイント: https://apiv5.openrec.tv/api/v5/users/me/chat-setting
概要: ログイン中のユーザのチャット設定を変更する
認証: 必要
パラメータ:
  - name_color (string): チャットの名前の色を変更する。16進のカラーコードで指定する。(プレ垢限定機能)
  - is_fixed_phrase_hidden (bool): 定型文を表示するか？
  - muted_warned_user (bool): 警告ユーザを非表示にするか？
  - muted_fresh_user (bool): 新参ユーザを非表示にするか？
  - muted_banned_word (bool): NGワードに登録した単語を含むコメントを非表示にするか？
  - muted_unauthenticated_user (bool): 未ログインユーザを非表示にするか？
  - adjust_chat_delay (bool): 超低遅延ユーザのコメントの表示を遅延させるか？
  - is_small_size_stamp (bool): スタンプの表示を小さくするか？
  - is_subs_badge_hidden (bool): 自身のサブスクバッジを非表示にするか？
  - is_premium_hidden (bool): 自身がプレ垢であることを非表示にするか？
```

## その他

### スポットライト

```
メソッド: GET
エンドポイント: https://public.openrec.tv/external/api/v5/spotlights
概要: フンレクトップに載っているバナーの情報を取得する
認証: 不要
パラメータ:
  - device_type (string): デバイスタイプを指定する。web | android | ios
```

### お知らせ

```
メソッド: GET
エンドポイント: https://public.openrec.tv/external/api/v5/informations
概要: フンレクからのお知らせを取得する。メンテの情報など
認証: 不要
パラメータ:
  - device_type (string): デバイスタイプを指定する。web | android | ios
  - user_type (number): 不明
  - group_key (string): information_top?
```

### 配信人気タグ

```
メソッド: GET
エンドポイント: https://public.openrec.tv/external/api/v5/feature-tags
概要: 配信中の枠の人気タグを取得する
認証: 不要
```

### フェス一覧

```
メソッド: GET
エンドポイント: https://public.openrec.tv/external/api/v5/fes-events
概要: フェス一覧
認証: 不要
パラメータ:
  - status (string): opened | closed | scheduled
  - page (number): ページ数を指定する。デフォルトは1
```

### フェス情報

```
メソッド: GET
エンドポイント: https://public.openrec.tv/external/api/v5/fes-events/{FES_ID}
概要: FES_IDで指定したイベントの詳細情報を取得する
認証: 不要
パラメータ:
  - secret_key (string): よくわからん。undefinedでいい？
  - include_content (bool): よくわからん
```

### 人気ゲーム一覧

```
メソッド: GET
エンドポイント: https://public.openrec.tv/external/api/v5/popular-games
概要: 現在、配信されているゲームを同接が高い順に取得する
認証: 不要
パラメータ:
  - page (number): ページ数を指定する。デフォルトは1
```

## 検索

### ユーザの検索

```
メソッド: GET
エンドポイント: https://public.openrec.tv/external/api/v5/search-users
概要: OPENRECのユーザを検索する
認証: 不要
パラメータ:
  - search_query (string): 検索文字列
  - channel_only (bool): 配信者権限があるユーザのみに限定するか？
```

### ゲームの検索

```
メソッド: GET
エンドポイント: https://public.openrec.tv/external/api/v5/search-games
概要: ゲームの検索
認証: 不要
パラメータ:
  - search_query (string): 検索文字列
```

### 配信・動画の検索

```
メソッド: GET
エンドポイント: https://public.openrec.tv/external/api/v5/search-movies
概要: 配信・動画の検索
認証: 不要
パラメータ:
  - search_query (string): 検索文字列