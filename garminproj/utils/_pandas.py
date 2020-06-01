import pandas as pd
from sqlalchemy.orm import Query

__all__ = ['dataframe_from_query']


def dataframe_from_query(
        query: Query,

        index_col=None,
        coerce_float=True,
        params=None,
        parse_dates=None,
        columns=None,
        chunksize=None,
):
    """
    From an active sqlalchemy.orm.Query, return a pandas DataFrame

    Parameters
    ----------
    query: `sqlalchemy.orm.Query`
        A query from an active `sqlalchemy.orm.Session`

    index_col
    coerce_float
    params:
    parse_dates
    columns
    chunksize

    Returns
    -------
    pd.DataFrame
        Pandas DataFrame
    """
    return pd.read_sql(
            query.statement,
            query.session.bind,
            index_col=index_col,
            coerce_float=coerce_float,
            params=params,
            parse_dates=parse_dates,
            columns=columns,
            chunksize=chunksize,
    )
