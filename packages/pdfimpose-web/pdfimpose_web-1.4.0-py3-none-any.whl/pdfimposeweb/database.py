# Copyright 2024-2025 Louis Paternault
#
# This file is part of pdfimpose-web.
#
# Pdfimpose-web is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# Pdfimpose-web is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with pdfimpose-web. If not, see <https://www.gnu.org/licenses/>.

"""Define and process database."""

# pylint: disable=too-few-public-methods

import collections
import datetime
import functools
import itertools
import logging
import math
import typing

from flask_babel import lazy_pgettext as pgettext
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, exc, func
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column


class Base(MappedAsDataclass, DeclarativeBase):
    """Base SQLAlchemy class."""


db = SQLAlchemy(model_class=Base)


class DailyStat(db.Model):
    """Statistics about one single day.

    - How many files were processed that day?
    - What were their total size (in bytes)?
    """

    layout: Mapped[str] = mapped_column(String(32), primary_key=True)
    date: Mapped[datetime.date] = mapped_column(
        primary_key=True, default_factory=datetime.date.today
    )
    files: Mapped[int] = mapped_column(default=0)
    size: Mapped[int] = mapped_column(default=0)


def init(app):
    """Initialize the database.

    If the tables do not exist, they are created.
    """
    if "SQLALCHEMY_ENGINE_OPTIONS" not in app.config:
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {}
    app.config["SQLALCHEMY_ENGINE_OPTIONS"].update({"pool_recycle": 280})
    db.init_app(app)

    with app.app_context():
        db.create_all()
        if not db.session.query(DailyStat).first():
            # Database is empty.
            # Create an empty row: it will be used to know the date the application was started on.
            db.session.add(DailyStat(layout=""))
            db.session.commit()


def add(size: int, layout: str):
    """Record the information that a new file has been processed.

    :param int size: The file size, in bytes.

    The database is changed to record that:
    *today*, *one* more file of *size* Mb has been processed.
    """
    # Avoiding the weird condition where today() changes *while running this function*.
    today = datetime.date.today()

    if db.session.get(DailyStat, {"layout": layout, "date": today}) is None:
        try:
            db.session.add(DailyStat(layout=layout))
            db.session.commit()
        except exc.IntegrityError:
            # Today statistics has already been created by another process.
            db.session.rollback()

    todaystat = db.session.get(DailyStat, {"layout": layout, "date": today})
    todaystat.files = todaystat.files + 1
    todaystat.size = todaystat.size + size
    db.session.commit()


_UNITS = [
    pgettext("unit", "b"),
    pgettext("unit", "kb"),
    pgettext("unit", "Mb"),
    pgettext("unit", "Gb"),
    pgettext("unit", "Tb"),
    pgettext("unit", "Pb"),
]


def _between(low, number, hight):
    return min(max(number, low), hight)


def prettyprint_size(size: int, *, round_func: typing.Callable = None) -> str:
    """Return a human readable size.

    :param int size: Size, in bytes.
    :return: A human readable size.

    >>> prettyprint_size(12345)
    l'12.345 kb'
    >>> prettyprint_size(51_234_567, round_func=round)
    l'51 Mb'
    """
    if size == 0:
        power3 = 0
    else:
        power3 = _between(0, math.floor(math.log(size, 1000)), len(_UNITS) - 1)
    if round_func is None:
        round_func = lambda x: x  #  pylint: disable=unnecessary-lambda-assignment

    return pgettext(
        "unit",
        "%(size)s %(unit)s",
        size=round_func(size / 10 ** (3 * power3)),
        unit=_UNITS[power3],
    )


