# 作って学ぶ sql injection

このリポジトリは Django の検証用プロジェクトです。  
以下の手順でローカル環境を構築できます。

## 前提

- macOS / Linux（Windows の場合は venv の有効化コマンドのみ読み替え）
- Python 3.13 系
- ターミナル（zsh / bash）

## 環境構築手順

2. 仮想環境を作成

```bash
python3 -m venv .venv
```

3. 仮想環境を有効化

```bash
source .venv/bin/activate
```

4. 依存パッケージをインストール

```bash
pip install -r requirements.txt
```

5. マイグレーションを適用

```bash
python manage.py migrate
```

6. 開発サーバーを起動

```bash
python manage.py runserver
```

ブラウザで以下へアクセス:

- http://127.0.0.1:8000/

## 初回セットアップを 1 コマンドで実行（任意）

```bash
python3 -m venv .venv \
&& source .venv/bin/activate \
&& pip install -r requirements.txt \
&& python manage.py migrate \
&& python manage.py runserver
```

## よく使うコマンド

### システムチェック

```bash
python manage.py check
```

### 管理ユーザー作成

```bash
python manage.py createsuperuser
```

### 管理画面

- http://127.0.0.1:8000/admin/

## 補足

- ローカル DB は SQLite（`db.sqlite3`）です。
- 仮想環境（`.venv`）やローカル DB は `.gitignore` で除外済みです。
