from arpeggio import PTNodeVisitor, visit_parse_tree
from arpeggio.cleanpeg import ParserPEG


class JavaClass:
    def __init__(self, name, parent, interface_list=None):
        self.name = name
        if parent is None:
            self.parent = "java.lang.Object"
        else:
            self.parent = parent
        self.interface_list = interface_list
        self.methods = [[]]
        self._visibility = "package-private"

    def set_visibility(self, vis):
        if vis is not None:
            self._visibility = vis

    def __str__(self):
        if self.interface_list is not None:
            iflist = f"implements {', '.join(self.interface_list)}"
        else:
            iflist = ""
        return f"{self._visibility} class {self.name} extends {self.parent} {iflist} {{ {[str(m) for m in self.methods]} }}"

    def set_methods(self, methods):
        if methods == None:
            methods = [[]]
        self.methods = methods[0]


class JavaMethod:
    def __init__(self, name, arg_list):
        self.name = name
        self.arg_list = arg_list

    def __str__(self):
        return "Method: " + str(self.__dict__)


class CalcVisitor(PTNodeVisitor):

    def visit_java(self, node, children):
        return children.results["class"]

    def visit_class(self, node, children):
        parent = children.results.get("parent", [None])[0]
        iflist = children.results.get("interface_list", [None])[0]
        jc = JavaClass(children.results["typename"][0], parent, iflist)
        visibility = children.results.get('visibility', [None])[0]
        jc.set_visibility(visibility)
        jc.set_methods(children.results.get("class_body"))
        return jc

    def visit_interface_list(self, node, children):
        return children.results['identifier']

    def visit_method(self, node, children):
        jm = JavaMethod(children.results["identifier"], [])
        jm.return_type = children.results["typename"]
        jm.arg_list = children.results.get("argument_list", [None])[0]
        return jm;

    def visit_argument_list(self, node, children):
        return children.results["typename"]

    def visit_class_body(self, node, children):
        return children.results.get("method", None)

def main():
    with open('java2.peg', 'r') as file:
        data = file.read()
    parser = ParserPEG(data, "java")

#    ok_samples = [
#        "class Baz extends Korv implements Runnable, Comparable {}",
#        "class Bar implements Runnable, Comparable {}",
#        "class Korv extends Fisk {}",
#        "class Knas {}",
#        "class Foo implements Runnable {}",
        # "class HejA { int foo() {} }",
        #"class HejB { int foo(String apaB) {} }",
        #"class HejC { int foo(String apaC, int korvC) {} }",
        #"class HejD { int foo(String apaD, int korvD, Object raketD) {} }",
        #"class HejE { int foo() {}  void bar(){} }",
        #"class HejF extends Knas { int foo() {}  void bar(){} }",
        #"class HejG extends Knas implements Runnable { int foo() {}  void bar(){} }",
#    ]
#    fail_samples = [
#        "class {}",
#        "class Knas extends implements Runnable {}",
#        "class Foo implements {}",
#    ]
    ok_samples = [
        "sampleinputs/SampleD.java",
        "sampleinputs/SampleB.java",
        "sampleinputs/SampleC.java",
        "sampleinputs/SampleA.java",

    ]
    for input_file in ok_samples:
        with open(input_file, 'r') as file:
            input_expr = file.read()
        parse_tree = parser.parse(input_expr)
        result = visit_parse_tree(parse_tree, CalcVisitor(debug=False))
        print(str(result[0]))

 #   failures = 0;
 #   for input_expr in fail_samples:
 #       try:
 #           parse_tree = parser.parse(input_expr)
 #           print(parse_tree)
 #       except:
 #           failures += 1
 #   print(f"Failed {failures} out of {len(fail_samples)} negative examples ({failures / len(fail_samples) * 100}%)")


if __name__ == "__main__":
    main()
