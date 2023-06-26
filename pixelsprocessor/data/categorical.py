"""Contains stuff for handling categorical data (tags)"""

from typing import Optional

class Tag:
    """Represents a single tag"""

    def __init__(self, name: str, category: Optional['Category'] = None, score: Optional[float] = None) -> None:
        """
        Initializes a Tag object.

        Args:
            name (str): The name of the tag.
            category (Category, optional): The category that the tag belongs to. Defaults to None.
            score (float, optional): The score associated with the tag for quantitative analysis. Defaults to None.
        """
        self.name = name
        self.category = category
        self.score = score

    def __str__(self) -> str:
        """Returns a string representation of the Tag object."""
        return f"{self.name} ({self.category.name})" if self.category else self.name

    def __repr__(self) -> str:
        """Returns a string representation of the Tag object."""
        return f"<Tag {self.name}>"

class Category:
    """Represents a single category of tags"""
    
    def __init__(self, name: str, tags: list[Tag]) -> None:
        """Initializes a Category object.
        """
        self.name = name
        for tag in tags:
            tag.category = self
        self.tags = tags
    
    def __str__(self) -> str:
        """Returns a string representation of the Category object.
        """
        return f"{self.name}: {self.tags}"
    
    def __repr__(self) -> str:
        """Returns a string representation of the Category object.
        """
        return f"<Category {self.name}>"

    def add_tag(self, tag: Tag) -> None:
        """Adds a tag to the category."""
        tag.category = self
        self.tags.append(tag)

    def find_tag(self, name: str) -> Tag:
        """Finds a tag in the category by name."""
        for tag in self.tags:
            if tag.name == name:
                return tag
        raise ValueError(f"Tag {name} not found in category {self.name}")
