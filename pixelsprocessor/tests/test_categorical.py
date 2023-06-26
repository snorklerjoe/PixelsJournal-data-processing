from pixelsprocessor.data.categorical import Tag, Category

def test_tag_str():
    tag = Tag("red", Category("color", []))
    assert str(tag) == "red (color)"

def test_tag_repr():
    tag = Tag("red", Category("color", []))
    assert repr(tag) == "<Tag red>"

def test_category_init():
    category = Category("color", [Tag("red"), Tag("green"), Tag("blue")])
    assert category.name == "color"
    assert len(category.tags) == 3

def test_category_add_tag():
    category = Category("color", [])
    tag = Tag("red")
    category.add_tag(tag)
    assert len(category.tags) == 1
    assert category.tags[0].name == "red"
    assert category.tags[0].category == category
