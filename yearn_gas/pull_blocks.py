import requests
import datetime
import os
from tqdm import tqdm

# tqdm example: https://github.com/tqdm/tqdm#hooks-and-callbacks
# london fork block: 12_965_000
# london fork date: 2021-08-05

LONDON_FORK_DATE = "2021-08-05"
DATAFOLDER = "data/raw"


def url(d):
    return f"https://gz.blockchair.com/ethereum/blocks/blockchair_ethereum_blocks_{d}.tsv.gz"


def main():
    print("Pulling blocks...")

    if not os.path.exists(DATAFOLDER):
        os.makedirs(DATAFOLDER)

    fin = datetime.datetime.today().date()
    cur = datetime.datetime.strptime(LONDON_FORK_DATE, "%Y-%m-%d").date()
    while cur < fin:  # don't pull today
        u = url(cur.strftime("%Y%m%d"))
        filename = u.split("/")[-1]
        filepath = f"{DATAFOLDER}/{filename}"

        if not os.path.exists(filepath):  # don't overwrite files
            response = requests.get(u, stream=True)

            with tqdm.wrapattr(
                open(filepath, "wb"),
                "write",
                miniters=1,
                desc=filename,
                total=int(response.headers.get("content-length", 0)),
            ) as f:
                for chunk in response.iter_content(chunk_size=4096):
                    f.write(chunk)

        cur += datetime.timedelta(days=1)


if __name__ == "__main__":
    main()
