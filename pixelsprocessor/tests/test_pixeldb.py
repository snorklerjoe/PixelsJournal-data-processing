import os
import tempfile
import datetime
from pixelsprocessor.data.categorical import Category, Tag
from pixelsprocessor.data.pixel import Pixel
from pixelsprocessor.data.pixeldb import PixelDb, PixelDbQuery

def test_pixeldb_add_pixel():
    db = PixelDb.from_json_str('[{"date": "2023-5-23","type": "Mood","scores": [4],"notes": "Band banquet","tags": [{"type": "Emotions","entries": ["chill","happiness"]}]}]')
    pixel = Pixel(datetime.datetime.now(), 1, "test notes", {})
    db.add_pixel(pixel)
    assert len(db.pixels) == 2
    assert len(db.categories) == 1
    assert db.pixels[0].mood == 4
    assert db.pixels[0].tags_list[0] in db.categories[0].tags
    assert db.pixels[1] == pixel

def test_pixeldbquery_execute_categorical():
    cat1 = Category("color", [Tag("red"), Tag("green"), Tag("blue")])
    cat2 = Category("shape", [Tag("square"), Tag("circle"), Tag("triangle")])
    db = PixelDb([], [cat1, cat2])
    pixel1 = Pixel(datetime.datetime(2022, 1, 1), 1, "test notes 1", {cat1: [cat1.tags[0]], cat2: [cat2.tags[0]]})
    pixel2 = Pixel(datetime.datetime(2022, 1, 2), 2, "test notes 2", {cat1: [cat1.tags[1]], cat2: [cat2.tags[1]]})
    pixel3 = Pixel(datetime.datetime(2022, 1, 3), 3, "test notes 3", {cat1: [cat1.tags[2]], cat2: [cat2.tags[2]]})
    db.add_pixel(pixel1)
    db.add_pixel(pixel2)
    db.add_pixel(pixel3)
    query_string = "WHERE color='red' AND shape='square'"
    query = PixelDbQuery()
    query.parse(query_string)
    filtered_pixels = query.execute(db)
    assert len(filtered_pixels) == 1
    assert filtered_pixels[0] == pixel1