def ttl_cache(delta: datetime.timedelta):
    """A function cache that calls the actual function once every `delta` time.

    Only works with functions that take no arguments.
    """

    def wrapper(function: typing.Callable):
        # The idea is to use :func:`functools.lru_cache` with a dummy argument
        # that changes each day. Idea borrowed from Peng Qian
        # https://www.dataleadsfuture.com/implement-a-cache-decorator-with-time-to-live-feature-in-python/

        def count() -> int:
            """Increment value each day"""
            start = datetime.datetime.now()
            while True:
                yield math.floor((datetime.datetime.now() - start) / delta)

        counter = count()

        @functools.lru_cache(maxsize=1)
        def lru_cached_func(dummy):  #  pylint: disable=unused-argument
            """Dummy function to make :func:`functools.lru_cache` handle cache.

            The dummy argument is changed every time we want to run the
            function instead of returning the cached data.
            """
            return function()

        def wrapped():
            return lru_cached_func(next(counter))

        return wrapped

    return wrapper


@ttl_cache(datetime.timedelta(days=1))
def stat() -> dict:
    """Return some statistics about this application since it was started.

    Data is:
    - number of files processed;
    - year it was started on;
    - total size of processed files.

    Might return an empty dictionary if an exception is raised while querying the database.
    """
    try:
        files, size = db.session.execute(
            db.select(func.sum(DailyStat.files), func.sum(DailyStat.size))
        ).first()
        year = (
            db.session.execute(db.select(DailyStat.date).order_by("date"))
            .first()[0]
            .year
        )
    except exc.SQLAlchemyError as error:
        logging.warning("Error while querying statistics from the database: %s", error)
        return {}
    return {
        "files": files,
        "year": year,
        "size": prettyprint_size(size, round_func=math.floor),
    }


# Dialect-agnostic function to format date
def strftime(dialect, date, dateformat):
    """Format date according to dialect."""
    if dialect == "sqlite":
        return func.strftime(dateformat, date)
    if dialect == "mysql":
        return func.date_format(date, dateformat)
    if dialect == "postgresql":
        return func.to_char(date, dateformat)
    raise NotImplementedError(
        f"Dialect {dialect} is not supported. Please submit an issue or a patch."
    )


def _iter_months(start, end):
    """Iter first days of month from start to end.

    The first item is the first day of the month of `start`.
    The last item is the first day of the month of `end`.

    >>> list(_iter_months(datetime.date(2024, 11, 10), datetime.date(2025, 1, 7)))
    [datetime.date(2024, 11, 1), datetime.date(2024, 12, 1), datetime.date(2025, 1, 1)]
    """
    month = start.replace(day=1)
    while month <= end:
        yield month
        month = (month + datetime.timedelta(days=31)).replace(day=1)


def _iter_days(start, end):
    """Iter days from start to end.

    >>> list(_iter_days(datetime.date(2023, 12, 31), datetime.date(2024, 1, 2)))
    [datetime.date(2023, 12, 31), datetime.date(2024, 1, 1), datetime.date(2024, 1, 2)]
    """
    day = start
    while day <= end:
        yield day
        day += datetime.timedelta(days=1)


def _iter_years(start, end):
    """Iter first days of years from start to end.

    The first item is the first day of the year of `start`.
    The last item is the first day of the year of `end`.

    >>> list(_iter_years(datetime.date(2022, 2, 20), datetime.date(2024, 11, 7)))
    [datetime.date(2022, 1, 1), datetime.date(2023, 1, 1), datetime.date(2024, 1, 1)]
    """
    year = start.replace(month=1, day=1)
    while year <= end:
        yield year
        year = (year + datetime.timedelta(days=366)).replace(month=1, day=1)


