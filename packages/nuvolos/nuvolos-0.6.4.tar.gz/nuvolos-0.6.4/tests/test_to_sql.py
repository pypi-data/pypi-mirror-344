import os
import pytest
import pandas as pd
import numpy as np

from nuvolos import get_connection, to_sql


@pytest.fixture
def df_case_insensitive():
    # Taken from https://github.com/pandas-dev/pandas/blob/7d9dd1a68334cd7a8ed19629c63e84713abc77ef/pandas/tests/io/test_parquet.py#L111
    df = pd.DataFrame(
        {
            "col_string": list("abc"),
            "col_string_with_nan": ["a", np.nan, "c"],
            "col_string_with_none": ["a", None, "c"],
            # "col_bytes": [b"foo", b"bar", b"baz"], : Binary is not supported, as it's not a distinct Pandas type
            "col_unicode": ["foo", "bar", "baz"],
            "col_int": list(range(1, 4)),
            "col_uint": np.arange(3, 6).astype("u1"),
            "col_float": np.arange(4.0, 7.0, dtype="float64"),
            "col_float_with_nan": [2.0, np.nan, 3.0],
            "col_bool": [True, False, True],
            "col_datetime": pd.date_range("20130101", periods=3),
            "col_datetime_with_nat": [
                pd.Timestamp("20130101"),
                pd.NaT,
                pd.Timestamp("20130103"),
            ],
        }
    )
    return df


@pytest.fixture
def df_case_sensitive():
    # Taken from https://github.com/pandas-dev/pandas/blob/7d9dd1a68334cd7a8ed19629c63e84713abc77ef/pandas/tests/io/test_parquet.py#L111
    df = pd.DataFrame(
        {
            "col_String": list("abc"),
            "COL_STRING_WITH_NAN": ["a", np.nan, "c"],
            "COL_STRING_WITH_NONE": ["a", None, "c"],
            # "COL_BYTES": [b"foo", b"bar", b"baz"], : Binary is not supported, as it's not a distinct Pandas type
            "COL_UNICODE": ["foo", "bar", "baz"],
            "col_Int": list(range(1, 4)),
            "COL_UINT": np.arange(3, 6).astype("u1"),
            "COL_FLOAT": np.arange(4.0, 7.0, dtype="float64"),
            "COL_FLOAT_WITH_NAN": [2.0, np.nan, 3.0],
            "col_bool": [True, False, True],
            "COL_DATETIME": pd.date_range("20130101", periods=3),
            "COL_DATETIME_WITH_NAT": [
                pd.Timestamp("20130101"),
                pd.NaT,
                pd.Timestamp("20130103"),
            ],
        }
    )
    df["Seq_Num"] = df.index
    df.set_index("Seq_Num", inplace=True)
    return df


@pytest.fixture
def df_without_ns():
    df = pd.DataFrame(
        {
            "col_without_ns": [
                pd.Timestamp(year=2022, month=9, day=1, hour=2, minute=34, second=56),
                pd.NaT,
                pd.Timestamp(
                    year=2022,
                    month=9,
                    day=1,
                    hour=2,
                    minute=34,
                    second=56,
                    microsecond=123456,
                ),
            ],
        }
    )
    df["seq_num"] = df.index
    df.set_index("seq_num", inplace=True)
    return df


@pytest.fixture
def df_with_ns():
    df = pd.DataFrame(
        {
            "col_with_ns": [
                pd.Timestamp(
                    year=2022,
                    month=9,
                    day=1,
                    hour=2,
                    minute=34,
                    second=56,
                    microsecond=123456,
                    nanosecond=789,
                ),
                pd.NaT,
                pd.Timestamp(
                    year=2022,
                    month=9,
                    day=1,
                    hour=2,
                    minute=34,
                    second=57,
                    microsecond=123456,
                    nanosecond=789,
                ),
            ],
        }
    )
    df["seq_num"] = df.index
    df.set_index("seq_num", inplace=True)
    return df


def test_case_insensitive(df_case_insensitive):
    conn = None
    try:
        conn = get_connection(
            username=os.getenv("TEST_USERNAME"),
            password=os.getenv("TEST_PASSWORD"),
            dbname=os.getenv("TEST_DBNAME"),
            schemaname=os.getenv("TEST_SCHEMANAME"),
        )
        to_sql(
            df=df_case_insensitive,
            name="no_quotes_no_index",
            con=conn,
            database=os.getenv("TEST_DBNAME"),
            schema=os.getenv("TEST_SCHEMANAME"),
            index=False,
            if_exists="replace",
        )
        df_r = pd.read_sql("SELECT * FROM NO_QUOTES_NO_INDEX;", con=conn)
        df_c = df_case_insensitive.compare(df_r)
        assert len(df_c.index) == 0
    finally:
        if conn:
            conn.close()


