import datetime
import re
from typing import List, Callable
import json

from .pixel import Pixel
from .categorical import Category, Tag

class PixelDb:
    """Represents a database of pixels"""

    def __init__(self, pixels: List[Pixel], categories: List[Category]) -> None:
        """Initializes a PixelDb object.

        Args:
            pixels (List[Pixel]): The pixels in the database.
            categories (List[Category]): The categories of tags in the database.
        """
        self.pixels = pixels
        self.categories = categories

    def filter_by_tag(self, tag: str) -> List[Pixel]:
        """Filters the database by the given tag.

        Args:
            tag (str): The tag to filter by.

        Returns:
            List[Pixel]: A list of Pixel objects that have a tag that matches the given tag.
        """
        filtered_pixels = []
        for pixel in self.pixels:
            for category, tags in pixel.tags.items():
                for t in tags:
                    if t.name == tag:
                        filtered_pixels.append(pixel)
                        break
        return filtered_pixels
    
    def add_pixel(self, pixel: Pixel) -> None:
        """Adds a pixel to the database.

        Args:
            pixel (Pixel): The pixel to add.
        """
        for category, tags in pixel.tags.items():
            if category not in self.categories:
                self.categories.append(category)
            for tag in tags:
                if tag.category is None:
                    tag.category = category
        self.pixels.append(pixel)

    @classmethod
    def from_json_str(cls, json_str: str) -> 'PixelDb':
        """Creates a PixelDb object from a JSON string.

        Args:
            json_str (str): A string of JSON data to import.

        Returns:
            PixelDb: A PixelDb object created from the JSON data.
        """

        data = json.loads(json_str)

        pixels = []
        categories = []

        for pixel_data in data:
            pixel = Pixel.from_dict(pixel_data)
            pixels.append(pixel)

            for tag_data in pixel_data['tags']:
                category_name = tag_data['type']
                category = next((c for c in categories if c.name == category_name), None)
                if category is None:
                    category = Category(category_name, [])
                    categories.append(category)
                for entry in tag_data['entries']:
                    tag = Tag(entry, category)
                    category.add_tag(tag)
                    pixel.add_tag(tag)

        return cls(pixels, categories)
    
    @classmethod
    def from_json_file(cls, file_path: str) -> 'PixelDb':
        """Creates a PixelDb object from a JSON file.

        Args:
            file_path (str): The path to the JSON file to import.

        Returns:
            PixelDb: A PixelDb object created from the JSON file.
        """
        with open(file_path, 'r') as f:
            return cls.from_json_str(f.read())

class PixelDbQuery:
    """Represents a query on a PixelDb object."""

    def __init__(self, filters = []) -> None:
        """Initializes a PixelDbQuery object.

        Args:
            db (PixelDb): The PixelDb object to query.
        """
        self.filters = filters

    def execute(self, db: PixelDb) -> List[Pixel]:
        """Executes the query and returns the resulting pixels.

        Returns:
            List[Pixel]: The pixels that match the query.
        """
        filtered_pixels = db.pixels
        for f in self.filters:
            filtered_pixels = list(filter(f, filtered_pixels))
        return filtered_pixels

    class Subquery:
        """A placeholder object for a subquery filter function."""
        def __init__(self, filters=None):
            self.filters = filters or []

        def __call__(self, pixel):
            return any(f(pixel) for f in self.filters)

    def parse(self, query_string: str):  # TODO: Make OR and parentheses work
        """Parses a query string and returns a PixelDbQuery object.

        Args:
            query_string (str): The query string to parse.

        Returns:
            PixelDbQuery: The resulting query object.
        """
        self.filters = []
        clauses = re.findall(r"(\(.+?\)|\w+\s*=\s*'.+?')(\s+(AND|OR)\s+|\s*$)", query_string)
        for clause, _, operator in clauses:
            if clause.startswith("("):
                self.filters.append(PixelDb.Subquery())
            elif clause.endswith(")"):
                tag_name, tag_value = re.match(r"(\w+)\s*=\s*'(.+?)'", clause).groups()
                subquery_filters = [lambda pixel, tag_name=tag_name, tag_value=tag_value: any(t.name == tag_value for tags in pixel.tags.values() for t in tags if tags[0].category.name == tag_name)]
                while isinstance(self.filters[-1], PixelDb.Subquery):
                    subquery_filters.extend(self.filters.pop().filters)
                subquery = self.filters.pop()
                subquery.filters = [lambda pixel, subquery_filters=subquery_filters: any(f(pixel) for f in subquery_filters)]
                self.filters.append(subquery)
            else: # TODO: Implement notes CONTAINS and DATE BETWEEN
                tag_name, tag_value = re.match(r"(\w+)\s*=\s*'(.+?)'", clause).groups()
                filter_function = lambda pixel, tag_name=tag_name, tag_value=tag_value: any(t.name == tag_value for tags in pixel.tags.values() for t in tags if tags[0].category.name == tag_name)
                self.filters.append(filter_function)
            if operator:
                if operator.strip().lower() == "and":
                    filter_function = lambda pixel, filters=self.filters[-2:]: all(f(pixel) for f in filters)
                    self.filters = self.filters[:-2]
                    self.filters.append(filter_function)
                # elif operator.strip().lower() == "or":
                #     if len(self.filters) > 1 and isinstance(self.filters[-2], types.LambdaType) and not isinstance(self.filters[-1], Subquery):
                #         filter_function = lambda pixel, filters=self.filters[-2:]: any(f(pixel) for f in filters)
                #         self.filters = self.filters[:-2]
                #         self.filters.append(filter_function)
                #     else:
                #         filter_function = lambda pixel, filters=self.filters[-2:]: any(f(pixel) for f in filters)
                #         self.filters.append(filter_function)
        return self
