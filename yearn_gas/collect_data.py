import requests
import os
import gzip
import datetime
import csv
from yearn_gas import db
from tqdm import tqdm

# tqdm example: https://github.com/tqdm/tqdm#hooks-and-callbacks
# london fork block: 12_965_000
# london fork date: 2021-08-05

LONDON_FORK_DATE = "2021-08-05"
DATAFOLDER = "data/raw"
PREFIX = "blockchair_ethereum_blocks"


def url(d):
    return f"https://gz.blockchair.com/ethereum/blocks/blockchair_ethereum_blocks_{d}.tsv.gz"


def pull_blocks():
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


def create_db():
    # open session once
    with db.db_session:
        for filename in tqdm(os.listdir(DATAFOLDER)):
            if filename.startswith(PREFIX):
                with gzip.open(f"{DATAFOLDER}/{filename}", "rt") as f:
                    tsv_file = csv.DictReader(f, delimiter="\t")
                    for block in tsv_file:
                        if not db.Block.exists(id=block["id"]):
                            fix_keys = [
                                "hash",
                                "miner",
                                "extra_data_hex",
                                "logs_bloom",
                                "mix_hash",
                                "receipts_root",
                                "sha3_uncles",
                                "state_root",
                                "transactions_root",
                            ]

                            for k in fix_keys:
                                block[k] = block[k].encode()

                            db.Block(**block)


def main():
    pass


if __name__ == "__main__":
    main()