def test_case_sensitive(df_case_sensitive):
    conn = None
    try:
        conn = get_connection(
            username=os.getenv("TEST_USERNAME"),
            password=os.getenv("TEST_PASSWORD"),
            dbname=os.getenv("TEST_DBNAME"),
            schemaname=os.getenv("TEST_SCHEMANAME"),
        )
        to_sql(
            df=df_case_sensitive,
            name="quotes_AND_index",
            con=conn,
            database=os.getenv("TEST_DBNAME"),
            schema=os.getenv("TEST_SCHEMANAME"),
            index=True,
            if_exists="replace",
        )

        df_r = pd.read_sql(
            'SELECT * FROM "quotes_AND_index";', con=conn, index_col="Seq_Num"
        )

        # Fully-uppercase, quoted columns are also returned as lowercase due to
        # https://github.com/snowflakedb/snowflake-sqlalchemy/issues/157
        df_cols = zip(df_case_sensitive.columns, df_r.columns)
        df_r.columns = [c[1].upper() if c[1].upper() == c[0] else c[1] for c in df_cols]
        df_c = df_case_sensitive.compare(df_r)
        assert len(df_c.index) == 0
    finally:
        if conn:
            conn.close()


def test_check_transaction(df_case_insensitive):
    conn = None
    try:
        conn = get_connection(
            username=os.getenv("TEST_USERNAME"),
            password=os.getenv("TEST_PASSWORD"),
            dbname=os.getenv("TEST_DBNAME"),
            schemaname=os.getenv("TEST_SCHEMANAME"),
        )
        to_sql(
            df=df_case_insensitive,
            name="check_transaction",
            con=conn,
            database=os.getenv("TEST_DBNAME"),
            schema=os.getenv("TEST_SCHEMANAME"),
            index=False,
            if_exists="replace",
        )
    finally:
        if conn:
            conn.close()
    conn2 = None
    try:
        conn2 = get_connection(
            username=os.getenv("TEST_USERNAME"),
            password=os.getenv("TEST_PASSWORD"),
            dbname=os.getenv("TEST_DBNAME"),
            schemaname=os.getenv("TEST_SCHEMANAME"),
        )
        df_r = pd.read_sql("SELECT * FROM check_transaction;", con=conn2)
        df_c = df_case_insensitive.compare(df_r)
        assert len(df_c.index) == 0
    finally:
        if conn2:
            conn2.close()


def test_without_nanoseconds(df_without_ns):
    conn = None
    try:
        conn = get_connection(
            username=os.getenv("TEST_USERNAME"),
            password=os.getenv("TEST_PASSWORD"),
            dbname=os.getenv("TEST_DBNAME"),
            schemaname=os.getenv("TEST_SCHEMANAME"),
        )
        to_sql(
            df=df_without_ns,
            name="without_ns",
            con=conn,
            database=os.getenv("TEST_DBNAME"),
            schema=os.getenv("TEST_SCHEMANAME"),
            index=False,
            if_exists="replace",
        )
    finally:
        if conn:
            conn.close()
    conn2 = None
    try:
        conn2 = get_connection(
            username=os.getenv("TEST_USERNAME"),
            password=os.getenv("TEST_PASSWORD"),
            dbname=os.getenv("TEST_DBNAME"),
            schemaname=os.getenv("TEST_SCHEMANAME"),
        )
        df_r = pd.read_sql("SELECT * FROM without_ns;", con=conn2)
        df_c = df_without_ns.compare(df_r)
        assert len(df_c.index) == 0
    finally:
        if conn2:
            conn2.close()


def test_with_nanoseconds(df_with_ns):
    conn = None
    try:
        conn = get_connection(
            username=os.getenv("TEST_USERNAME"),
            password=os.getenv("TEST_PASSWORD"),
            dbname=os.getenv("TEST_DBNAME"),
            schemaname=os.getenv("TEST_SCHEMANAME"),
        )
        to_sql(
            df=df_with_ns,
            name="with_ns",
            con=conn,
            database=os.getenv("TEST_DBNAME"),
            schema=os.getenv("TEST_SCHEMANAME"),
            index=False,
            if_exists="replace",
        )
    finally:
        if conn:
            conn.close()
    conn2 = None
    try:
        conn2 = get_connection(
            username=os.getenv("TEST_USERNAME"),
            password=os.getenv("TEST_PASSWORD"),
            dbname=os.getenv("TEST_DBNAME"),
            schemaname=os.getenv("TEST_SCHEMANAME"),
        )
        df_r = pd.read_sql("SELECT * FROM with_ns;", con=conn2)
        df_c = df_with_ns.compare(df_r)
        assert len(df_c.index) == 0
    finally:
        if conn2:
            conn2.close()
