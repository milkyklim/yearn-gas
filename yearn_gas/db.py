from datetime import date, datetime, time
from decimal import Decimal
from pony.orm import Database, PrimaryKey, Required, db_session
from os import environ


db = Database()


class Block(db.Entity):
    """Whole one block data"""

    _table_ = "block"
    id = PrimaryKey(int)
    hash = Required(bytes, unique=True)
    time = Required(datetime, unique=True)
    size = Required(int)
    miner = Required(bytes)
    extra_data_hex = Required(bytes)
    difficulty = Required(str)  # Required(int, size=64)
    gas_used = Required(int)
    gas_limit = Required(int)
    logs_bloom = Required(bytes)  # ?
    mix_hash = Required(bytes)
    nonce = Required(str)  # Required(int, size=64)
    receipts_root = Required(bytes)
    sha3_uncles = Required(bytes)
    state_root = Required(bytes)
    total_difficulty = Required(str)  # Required(int, size=64)
    transactions_root = Required(bytes)
    uncle_count = Required(int)
    transaction_count = Required(int)
    synthetic_transaction_count = Required(int)
    call_count = Required(int)
    synthetic_call_count = Required(int)
    value_total = Required(str)  # Required(int, size=64)
    value_total_usd = Required(Decimal)
    internal_value_total = Required(str)  # Required(int, size=64)
    internal_value_total_usd = Required(Decimal)
    generation = Required(str)  # Required(int, size=64)
    generation_usd = Required(Decimal)
    uncle_generation = Required(str)  # Required(int, size=64)
    uncle_generation_usd = Required(Decimal)
    fee_total = Required(str)  # Required(int, size=64)
    fee_total_usd = Required(Decimal)
    reward = Required(str)  # Required(int, size=64)
    reward_usd = Required(Decimal)


db.bind("sqlite", "../data/db-test.sqlite", create_db=True)
# db.bind('sqlite', ':memory:', create_db=True)
db.generate_mapping(create_tables=True)
