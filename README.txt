===========
Action Mapper
===========

TestUtils provides such and such and so and so. You might find
it most useful for tasks involving <x> and also <y>. Typical usage
often looks like this::

    #!/usr/bin/env python3.6

    import testutils

    ds = testutils.DataStore()

    def append_a(string: str) -> str:
        return f"{string}a"

    def test_append_a():
        assert append_a(ds.str_x)==f"{ds.str_x}a"


(Note the double-colon and 4-space indent formatting above.)

Paragraphs are separated by blank lines. *Italics*, **bold**,
and ``monospace`` look like this.


A Section
=========

Lists look like this:

* First

* Second. Can be multiple lines
  but must be indented properly.

A Sub-Section
-------------

Numbered lists look like you'd expect:

1. hi there

2. must be going

Urls are http://like.this and links can be
written `like this <http://www.example.com/foo/bar>`_.