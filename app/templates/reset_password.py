from app.config import settings


def html_reset_password_mail(reset_password_token: str):
    return f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Восстановление пароля</title>
        </head>
        <body>
            <h3>С вашего аккаунта пришел запрос на сброс пароля</h3>
            <p>Для продолжения перейдите по
                <a href="{settings.domain_name}/reset-password/{reset_password_token}"> ссылке</a>
            </p>
            <p>Если это были не Вы, смените пароль</p>
        </body>
        </html>
        """
