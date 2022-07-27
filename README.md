# Flask API Based on JWT authentication.
Сервис делает возможным аутентификацию пользователей с выдачей JWT и последующей авторизацией посредством JWT без необходимости обращения к БД при каждом запросе пользователя.

Через API можно управлять ролями, присваивать их пользователям. Это доступно только администраторам сервиса. Через основной авторизационный эндпоинт можно получить информацию в виде ID пользователя и его ролей. Обращений к БД, хранящей информацию о пользователях, при этом не происходит, если токен не отозван вследствии изменений в аккаунте пользователя или его ролей, а так же если токен не просрочен. Администратор может просмотреть информацию о пользователе.

Вся информация об API (OpenAPI) эндпоинтах размещена по адресу /api/v1/

Администратора можно создать только через коммандную строку приложения: flask create-superuser, далее следуйте указаниям на экране

Для первого запуска, после настройки параметров окружения (например через .env файл), необходимо инициализировать БД командой flask db upgrade

