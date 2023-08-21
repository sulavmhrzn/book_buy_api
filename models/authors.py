from beanie import Document


class Author(Document):
    first_name: str
    last_name: str

    class Settings:
        name = "authors"
