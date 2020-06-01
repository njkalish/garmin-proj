from ..models import session_scope, Activity

__all__ = ['query_activities']


def query_activities(*filters):
    with session_scope() as session:
        query = session.query(Activity)
        for filter in filters:
            query = query.filter(filter)
    return query
