pre-commit-config-shellcheck
============================

.. contents::

Передісторія
------------

Повторна перевірка написаного коду може бути складним, ненадійним і замороченим завданням для програміста.
Нещодавно, під час рефакторингу коду ми помітили декілька помилок у shell коді всередині файла налаштувань пре-коміту, які існували там впродовж довгого часу, не видаючи помилок.
Саме тому необхідність перевіряти код вручну хотілося б мінімізувати, або автоматизувати.
Для цього було створено утіліту `pre-commit-config-shellcheck <https://github.com/Anadea/pre-commit-config-shellcheck>`__.

Яку проблему вирішує
--------------------

Ми створили інструмент, що дозволяє зменшити кількість помилок і неточностей у проектах шляхом автоматичної перевірки файла налаштувань пре-коміту.
Дана перевірка проводиться за допомогою іншого інструмента - Shellcheck.

Shellcheck
----------

`Shellcheck <https://github.com/koalaman/shellcheck>`__ - shell скріпт інструмент для статичного аналізу (A shell script static analysis tool).
Він вміє як виявляти синтаксичні проблеми, що можуть виникати у новачків, так і складніші семантичні проблеми, що можуть викликати неочікуване поводження команд.

Перевірка файла
---------------

Для використання Shellcheck йому передається файл зі збереженим shell кодом.
Оскільки файл .pre-commit-config.yaml містить в собі не лише перелік команд, записаних shell кодом, то робота даної утіліти буде неправильною.
Через це наш інструмент проводить попередню підготовку вхідних точок до перевірки:
підготовка полягає у створенні малих тимчасових файлів для точок входу, кожен з яких окремо перевіряється інструментом Shellcheck.

.. code-block:: python

    for entry in self._list_entries():
        with tempfile.NamedTemporaryFile("w+") as tmp:
            tmp.write("#!/bin/sh\n")
            tmp.write(str(entry["entry"]["entry"]))
            tmp.flush()

Робота з процесами
------------------

Згаданий вище інструмент ``Shellcheck`` - консольна утіліта, що не має бібліотек-адаптерів для різних мов програмування,
тому для кожного створеного файлу створюється підпроцес з виконанням перевірки:

.. code-block:: python

    process = subprocess.Popen(
        args=[self.options.shellcheck, tmp.name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

Результати виконання підпроцесів збираються і на їх основі будується вивід, який буде містити перелік знайдених неточностей разом із їхнім місцем знаходження у файлі.

`Приклад використання і виводу <https://asciinema.org/a/514275>`_ (має бути embedded елемент)


Зручність використання
----------------------

Задля збереження простоти і зручності використання цієї утіліти створено декілька шляхів використання:

- Як утіліта командного рядку

.. code-block:: bash

    $ pip install pre-commit-config-shellcheck
    $ pre_commit_config_shellcheck.py .pre-commit-config.yaml

- Як pre-commit hook

.. TODO: Вставити, що це

.. code-block:: yaml

    # .pre-commit-config.yaml
    - repo: "https://github.com/Anadea/pre-commit-config-shellcheck"
      rev: "0.3.3"
        hooks:
          - id: "pre-commit-config-shellcheck"

- Та як github action

.. code-block::

    - name: "pre-commit-config-shellcheck"
      uses: "Anadea/pre-commit-config-shellcheck@0.3.3"
      id: "pre-commit-config-shellcheck"
      with:
        config: ".pre-commit-config.yaml"


