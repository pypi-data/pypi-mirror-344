import pytest

from camouflage.utils import extract_module_name


def test_valid_filename():
    assert extract_module_name("/path/to/valid_module.py") == "valid_module"
    assert extract_module_name("another_module.py") == "another_module"
    assert extract_module_name("./simple.py") == "simple"
    assert extract_module_name("/path/to/_valid.py") == "_valid"
    assert extract_module_name("/path/to/module") == "module"


def test_invalid_filename():
    with pytest.raises(ValueError, match=r"Invalid plugin filename \[invalid-module\]"):
        extract_module_name("/path/to/invalid-module.py")

    with pytest.raises(ValueError, match=r"Invalid plugin filename \[123module\]"):
        extract_module_name("/path/to/123module.py")

    with pytest.raises(ValueError, match=r"Invalid plugin filename \[module\ name\]"):
        extract_module_name("/path/to/module name.py")


def test_empty_string():
    with pytest.raises(ValueError, match=r"Invalid plugin filename \[\]"):
        extract_module_name("")
