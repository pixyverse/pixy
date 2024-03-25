import unittest

from pixieverse.pixie.transpile import transpile_source


class TestTranspileSource(unittest.TestCase):
    def test_transpileEmpty(self) -> None:
        input = ""
        expected = ""
        transpiled = transpile_source(input)
        self.assertEquals(expected, transpiled)

    def test_transpilePlainPy(self) -> None:
        input = """a = 1
print(a)
"""
        expected = input
        transpiled = transpile_source(input)
        self.assertEquals(expected, transpiled)

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
print(a)
"""
        transpiled = transpile_source(input)
        self.assertEquals(expected, transpiled)

    def test_transpileSelfWithAttributes(self) -> None:
        input = """
from runtime import createElement
a = <Hello who={'Bertie Wooster'} salutation={'Sir'}/>
print(a)
"""
        expected = """from runtime import createElement
a = createElement('Hello', {'who': "'Bertie Wooster'", 'salutation': "'Sir'"})
print(a)
"""
        transpiled = transpile_source(input)
        self.assertEquals(expected, transpiled)

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
a = createElement('Hello', {'who': "'Bertie Wooster'", 'salutation': "'Mr'",
    'salutation': "'Sir'"})
print(a)
"""
        transpiled = transpile_source(input)
        self.assertEquals(expected, transpiled)

    def test_transpileNestedBlockElements(self) -> None:
        input = """
from runtime import createElement
a = <Terminal><StatusBar></StatusBar></Terminal>
print(a)
"""
        expected = """from runtime import createElement
a = createElement('Terminal', {}, [createElement('StatusBar', {}, [])])
print(a)
"""
        transpiled = transpile_source(input)
        self.assertEquals(expected, transpiled)

    def test_transpileNestedBlockElementsWithAttributes(self) -> None:
        input = """
from runtime import createElement
a = <Terminal width={100}><StatusBar status={'IDLE'}></StatusBar></Terminal>
print(a)
"""
        expected = """from runtime import createElement
a = createElement('Terminal', {'width': 100}, [createElement('StatusBar', {
    'status': "'IDLE'"}, [])])
print(a)
"""
        transpiled = transpile_source(input)
        self.assertEquals(expected, transpiled)

    def test_transpileAttributeExpressionsWithVars(self) -> None:
        input = """
from runtime import createElement
a = <Display dimensions={100+200}/>
print(a)
"""
        expected = """from runtime import createElement
a = createElement('Display', {'dimensions': 100 + 200})
print(a)
"""
        transpiled = transpile_source(input)
        self.assertEquals(expected, transpiled)

    def test_transpileAttributeExpressionsWithFormattedString(self) -> None:
        input = """
from runtime import createElement
a = <Greeter greeting={f'Have a lovely day {salutation} {person}'}/>
print(a)
"""
        expected = """from runtime import createElement
a = createElement('Greeter', {'greeting':
    "f'Have a lovely day {salutation} {person}'"})
print(a)
"""
        transpiled = transpile_source(input)
        self.assertEquals(expected, transpiled)

    def test_transpileComponentPassedAsProp(self) -> None:
        input = """
from runtime import createElement
a = <Hello greet={<World/>}/>
print(a)
"""
        expected = """from runtime import createElement
a = createElement('Hello', {'greet': createElement('World', {})})
print(a)
"""
        transpiled = transpile_source(input)
        self.assertEquals(expected, transpiled)

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
print(a)
"""
        transpiled = transpile_source(input)
        self.assertEquals(expected, transpiled)


if __name__ == "__main__":
    unittest.main()
