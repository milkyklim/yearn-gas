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
                            fixy = [
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

                            for f in fixy:
                                block[f] = block[f].encode()

                            db.Block(**block)

                            # block = db.Block(
                            #     id=line["id"],
                            #     hash=line["hash"].encode(),
                            #     time=line["time"],
                            #     size=line["size"],
                            #     miner=line["miner"].encode(),
                            #     extra_data_hex=line["extra_data_hex"].encode(),
                            #     difficulty=line["difficulty"],
                            #     gas_used=line["gas_used"],
                            #     gas_limit=line["gas_limit"],
                            #     logs_bloom=line["logs_bloom"].encode(),
                            #     mix_hash=line["mix_hash"].encode(),
                            #     nonce=line["nonce"],
                            #     receipts_root=line["receipts_root"].encode(),
                            #     sha3_uncles=line["sha3_uncles"].encode(),
                            #     state_root=line["state_root"].encode(),
                            #     total_difficulty=line["total_difficulty"],
                            #     transactions_root=line["transactions_root"].encode(),
                            #     uncle_count=line["uncle_count"],
                            #     transaction_count=line["transaction_count"],
                            #     synthetic_transaction_count=line["synthetic_transaction_count"],
                            #     call_count=line["call_count"],
                            #     synthetic_call_count=line["synthetic_call_count"],
                            #     value_total=line["value_total"],
                            #     value_total_usd=line["value_total_usd"],
                            #     internal_value_total=line["internal_value_total"],
                            #     internal_value_total_usd=line["internal_value_total_usd"],
                            #     generation=line["generation"],
                            #     generation_usd=line["generation_usd"],
                            #     uncle_generation=line["uncle_generation"],
                            #     uncle_generation_usd=line["uncle_generation_usd"],
                            #     fee_total=line["fee_total"],
                            #     fee_total_usd=line["fee_total_usd"],
                            #     reward=line["reward"],
                            #     reward_usd=line["reward_usd"],
                            # )


if __name__ == "__main__":
    main()
