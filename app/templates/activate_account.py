from app.settings import settings


def html_activate_account_mail(token: str):
    return f"""
    <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Активация аккаунта</title>
        </head>
        <body>
            <h3>Ваш аккаунт на {settings.domain_name} создан!</h3>
            <p>Для завершения регистрации перейдите по
                <a href="{settings.domain_name}/reset-password/{token}"> ссылке</a>
            </p>
        </body>
        </html>
    """
