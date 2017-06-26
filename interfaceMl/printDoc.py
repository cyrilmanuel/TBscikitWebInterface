import ast
import re
from numpydoc.docscrape import NumpyDocString

default_re = re.compile(r'\bdefault\s*[=:]\s*(?P<default>[^\)\b]+)')
types_re = re.compile(r"(?P<type>(float|int(eger)?|str(ing)?|bool(ean)?|dict|))")

type_map = {
    'string': str,
    'str': str,
    'boolean': bool,
    'bool': bool,
    'int': int,
    'integer': int,
    'float': float,
    'dict': dict,
}


def getDicoParams(instanceClassifier):
    doc = NumpyDocString("    " + instanceClassifier.__doc__)  # hack
    dico = {}
    for name, type_, descriptions in doc['Parameters']:

        match = types_re.finditer(type_)
        types = (t.group('type') for t in match)

        types = [type_map.get(t, t) for t in types]

        match = default_re.search(type_)
        if match:
            default = ast.literal_eval(match.group('default'))
        else:
            default = None
        dico[name] = types[0]
        # print(name, types, default)
