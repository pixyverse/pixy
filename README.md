Pixy
------

[![Build](https://github.com/versionprime/pixy/actions/workflows/ci.yml/badge.svg)](https://github.com/versionprime/pixy/actions/workflows/ci.yml)

What is Pixy
---------------

pixy is a transpiler that transpiles pixy files into regular python code. Pixy files are JSX inspired component description formats that brings markup style declarative language natively embedded in python. Check out it's [DESIGN](https://github.com/pixyverse/pixy/blob/develop/DESIGN.md).

Example
--------

```python
todo_page = (
    <div class_name="TodoList">
        <todo_list>
            <todo_item status={Status.Completed}>"Remember the milk 🥛"</todo_item>
            <todo_item status={Status.Todo}>"Eggs 🥚"</todo_item>
        </todo_list>
    </div>
    )
```

In order to actually transform that to a UI representation like HTML you need the sister 👩 package, [render_html](https://github.com/pixyverse/render_html). A full example implementing a todo-list can be found in [todo_pixy](https://github.com/pixyverse/todo_pixy)

Development
-------------

1. ```git checkout github.com/pixyverse/pixy.git```
2.  ```cd pixy```
3.  create/install deps in a virtualenv environment and activate it.

    ```shell
    make venv
    source .venv/bin/activate
    ```
4. lint and typecheck
    ```shell
    make lint
    make pie
    ```

5.  Run Tests
    ```shell
    # Run Tests
    make test
    ```
6. Example Pixy file
    ```python
    # a.pix
    comp=<div>"Hello World"</div>
    print(comp)
    ```
    Transpile
    ```shell
    # Transpile a sample pixy file
    python -m pixyverse.pixy -p test.pix -o test.py
    ```

Known Limitations
-------------------
Strings within tags always need to be quoted within single or double quotes.

Development Status
--------------------

Prototype stage. Liable to explode without warning