from pprint import pprint
from typing import List
from os import path
import os
from requests_html import HTMLSession, HTMLResponse, HTML
import requests
from .objects import GeneralInfo, ItemInfo, HeroInfo, SkillInfo
from tqdm import tqdm

username = os.getenv("news-feed-username")
password = os.getenv("news-feed-password")


class PatchFetcher:
    def __init__(self, version="7.26a"):
        self.version = version
        self.baseURL = f"http://www.dota2.com/patches/{version}"
        self.baseGitURL = "https://sirily11.github.io/dota2_patch_fetcher"

    def fetch_versions(self) -> List[str]:
        a_session = HTMLSession()
        r: HTMLResponse = a_session.get(self.baseURL)
        container = r.html.find("select", first=True)
        options = []
        for o in container.find("option"):
            if "value" in o.attrs:
                options.append(o.text)
        return options

    def download_image(self, image_src: str, dest: str):
        """
        Download image and then return new git url
        :param image_src:
        :param dest:
        :return:
        """
        base_name = path.basename(image_src)
        download_path = path.join(os.curdir, "download", dest, base_name)
        if not path.exists(path.join("download", dest)):
            os.makedirs(path.join("download", dest))
        if not path.exists(download_path):
            resp = requests.get(image_src)
            with open(download_path, 'wb+') as f:
                f.write(resp.content)
        return os.path.join(self.baseGitURL, "download", dest, base_name)

    def upload(self):
        username = os.getenv("username")
        password = os.getenv("password")
        auth_url = "http://0.0.0.0:8000"
        url = "http://0.0.0.0:8000/dota2/version/"
        auth = requests.post(f"{auth_url}/api/token/",
                             {"username": username, "password": password})
        hed = {'Authorization': 'Bearer ' + auth.json()['access']}
        data = self.fetch()
        res = requests.post(url, json=data.to_json(), headers=hed)
        if res.status_code == 201:
            pprint(res.json())
        else:
            print("error")
        print("Finished...")

    def fetch(self):
        a_session = HTMLSession()
        r: HTMLResponse = a_session.get(self.baseURL)
        print("Fetching...")
        general = self.fetch_general(r.html)
        items = self.fetch_item(r.html)
        heroes = self.fetch_hero(r.html)
        general.heroes = heroes
        general.items = items
        return general

    def fetch_general(self, response: HTML) -> GeneralInfo:
        container = response.find("#GeneralSection", first=True)
        if not container:
            return GeneralInfo(version=self.version, description="None", items=None, heroes=None)
        patch_list = container.find(".PatchNote")
        content = ""
        for patch in tqdm(patch_list, desc="Fetching general"):
            content += f"{patch.text}\n"
        return GeneralInfo(version=self.version, description=content, items=None, heroes=None)

    def fetch_item(self, response: HTML) -> List[ItemInfo]:
        container = response.find("#ItemsSection", first=True)
        if not container:
            return []
        item_notes = container.find(".ItemNotes")
        items = []
        for i in tqdm(item_notes, desc="Fetching items"):
            img = i.find(".ItemImage", first=True)
            name = i.find(".ItemName", first=True)
            patch_notes = i.find(".PatchNote")
            content = ""
            for patch in patch_notes:
                content += f"{patch.text}\n"
            if img:
                image = img.attrs.get('src')
                if image:
                    image = self.download_image(image, dest="item")
                item = ItemInfo(name=name.text, update_description=content, image=image)
                items.append(item)
        return items

    def fetch_hero(self, response: HTML) -> List[HeroInfo]:
        container = response.find("#HeroesSection", first=True)
        if not container:
            return []
        hero_list = container.find(".HeroNotes")
        heroes = []
        for hero in tqdm(hero_list, desc="Fetching Heroes"):
            hero_name = hero.find(".HeroName", first=True)
            hero_image = hero.find(".HeroImage", first=True)

            skills = []
            talent_note = hero.find(".TalentNotes", first=True)
            hero_note = hero.find(".HeroNotesList", first=True)
            ability_notes = hero.find(".HeroAbilityNotes")
            if talent_note:
                label = "Talents"
                patches = ""
                for patch in talent_note.find(".PatchNote"):
                    patches += f"{patch.text}\n"
                skills.append(
                    SkillInfo(
                        name=label,
                        update_description=patches,
                        image=None
                    )
                )

            if hero_note:
                patches = ""
                for patch in hero_note.find(".PatchNote"):
                    patches += f"{patch.text}\n"
                skills.append(
                    SkillInfo(
                        name="Hero",
                        update_description=patches,
                        image=None
                    )
                )

            for ability in ability_notes:
                img = ability.find(".AbilityImage", first=True)
                name = ability.find(".AbilityName", first=True)
                patches = ""
                for patch in ability.find(".PatchNote"):
                    patches += f"{patch.text}\n"
                if img:
                    image = img.attrs.get("src")
                    if image:
                        image = self.download_image(image, dest="ability")
                    skills.append(
                        SkillInfo(
                            name=name.text,
                            image=image,
                            update_description=patches
                        )
                    )

            if hero_image:
                hero_image_src = hero_image.attrs.get("src")
                if hero_image_src:
                    hero_image_src = self.download_image(hero_image_src, dest="hero")
                heroes.append(
                    HeroInfo(
                        name=hero_name.text,
                        image=hero_image_src,
                        skills=skills,
                        update_description=None
                    )
                )
        return heroes
