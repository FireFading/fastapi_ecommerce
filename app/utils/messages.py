from dataclasses import dataclass


@dataclass
class Messages:
    USER_NOT_FOUND = "Пользователь с таким Email не существует"
    USER_ALREADY_EXISTS = "Пользователь с таким Email уже существует"
    USER_LOGOUT = "Вы вышли из аккаунта"

    INVALID_TOKEN = "Токен недействителен"

    CONFIRM_REGISTRATION_MAIL_SENT = "На почту отправлено письмо для подтверждения регистрации"
    RESET_PASSWORD_MAIL_SENT = "Письмо с токеном для сброса пароля отправлено"

    PHONE_UPDATED = "Телефон успешно обновлен"
    NAME_UPDATED = "Имя успешно обновлено"

    PROFILE_DELETED = "Профиль успешно удален"
    PROFILE_ACTIVATED = "Ваш аккаунт успешно активирован"

    WRONG_PASSWORD = "Неверный пароль"
    PASSWORDS_NOT_MATCH = "Пароли не совпадают"
    PASSWORD_RESET = "Пароль успешно сброшен"
    NEW_PASSWORD_SIMILAR_OLD = "Новый пароль похож на старый"
    PASSWORD_UPDATED = "Пароль успешно обновлен"

    PRODUCT_CREATED = "Товар успешно создан"
    PRODUCT_DELETED = "Продукт успешно удален"
    PRODUCT_ALREADY_EXISTS = "Данный продукт уже существует"


messages = Messages()