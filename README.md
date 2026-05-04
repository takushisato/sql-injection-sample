# 作って学ぶ sql injection

SQL インジェクションの脆弱性を学ぶためのリポジトリです。  
以下の手順でローカル環境を構築できます。

## 前提

- macOS / Linux（Windows の場合は venv の有効化コマンドのみ読み替え）
- Python 3.13 系
- ターミナル（zsh / bash）

## 環境構築手順

1. Docker Desktop を起動（または Docker Engine を起動）

2. プロジェクトディレクトリへ移動

```bash
cd /任意のパス
```

3. コンテナをビルドして起動

```bash
docker compose up -d --build
```

4. コンテナ内に入る

```bash
docker compose exec web /bin/sh
```

5. マイグレーションを実行

```bash
python manage.py migrate
```

6. 管理ユーザーを作成

```bash
python manage.py createsuperuser

# 上記コマンドを入力後、プロンプトに従ってユーザー名、メールアドレス、パスワードを入力
```

7. ブラウザでアクセス

- ホーム: http://127.0.0.1:8000/accounts/
- ログイン: http://127.0.0.1:8000/accounts/login/
- BADログイン: http://127.0.0.1:8000/accounts/bad-login/
- ログアウト: http://127.0.0.1:8000/accounts/logout/

**補足**

ログイン・・・問題ないログイン画面のサンプル
BADログイン・・・SQLインジェクションの脆弱性があるログイン画面のサンプル。画面上の説明を読んで、SQLインジェクション攻撃を試してみてください。

## User 管理モデルとログイン

- `accounts.User`（`AbstractUser` 継承）を利用しています。
- 追加項目: `display_name`, `created_at`, `updated_at`
- Django 標準認証を使ってログイン/ログアウトできます。

管理ユーザー作成後、以下でログイン確認できます。

- ログイン: http://127.0.0.1:8000/accounts/login/
- ログイン後ホーム: http://127.0.0.1:8000/

停止するとき:

```bash
docker compose down
```
## 感想

私自身は理論ではSQLインジェクション学んだことはありますが、実際に攻撃を試すことで理解が深まると思いこのリポジトリを作成しました。
構造としては画面からUserが入力した値をそのままSQLクエリに埋め込んでいる形になっていて、よくあるアンチパターンを再現しています。
こうしたアンチパターンを学ぶことで、セキュアなコードを書くための意識が高まると思いました。

