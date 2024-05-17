Pixie
------

[![Build](https://github.com/versionprime/pixie/actions/workflows/ci.yml/badge.svg)](https://github.com/versionprime/pixie/actions/workflows/ci.yml)

What is Pixie
---------------

pixie is a transpiler that transpiles pixie files into regular python code. Pixie files are JSX inspired component description formats that brings markup style declarative language natively embedded in python.

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


Known Limitations
-------------------
Strings within tags always need to be quoted within single or double quotes.

Development Status
--------------------

Prototype stage. Liable to explode without warning