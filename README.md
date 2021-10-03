# YT-Livechat-checker

## 目的
このツールは、現在Youtubeで発生している  
**ライブチャットにコメントを投稿しても反映されない**問題を  
検証しGoogle社に対して提出するAPIサーバからの戻り値情報を取得する為のものです。

## 事前準備
* [Google Cloud Platform](https://console.cloud.google.com/)から
  * ``Youtube DATA API v3``のパーミッションを取得
  * ``OAuth 2.0 Client ID``を取得（デスクトップで問題ありません）

* Python
`` pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib ``

## 実行方法
`` ./livechat_insert_pub.py (Youtube配信識別子) (投稿する文字列) ``

