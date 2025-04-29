from sqlalchemy import String, orm

from .base import mapped_column

number_field = lambda **kwargs: mapped_column(  # noqa
    String(256), unique=True, index=True, nullable=False, **kwargs
)

relation_field = lambda back_pop: orm.relationship(  # noqa
    back_populates=back_pop,
    cascade="all, delete-orphan",
    # lazy="joined",
)
