from patch_fetcher.patch_fetcher import PatchFetcher
from pprint import pprint
from tqdm import tqdm

if __name__ == '__main__':
    p = PatchFetcher(version='7.22')
    # g = p.upload()
    versions = p.fetch_versions()
    for v in tqdm(versions):
        try:
            print("Uploading version ", v)
            p = PatchFetcher(version=v)
            p.upload()
        except Exception as e:
            print(e)
