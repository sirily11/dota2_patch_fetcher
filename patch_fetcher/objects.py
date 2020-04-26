from typing import List, Optional


class ItemInfo:
    def __init__(self, name: str, update_description: str, image: str):
        self.name = name
        self.update_description = update_description
        self.image = image

    def to_json(self):
        return {
            "name": self.name,
            "update_description": self.update_description,
            "image": self.image
        }


class SkillInfo:
    def __init__(self, name: str, update_description: str, image: Optional[str]):
        self.name = name
        self.update_description = update_description
        self.image = image

    def to_json(self):
        if self.update_description is None:
            print("None!!!")
        return {
            "name": self.name,
            "update_description": self.update_description,
            "image": self.image,
        }


class HeroInfo:
    def __init__(self, name: str, update_description: Optional[str], image: str, skills: List[SkillInfo]):
        self.name = name
        self.update_description = update_description
        self.image = image
        self.skills = skills

    def to_json(self):
        return {
            "name": self.name,
            "image": self.image,
            "skills": [s.to_json() for s in self.skills]
        }


class GeneralInfo:
    def __init__(self, version: str, description: str,
                 items: Optional[List[ItemInfo]], heroes: Optional[List[HeroInfo]]):
        self.version = version
        self.description = description
        self.items = items
        self.heroes = heroes

    def to_json(self):
        return {
            "version": self.version,
            "update_description": self.description,
            "items": [i.to_json() for i in self.items],
            "heroes": [h.to_json() for h in self.heroes]
        }