def get_history_all(period="day", /, *, dateformat):
    """Return the history of processed files.

    Returned value is a tuple of three lists `(dates, files, sizes)`, sorted by dates.
    For instance, `files[0]` files (totalizing `sizes[0]` bytes) have been processed on `dates[0]`.

    Dates are formatted using `dateformat`.
    """
    if period == "year":
        history = {
            date.replace(month=1, day=1): (files, size)
            for (date, files, size) in db.session.query(
                func.min(DailyStat.date),
                func.sum(DailyStat.files),
                func.sum(DailyStat.size),
            ).group_by(strftime(db.engine.name, DailyStat.date, "%Y"))
        }
        # Fill in the blanks with (0, 0) on missing years
        history = [
            (date, *history.get(date, (0, 0)))
            for date in _iter_years(min(history.keys()), datetime.date.today())
        ]
    elif period == "month":
        history = {
            date.replace(day=1): (files, size)
            for (date, files, size) in db.session.query(
                func.min(DailyStat.date),
                func.sum(DailyStat.files),
                func.sum(DailyStat.size),
            ).group_by(strftime(db.engine.name, DailyStat.date, "%Y-%m"))
        }
        # Fill in the blanks with (0, 0) on missing months
        history = [
            (date, *history.get(date, (0, 0)))
            for date in _iter_months(min(history.keys()), datetime.date.today())
        ]
    elif period == "day":
        history = {
            date: (file, size)
            for date, file, size in db.session.query(
                DailyStat.date,
                func.sum(DailyStat.files).label("total_files"),
                func.sum(DailyStat.size).label("total_size"),
            )
            .group_by(DailyStat.date)
            .order_by(DailyStat.date)
            .all()
        }
        # Fill in the blanks with (0, 0) on missing days
        history = [
            (date, *history.get(date, (0, 0)))
            for date in _iter_days(min(history.keys()), datetime.date.today())
        ]
    else:
        raise ValueError()

    return list(
        zip(
            *sorted(
                (date.strftime(dateformat), files, size)
                for date, files, size in history
            )
        )
    )


def get_history_layouts(period="day", /, *, dateformat):
    """Return the history of processed files.

    Returned value is a tuple of three lists `(dates, files, sizes)`, sorted by dates.
    For instance, `files[0]` files (totalizing `sizes[0]` bytes) have been processed on `dates[0]`.

    Dates are formatted using `dateformat`.
    """
    if period == "year":
        history = collections.defaultdict(lambda: collections.defaultdict(int))
        for date, layout, files in (
            db.session.query(
                func.min(DailyStat.date),
                DailyStat.layout,
                func.sum(DailyStat.files),
            )
            .filter(DailyStat.layout != "")
            .group_by(strftime(db.engine.name, DailyStat.date, "%Y"), DailyStat.layout)
            .order_by(DailyStat.date)
            .all()
        ):
            history[date.strftime(dateformat)][layout] = files
        dates = [
            date.strftime(dateformat)
            for date in _iter_years(
                datetime.datetime.strptime(min(history.keys()), dateformat).date(),
                datetime.date.today(),
            )
        ]
    elif period == "month":
        history = collections.defaultdict(lambda: collections.defaultdict(int))
        for date, layout, files in (
            db.session.query(
                func.min(DailyStat.date),
                DailyStat.layout,
                func.sum(DailyStat.files),
            )
            .filter(DailyStat.layout != "")
            .group_by(
                strftime(db.engine.name, DailyStat.date, "%Y-%m"), DailyStat.layout
            )
            .order_by(DailyStat.date)
            .all()
        ):
            history[date.strftime(dateformat)][layout] = files
        dates = [
            date.strftime(dateformat)
            for date in _iter_months(
                datetime.datetime.strptime(min(history.keys()), dateformat).date(),
                datetime.date.today(),
            )
        ]
    elif period == "day":
        history = collections.defaultdict(lambda: collections.defaultdict(int))
        for date, layout, files in (
            db.session.query(
                DailyStat.date,
                DailyStat.layout,
                DailyStat.files,
            )
            .filter(DailyStat.layout != "")
            .order_by(DailyStat.date)
            .all()
        ):
            history[date.strftime(dateformat)][layout] = files
        dates = [
            date.strftime(dateformat)
            for date in _iter_days(
                datetime.datetime.strptime(min(history.keys()), dateformat).date(),
                datetime.date.today(),
            )
        ]
    else:
        raise ValueError()

    return {
        "dates": dates,
        "layouts": {
            layout: [history[date][layout] for date in dates]
            for layout in set(
                itertools.chain.from_iterable(data.keys() for data in history.values())
            )
        },
    }
