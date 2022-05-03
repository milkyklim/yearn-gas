from tqdm import tqdm
import os
import gzip
import csv
from yearn_gas import db

LONDON_FORK_DATE = "2021-08-05"
DATAFOLDER = "data/raw"

PREFIX = "blockchair_ethereum_blocks"


def main():
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


if __name__ == "__main__":
    main()
