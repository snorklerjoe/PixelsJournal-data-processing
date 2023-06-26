from datetime import datetime
from pixelsprocessor.data.categorical import Category, Tag
from pixelsprocessor.data.pixel import Pixel

def test_pixel_str():
    cat1 = Category("color", [Tag("red"), Tag("green"), Tag("blue")])
    cat2 = Category("shape", [Tag("square"), Tag("circle"), Tag("triangle")])
    pixel = Pixel(datetime(2022, 1, 1), 3, "some notes", {cat1: [cat1.tags[0]], cat2: [cat2.tags[0]]})
    assert str(pixel) == "2022-01-01 00:00:00 : 3 | some notes | {<Category color>: [<Tag red>], <Category shape>: [<Tag square>]}"

def test_pixel_repr():
    pixel = Pixel(datetime(2022, 1, 1), 3, "some notes", {})
    assert repr(pixel) == "<Pixel 2022-01-01 00:00:00>"

def test_pixel_lt():
    pixel1 = Pixel(datetime(2022, 1, 1), 3, "some notes", {})
    pixel2 = Pixel(datetime(2022, 1, 2), 4, "some other notes", {})
    assert pixel1 < pixel2
    assert not pixel2 < pixel1

def test_pixel_eq():
    pixel1 = Pixel(datetime(2022, 1, 1), 3, "some notes", {})
    pixel2 = Pixel(datetime(2022, 1, 1), 3, "some notes", {})
    pixel3 = Pixel(datetime(2022, 1, 2), 4, "some other notes", {})
    assert pixel1 == pixel2
    assert not pixel1 == pixel3

def test_pixel_add_tag():
    cat1 = Category("color", [Tag("red"), Tag("green"), Tag("blue")])
    pixel = Pixel(datetime(2022, 1, 1), 3, "some notes", {cat1: [cat1.tags[0]]})
    pixel.add_tag(cat1.tags[1])
    assert pixel.tags == {cat1: [cat1.tags[0], cat1.tags[1]]}

def test_pixel_tags_list():
    cat1 = Category("color", [Tag("red"), Tag("green"), Tag("blue")])
    cat2 = Category("mood", [Tag("happy"), Tag("sad"), Tag("angry")])
    pixel = Pixel(datetime(2022, 1, 1), cat2.tags[0], "some notes", {cat1: [cat1.tags[0]], cat2: [cat2.tags[1], cat2.tags[2]]})
    assert pixel.tags_list == [cat1.tags[0], cat2.tags[1], cat2.tags[2]]
