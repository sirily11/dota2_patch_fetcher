from patch_fetcher.patch_fetcher import PatchFetcher
from pprint import pprint

if __name__ == '__main__':
    p = PatchFetcher(version='7.24')
    g = p.fetch()
    pprint(g.to_json())
