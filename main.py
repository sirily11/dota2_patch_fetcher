from patch_fetcher.patch_fetcher import PatchFetcher
from pprint import pprint

if __name__ == '__main__':
    p = PatchFetcher()
    g = p.fetch()
    pprint(g.to_json())
