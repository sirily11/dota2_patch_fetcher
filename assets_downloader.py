from os import path
import os
import requests
from tqdm import tqdm
import json


def download_image(image_src: str, dest: str):
    """
    Download image
    :param image_src:
    :param dest:
    :return:
    """
    base_name = path.basename(image_src)
    stored_dir = "assets"

    download_path = path.join(os.curdir, "assets", dest, base_name)
    if not path.exists(path.join("assets", dest)):
        os.makedirs(path.join("assets", dest))
    if not path.exists(download_path):
        resp = requests.get(image_src)
        with open(download_path, 'wb+') as f:
            f.write(resp.content)


def main():
    for attr in ["abilities"]:
        p = path.join('resources', attr + '.json')
        with open(p) as f:
            data = json.loads(f.read())
            for key, value, in tqdm(data.items()):
                if 'img' in value:
                    img = value['icon'].replace('png?', 'png')
                    img = img.split('t=')[0]
                    image_path = "https://cdn.dota2.com" + img
                    try:
                        download_image(image_path, attr)
                    except  Exception as e:
                        print(e)


if __name__ == '__main__':
    main()
