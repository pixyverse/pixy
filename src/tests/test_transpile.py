import unittest
import sys
from pixieverse.pixie.transpile import transpile_source


class TestTranspileSource(unittest.TestCase):
    def test_transpileEmpty(self) -> None:
        input = ""
        expected = ""
        transpiled = transpile_source(input)
        self.assertEqual(expected, transpiled)

    def test_transpilePlainPy(self) -> None:
        input = """a = 1
print(a)
"""
        expected = input.rstrip()
        transpiled = transpile_source(input)
        self.assertEqual(expected, transpiled)

    def test_transpileInvalidPy(self) -> None:
        input = """
a =
print(a)"""
        self.assertRaises(SyntaxError, transpile_source, input)

    def test_transpileSelfClosingComponent(self) -> None:
        input = """
from runtime import createElement
a = <Hello/>
print(a)
"""
        expected = """from runtime import createElement
a = createElement('Hello', {})
print(a)"""
        transpiled = transpile_source(input)
        self.assertEqual(expected, transpiled)

    def test_transpileSelfWithAttributes(self) -> None:
        input = """
from runtime import createElement
a = <Hello who={'Bertie Wooster'} salutation={'Sir'}/>
print(a)
"""
        expected = """from runtime import createElement
a = createElement('Hello', {'who': 'Bertie Wooster', 'salutation': 'Sir'})
print(a)"""
        transpiled = transpile_source(input)
        self.assertEqual(expected, transpiled)

    def test_transpileSelfWithAttributesDuplicateOverride(self) -> None:
        """
        Since attributes are now passed as a dictionary the last attribute definition
        will win just as normal as a python dict.
        """
        input = """
from runtime import createElement
a = <Hello who={'Bertie Wooster'} salutation={'Mr'} salutation={'Sir'}/>
print(a)
"""
        expected = """from runtime import createElement
a = createElement('Hello', {'who': 'Bertie Wooster', 'salutation': 'Mr', 'salutation': 'Sir'})
print(a)"""
        transpiled = transpile_source(input)
        self.assertEqual(expected, transpiled)

    def test_transpileNestedBlockElements(self) -> None:
        input = """
from runtime import createElement
a = <Terminal><StatusBar></StatusBar></Terminal>
print(a)
"""
        expected = """from runtime import createElement
a = createElement('Terminal', {}, [createElement('StatusBar', {}, [])])
print(a)"""
        transpiled = transpile_source(input)
        self.assertEqual(expected, transpiled)

    def test_transpileNestedBlockElementsWithAttributes(self) -> None:
        input = """
from runtime import createElement
a = <Terminal width={100}><StatusBar status={'IDLE'}></StatusBar></Terminal>
print(a)
"""
        expected = """from runtime import createElement
a = createElement('Terminal', {'width': 100}, [createElement('StatusBar', {'status': 'IDLE'}, [])])
print(a)"""
        transpiled = transpile_source(input)
        self.assertEqual(expected, transpiled)

    def test_transpileNestedBlockElementsWithExpressions(self) -> None:
        input = """
from runtime import createElement
a = <Terminal>{200+300}{'TEST'}</Terminal>
print(a)
"""
        expected = """from runtime import createElement
a = createElement('Terminal', {}, [200 + 300, 'TEST'])
print(a)"""
        transpiled = transpile_source(input)
        self.assertEqual(expected, transpiled)

    def test_transpileGenExpressionsInBlockElements(self) -> None:
        input = """
from runtime import createElement
names = ['Alice','Bob','Charlie']
c=<Hello>
<ul>
{map(lambda name: <li>{name}</li>, names)}
</ul>
</Hello>
"""
        expected = """from runtime import createElement
names = ['Alice', 'Bob', 'Charlie']
c = createElement('Hello', {}, [createElement('ul', {}, [map(lambda name: createElement('li', {}, [name]), names)])])"""
        transpiled = transpile_source(input)
        self.assertEqual(expected, transpiled)

    def test_transpileAttributeExpressionsWithVars(self) -> None:
        input = """
from runtime import createElement
a = <Display dimensions={100+200}/>
print(a)
"""
        expected = """from runtime import createElement
a = createElement('Display', {'dimensions': 100 + 200})
print(a)"""
        transpiled = transpile_source(input)
        self.assertEqual(expected, transpiled)

    @unittest.skipIf(
        sys.version_info >= (3, 12), "TODO: differing outputs in 3.12 string quote"
    )
    def test_transpileAttributeExpressionsWithFormattedString(self) -> None:
        input = """
from runtime import createElement
a = <Greeter greeting={f'Have a lovely day {salutation} {person}'}/>
print(a)
"""
        expected = """from runtime import createElement
a = createElement('Greeter', {'greeting': f'Have a lovely day {salutation} {person}'})
print(a)"""
        transpiled = transpile_source(input)
        self.assertEqual(expected, transpiled)

    def test_transpileComponentPassedAsProp(self) -> None:
        input = """
from runtime import createElement
a = <Hello greet={<World/>}/>
print(a)
"""
        expected = """from runtime import createElement
a = createElement('Hello', {'greet': createElement('World', {})})
print(a)"""
        transpiled = transpile_source(input)
        self.assertEqual(expected, transpiled)

    def test_transpileDeclaredComponentPassedAsProp(self) -> None:
        input = """
from runtime import createElement
w = <World/>
a = <Hello greet={w}/>
print(a)
"""
        expected = """from runtime import createElement
w = createElement('World', {})
a = createElement('Hello', {'greet': w})
print(a)"""
        transpiled = transpile_source(input)
        self.assertEqual(expected, transpiled)

    def test_transpileLiteralStringInBlockElement(self) -> None:
        input = """
from runtime import createElement
w = <Hello>"World"</Hello>
print(w)
"""
        expected = """from runtime import createElement
w = createElement('Hello', {}, ['World'])
print(w)"""
        transpiled = transpile_source(input)
        self.assertEqual(expected, transpiled)

    def test_transpileMultipleLiteralStringInBlockElement(self) -> None:
        input = """
from runtime import createElement
w = <Hello>"World"
"Gone By"</Hello>
print(w)
"""
        expected = """from runtime import createElement
w = createElement('Hello', {}, ['World', 'Gone By'])
print(w)"""
        transpiled = transpile_source(input)
        self.assertEqual(expected, transpiled)

    def test_transpileMixedInBlockElement(self) -> None:
        input = """

from runtime import createElement
def greet_me(tagName, props, children):
        return <p>"Morning"</p>

w = <Hello>
<greet_me/>
"World"
"Gone By"</Hello>
print(w)
"""
        expected = """from runtime import createElement

def greet_me(tagName, props, children):
    return createElement('p', {}, ['Morning'])
w = createElement('Hello', {}, [greet_me('greet_me', {}), 'World', 'Gone By'])
print(w)"""
        transpiled = transpile_source(input)
        self.assertEqual(expected, transpiled)


if __name__ == "__main__":
    unittest.main()
