# kvlang

Grammar and parser for [Kv][kv] ([wiki][wiki]) as a more reliable approach for
reading the `.kv` files.

Install from PyPI:

```
pip install kvlang
```

or from the repo:

```
git clone https://github.com/KeyWeeUsr/kvlang
pip install -e .
# or
pip install git+https://github.com/KeyWeeUsr/kvlang.git
# or
pip install https://github.com/KeyWeeUsr/kvlang/zipball/master
# or
pip install https://github.com/KeyWeeUsr/kvlang/zipball/1.0.0
```

then

```python
from kvlang import parse

print(parse("#:kivy 2.3.1"))
# Tree(Token('RULE', 'start'), [Tree(Token('RULE', 'special'), [...])])

print(parse("#:kivy 2.3.1").pretty())
# start
#   special
#     special_directive
#       kivy_version
#          
#         version
#           2
#           3
#           1
```

[kv]: https://kivy.org/doc/stable/guide/lang.html
[wiki]: https://en.wikipedia.org/wiki/Kivy_(framework)#Kv_language
