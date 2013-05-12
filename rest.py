from docutils.core import publish_doctree
from docutils import writers
from docutils.nodes import GenericNodeVisitor

class Visitor(GenericNodeVisitor):
    def default_visit(self, node):
        pass
    def default_departure(self, node):
        pass
    def visit_strong(self, node):
        print node.tagname
        print node.children
    def visit_emphasis(self, node):
        print node.tagname
        print node.children
    def visit_Text(self, node):
        print node
        print node.parent

text = '''
=====
Title
=====

Subtitle
--------

Section
=======

Subsection
----------

**bold** *italic* normal
'''

document = publish_doctree(text)
visitor = Visitor(document)
document.walkabout(visitor)
