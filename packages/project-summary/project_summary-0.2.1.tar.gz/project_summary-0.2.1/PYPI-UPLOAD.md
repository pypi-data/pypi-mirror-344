Отлично, давайте все подготовим!

**1. Commit на GitHub**

Сначала убедимся, что Git использует правильного автора для этого коммита.

*   **Проверьте текущие настройки Git для этого репозитория:**
    ```bash
    # Проверить имя пользователя
    git config user.name
    # Проверить email
    git config user.email
    ```
*   **Если они неверны (показывают другой аккаунт):** Установите правильные данные *только для этого репозитория* (флаг `--local` обычно используется по умолчанию, но можно указать явно):
    ```bash
    git config --local user.name "Ваше Правильное Имя GitHub"
    git config --local user.email "ваш_правильный_github_email@example.com"
    ```
    Теперь коммиты в этом репозитории будут использовать эти данные.

*   **Conventional Commit Message:**
    Вот хороший вариант коммита, суммирующий все изменения для версии 0.2.0:

    ```
    feat: add include_no_extension, default config, and help command

    Implements several enhancements for version 0.2.0:

    - Adds `include_no_extension` list to `DirectoryConfig` to allow explicit inclusion of files like Dockerfile, LICENSE, etc.
    - Fixes file inclusion logic (`should_include_file`) so that `files`, `extensions`, and `include_no_extension` criteria work additively.
    - Implements automatic creation of a default `project_summary_config.yaml` with comments if the specified config file is not found.
    - Adds a `project-summary help` command to display usage instructions and link to documentation.
    - Ensures the `-v` flag correctly enables DEBUG level logging and sets default non-verbose level to INFO.
    - Updates README.md and CHANGELOG.md for new features and version bump.
    ```

*   **Процесс коммита:**
    ```bash
    # 1. Убедитесь, что виртуальное окружение активно (хотя для git это не обязательно)
    # source .venv/bin/activate

    # 2. Проверьте статус, чтобы увидеть измененные файлы
    git status

    # 3. Добавьте все измененные/новые файлы в индекс
    # (Внимательно проверьте, что добавляете только нужные файлы!)
    git add src/project_summary/config.py src/project_summary/core.py src/project_summary/cli.py README.md CHANGELOG.md pyproject.toml # или setup.py, если версия там

    # Или добавьте все изменения в отслеживаемых файлах:
    # git add .

    # 4. Сделайте коммит (используя сообщение выше)
    # Способ A: Прямо в команде (убедитесь, что кавычки правильные)
    git commit -m "feat: add include_no_extension, default config, and help command" -m "Implements several enhancements for version 0.2.0:

    - Adds \`include_no_extension\` list to \`DirectoryConfig\` to allow explicit inclusion of files like Dockerfile, LICENSE, etc.
    - Fixes file inclusion logic (\`should_include_file\`) so that \`files\`, \`extensions\`, and \`include_no_extension\` criteria work additively.
    - Implements automatic creation of a default \`project_summary_config.yaml\` with comments if the specified config file is not found.
    - Adds a \`project-summary help\` command to display usage instructions and link to documentation.
    - Ensures the \`-v\` flag correctly enables DEBUG level logging and sets default non-verbose level to INFO.
    - Updates README.md and CHANGELOG.md for new features and version bump."

    # Способ B: Открыть редактор для ввода сообщения (рекомендуется для многострочных)
    # git commit
    # (Вставьте сообщение в открывшийся редактор, сохраните и закройте)

    # 5. Отправьте изменения на GitHub
    # Убедитесь, что вы находитесь в правильной ветке (например, main или develop)
    git push origin <имя_вашей_ветки> # например, git push origin main
    ```

**2. Публикация новой версии на PyPI**

Да, публикацию на PyPI нужно делать явно после того, как вы уверены, что код готов и версия обновлена (в вашем `pyproject.toml` или `setup.py` должна стоять `version = "0.2.0"`).

*   **Предварительные требования:**
    1.  **Аккаунт на PyPI:** У вас должен быть зарегистрированный аккаунт на [pypi.org](https://pypi.org/).
    2.  **Пакеты `build` и `twine`:** Установите их в ваше *активное виртуальное окружение*:
        ```bash
        pip install build twine
        ```
    3.  **API Token (Рекомендуется):** Вместо ввода пароля каждый раз, безопаснее использовать API токен.
        *   Зайдите в свой аккаунт на PyPI.
        *   Перейдите в "Account settings".
        *   Прокрутите вниз до раздела "API tokens".
        *   Нажмите "Add API token".
        *   Дайте токену имя (например, `project-summary-upload`).
        *   Установите "Scope" на "Entire account" (для загрузки) или, если пакет уже существует, вы можете выбрать "Project: project-summary".
        *   Нажмите "Add token".
        *   **Сразу скопируйте сгенерированный токен!** Он больше не будет показан. Сохраните его в безопасном месте (например, менеджер паролей). Токен начинается с `pypi-`.

*   **Процесс публикации:**
    ```bash
    # 1. Убедитесь, что виртуальное окружение активно
    source .venv/bin/activate

    # 2. Очистите старые сборки (если они есть) - это хорошая практика
    rm -rf dist/ build/ *.egg-info

    # 3. Соберите пакет (исходный код и wheel)
    # Эта команда использует информацию из pyproject.toml (или setup.py)
    python -m build

    # После выполнения в директории проекта появятся папки `dist` и `build`.
    # В `dist` будут два файла: .whl (wheel) и .tar.gz (source archive).

    # 4. Проверьте собранные пакеты (опционально, но рекомендуется)
    twine check dist/*
    # Должно вывести "Checking distribution dist/..." и не показать ошибок.

    # 5. Загрузите пакеты на PyPI
    twine upload dist/*

    # 6. Ввод данных для аутентификации:
    #    - Когда спросит "Enter your username:", введите `__token__` (именно так, с двумя подчеркиваниями).
    #    - Когда спросит "Enter your password:", вставьте ваш скопированный API токен (он не будет отображаться при вводе).

    # Если вы НЕ используете токен (не рекомендуется):
    #    - Введите ваш логин PyPI.
    #    - Введите ваш пароль PyPI.

    # 7. Дождитесь завершения загрузки. Twine покажет URL вашего пакета на PyPI.
    ```

*   **Проверка:**
    *   Перейдите на страницу вашего пакета на PyPI (`https://pypi.org/project/project-summary/`).
    *   Убедитесь, что последняя версия теперь 0.2.0.
    *   Проверьте, что описание (из README) и другая информация отображаются корректно.
    *   Попробуйте установить новую версию в чистом окружении: `pip install project-summary==0.2.0`.

Готово! Вы успешно закоммитили изменения и опубликовали новую версию вашего пакета.