from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from .models import User


@login_required
def home(request):
    return render(request, "accounts/home.html")


# =============================================================================
# 警告: 学習用の意図的に脆弱なログイン実装。本番では絶対に使用しないこと。
#  - CSRF保護を無効化 (@csrf_exempt)
#  - 生SQLを文字列連結で構築 → SQL インジェクション可能
#  - パスワードを平文比較 (本来は make_password / check_password を使う)
# 例: username に  ' OR 1=1 --  を入れるとログインできてしまう。
# =============================================================================
@csrf_exempt
def bad_login(request):
    error = None
    executed_sql = None

    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        # 危険: 文字列連結で SQL を組み立てている
        executed_sql = (
            "SELECT id FROM accounts_user "
            f"WHERE username = '{username}' AND password = '{password}' "
            "LIMIT 1"
        )

        with connection.cursor() as cursor:
            try:
                cursor.execute(executed_sql)
                row = cursor.fetchone()
            except Exception as exc:  # 学習用にDBエラーを画面表示
                row = None
                error = f"SQL Error: {exc}"

        if row:
            user = User.objects.filter(pk=row[0]).first()
            if user is not None:
                # authenticate() を経由していないので backend を明示する必要がある
                login(
                    request,
                    user,
                    backend="django.contrib.auth.backends.ModelBackend",
                )
                return redirect("home")
            error = "ユーザーが見つかりません"
        elif error is None:
            error = "ログイン失敗"

    return render(
        request,
        "registration/bad_login.html",
        {"error": error, "executed_sql": executed_sql},
    )
