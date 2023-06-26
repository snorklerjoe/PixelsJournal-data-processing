# Based loosely off of pTinosq's Pixel.py
# https://github.com/pTinosq/pixelsparser/blob/main/src/pixelsparser/Pixel.py

import datetime
import json

from .categorical import Category, Tag

class Pixel:
    """Represents a single pixel in the Pixels Journal app."""

    def __init__(self, date: datetime, mood: int, notes: str, tags: dict[Category, list[Tag]]) -> None:
        """Initializes a Pixel object.
        """
        self.date = date
        self.mood = mood
        self.notes = notes
        self.tags = tags

    def __str__(self) -> str:
        """Returns a string representation of the Pixel object.
        """
        return f"{self.date} : {self.mood} | {self.notes} | {self.tags}"
    
    def __repr__(self) -> str:
        """Returns a string representation of the Pixel object.
        """
        return f"<Pixel {self.date}>"

    def __lt__(self, other: 'Pixel') -> bool:
        """Compares two Pixel objects by date.

        Args:
            other (Pixel): The other Pixel object to compare to.

        Returns:
            bool: True if this Pixel's date is less than the other Pixel's date, False otherwise.
        """
        return self.date < other.date

    def __eq__(self, other: 'Pixel') -> bool:
        """Compares two Pixel objects by date.

        Args:
            other (Pixel): The other Pixel object to compare to.

        Returns:
            bool: True if this Pixel's date is equal to the other Pixel's date, False otherwise.
        """
        return self.date == other.date
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Pixel':
        """Creates a Pixel object from a dictionary.

        Args:
            data (dict): The dictionary to create a Pixel object from.

        Returns:
            Pixel: The Pixel object created from the dictionary.
        """
        date = datetime.datetime.strptime(data["date"], "%Y-%m-%d")
        mood = data["scores"][0]
        notes = data["notes"]
        tags = {}
        return cls(date, mood, notes, tags)

    def add_tag(self, tag: Tag):
        """Adds a tag to the Pixel object.

        Args:
            tag (Tag): The tag to add.
        """
        if tag.category not in self.tags:
            self.tags[tag.category] = []
        self.tags[tag.category].append(tag)

    @property
    def tags_list(self):
        """Returns a list of all tags in the Pixel object.

        Returns:
            list: A list of all tags in the Pixel object.
        """
        tags = []
        for category, tags_list in self.tags.items():
            tags.extend(tags_list)
        return tags
