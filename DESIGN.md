# Pixy Design


## Motivation

Declarative and component-oriented UI frameworks got a massive boost with [react](https://react.dev), and the developer experience got an uplift with the introduction of JSX. JSX allowed intermixing declarative HTML alongside programmable Javascript.

Python frameworks are just catching up, with the templating legend Jinja2 still reigning supreme. However, its approach to treating everything as strings must be revised in the component age.

Pixy aims to intermix HTML with regular Python code.

## Approach

Pixy with file extension (.pix) will hold this mixed code.

All regular Python code is valid Pixy code. Pixy adds support for <component/> tags interspersed in Python code. The tags, like any other Python expression, are evaluated at runtime. The best way to support the entire Python syntax in Pixy code is to rely on the underlying Python grammar, and fortunately, the Python team has cleanly exposed the same for various reasons here. We have maximum conformance if we can extend this grammar with component support. And that is the achievement of this project. We can now support <tags/> in Python code with minimal extension to the core Python grammar.

To mean something, these <tags/> have to be transformed into something meaningful as Python primitives (strings, ints, etc.) That is achieved by the grammar action generating calls to a function ```create_element``` with all the context.

A standalone library can now interpret create_element as needed, like rendering it as an HTML string.

## Features

Extending the Python grammar to support tags enables interesting features **without any additional implementation. Less code is better!**

You can define and pass around tagged components.

```
def wrap_component(comp):
    ....
my_comp = <div>"Hello World"</div>
wrap_component(my_comp)
```

You can set computed values on component attributes.

```
<grid_layout rows={level + 5}> columns ={level + exp}>
...
</grid_layout>
```

You can embed Python expressions within tags.

```
<Hello>
{1+2}
{True}
</Hello>
```