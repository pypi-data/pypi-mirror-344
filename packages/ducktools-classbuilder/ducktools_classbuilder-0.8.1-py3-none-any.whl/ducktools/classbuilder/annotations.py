# MIT License
#
# Copyright (c) 2024 David C Ellis
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys


def get_ns_annotations(ns):
    """
    Given a class namespace, attempt to retrieve the
    annotations dictionary.

    :param ns: Class namespace (eg cls.__dict__)
    :return: dictionary of annotations
    """

    annotations = ns.get("__annotations__")
    if annotations is not None:
        annotations = annotations.copy()
    else:
        # See if we're using PEP-649 annotations
        # Guarding this with a try/except instead of a version check
        # In case there's a change and PEP-649 somehow doesn't make 3.14
        try:
            from annotationlib import Format, call_annotate_function, get_annotate_function
        except ImportError:
            pass
        else:
            annotate = ns.get("__annotate__")  # Works in the alphas, but may break
            if not annotate:
                annotate = get_annotate_function(ns)
            if annotate:
                annotations = call_annotate_function(annotate, format=Format.FORWARDREF)

    if annotations is None:
        annotations = {}

    return annotations


def is_classvar(hint):
    if isinstance(hint, str):
        # String annotations, just check if the string 'ClassVar' is in there
        # This is overly broad and could be smarter.
        return "ClassVar" in hint
    elif (annotationlib := sys.modules.get("annotationlib")) and isinstance(hint, annotationlib.ForwardRef):
        return "ClassVar" in hint.__arg__
    else:
        _typing = sys.modules.get("typing")
        if _typing:
            # Annotated is a nightmare I'm never waking up from
            # 3.8 and 3.9 need Annotated from typing_extensions
            # 3.8 also needs get_origin from typing_extensions
            if sys.version_info < (3, 10):
                _typing_extensions = sys.modules.get("typing_extensions")
                if _typing_extensions:
                    _Annotated = _typing_extensions.Annotated
                    _get_origin = _typing_extensions.get_origin
                else:
                    _Annotated, _get_origin = None, None
            else:
                _Annotated = _typing.Annotated
                _get_origin = _typing.get_origin

            if _Annotated and _get_origin(hint) is _Annotated:
                hint = getattr(hint, "__origin__", None)

            if (
                hint is _typing.ClassVar
                or getattr(hint, "__origin__", None) is _typing.ClassVar
            ):
                return True
    return False

