from arpeggio import Optional, ZeroOrMore, OneOrMore, EOF, PTNodeVisitor, visit_parse_tree
from arpeggio import RegExMatch as _
from arpeggio import ParserPython


class CalcVisitor(PTNodeVisitor):
    def visit_number(self, node, children):
        return float(node.value)

    def visit_factor(self, node, children):
        if len(children) == 1:
            return children[0]
        sign = -1 if children[0] == '-' else 1
        return sign * children[-1]

    def visit_term(self, node, children):
        if len(children) == 1:
            return children[0]
        return node

    def visit_expression(self, node, children):
        """
        Adds or subtracts terms.
        Term nodes will be already evaluated.
        """
        if self.debug:
            print("Expression {}".format(children))
        expr = children[0]
        for i in range(2, len(children), 2):
            if i and children[i - 1] == "-":
                expr -= children[i]
            else:
                expr += children[i]
        if self.debug:
            print("Expression = {}".format(expr))
        return expr



# Lista betyer eller.
# Komma betyder "följt av"
def number():
    return _(r'\d*\.\d*|\d+')


def factor():
    return Optional(["+", "-"]), [number, ("(", expression, ")")]


def term():
    return factor, ZeroOrMore(["*", "/"], factor)


def expression():
    return term, ZeroOrMore(["+", "-"], term)


def calc():
    return OneOrMore(expression), EOF


def main():
    parser = ParserPython(calc)  # calc is the root rule of your grammar
    # Use param debug=True for verbose debugging
    # messages and grammar and parse tree visualization
    # using graphviz and dot

    parse_tree = parser.parse("-(4-1)*5+(2+4.67)+5.89/(.2+7)")
    print(parse_tree)
    result = visit_parse_tree(parse_tree, CalcVisitor(debug=False))
    print(result)


if __name__ == "__main__":
    main()

