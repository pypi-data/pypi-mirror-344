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

"""Web interface to pdfimpose https://framagit.org/spalax/pdfimpose"""

import atexit
import collections
import contextlib
import datetime
import functools
import io
import operator
import os
import pathlib
import secrets
import shutil
import time
import typing

import papersize
import pdfimpose
import unidecode
from flask import (
    Flask,
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_babel import Babel
from flask_babel import lazy_gettext as _
from flask_basicauth import BasicAuth
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename

from . import database, layout, limiter, settings

VERSION = "1.4.1"


def allowed_file(filename: str):
    """Return `True` if the filename is allowed."""
    return filename.endswith(".pdf")


def papersizetranslations():
    """Return the location of translation of package `papersize`."""
    # Thanks to:
    # https://importlib-resources.readthedocs.io/en/latest/migration.html#pkg-resources-resource-filename
    file_manager = contextlib.ExitStack()
    atexit.register(file_manager.close)
    return file_manager.enter_context(papersize.translation_directory())


@functools.cache
def get_languages(babel: Babel) -> collections.OrderedDict[str, str]:
    """Return an ordered dictionary of available languages, sorted by language code.

    - Keys are the language codes (e.g. "en" for English).
    - Values are the display names (e.g. "English").
    """
    return collections.OrderedDict(
        (locale.language, locale.language_name)
        for locale in sorted(
            set(babel.list_translations()), key=operator.attrgetter("language")
        )
    )


# pylint: disable=too-many-statements
def create_app():
    """Create and configure the application"""

    app = Flask(__name__, instance_relative_config=True)
    app.jinja_env.add_extension("jinja2.ext.loopcontrols")

    # Load options
    settings.set_configuration(app)

    app.config["SESSION_COOKIE_SAMESITE"] = "Strict"

    # Configure Babel
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = (
        f"translations;{papersizetranslations()}"
    )
    app.config["BABEL_DOMAIN"] = "messages;papersize"

    def get_locale():
        """Return the chosen locale.

        - If a locale has been passed as argument '?language=en', and a translation is available:
          use it, and store the choice in cookies.
        - Otherwise, is a valid language has been stored in cookies, use it.
        - Otherwise, guess it.
        """
        # Has locale been passed as an argument '?language=en'?
        if "language" in request.args:
            if request.args["language"] in get_languages(babel):
                return request.args["language"]

        # Has locale been stored in cookies?
        if request.cookies.get("language") in get_languages(babel):
            return request.cookies.get("language")

        # Guess locale
        return request.accept_languages.best_match(
            locale.language for locale in babel.list_translations()
        )

    babel = Babel(app, locale_selector=get_locale)

    # Configure database
    database.init(app)

    # Configure limiter
    limiter.init(app)

    # Add stuff to template context

    @app.context_processor
    def context_processor():
        return {
            "UNITS": {
                key: _(value).split("(")[0].strip()
                for key, value in papersize.UNITS_HELP.items()
                if key in ("pt", "mm", "cm", "in")
            },
            "SIZES": {key: _(value) for key, value in papersize.SIZES_HELP.items()},
            "LAYOUTS": (
                # Layouts are sorted from a beginner point-of-view:
                # the simplest, most usual, to the weirdest.
                "saddle",
                "cards",
                "pdfautonup",
                "hardcover",
                "onepagezine",
                "wire",
                "copycutfold",
                "cutstackfold",
            ),
            "languages": get_languages(app.extensions["babel"].instance),
            "lang": app.extensions["babel"].locale_selector(),
            "stat": database.stat(),
            "max_size": database.prettyprint_size(
                app.config["MAX_CONTENT_LENGTH"], round_func=round
            ),
        }

    # Quick and dirty statistics page
    basic_auth = BasicAuth(app)

    # Redirect while keeping query string
    def smart_redirect(location, *args, **kwargs):
        if request.query_string:
            return redirect(
                f"{location}?{request.query_string.decode()}", *args, **kwargs
            )
        return redirect(location, *args, **kwargs)

    # Define routes

    @app.route("/stats")
    @basic_auth.required
    def stats():
        return render_template(
            "stats.html",
            datadayall=database.get_history_all("day", dateformat='"%Y-%m-%d"'),
            datamonthall=database.get_history_all("month", dateformat='"%Y-%m"'),
            datayearall=database.get_history_all("year", dateformat='"%Y"'),
            datadaylayouts=database.get_history_layouts("day", dateformat='"%Y-%m-%d"'),
            datamonthlayouts=database.get_history_layouts(
                "month", dateformat='"%Y-%m"'
            ),
            datayearlayouts=database.get_history_layouts("year", dateformat='"%Y"'),
        )

    @app.route("/", methods=["GET", "POST"])
    def root():
        if request.method == "POST":
            # Catch argument errors
            try:
                if (
                    app.config["MAX_FILE_REPEAT"]
                    != 0  # MAX_FILE_REPEAT == 0 means no limit
                    and int(
                        request.form.to_dict()[
                            f"""form-{request.form["layout"]}-repeat-value"""
                        ]
                    )
                    > app.config["MAX_FILE_REPEAT"]
                ):
                    flash(
                        _("Error: The maximum number of repetitions is %s.")
                        % app.config["MAX_FILE_REPEAT"],
                        category="impose",
                    )
                    return smart_redirect("/")
            except (KeyError, ValueError):
                pass

            # Remove bad files, save good files
            sourcefiles = []
            totalsize = 0
            destname = None
            for file in request.files.getlist("file"):
                if not file.filename:
                    flash(_("Error: No file."), "files")
                    continue
                if not allowed_file(file.filename):
                    flash(_("Error: Invalid filename."), "files")
                    continue
                if destname is None:
                    destname = unidecode.unidecode(
                        f"{pathlib.Path(file.filename).stem}-impose.pdf"
                    )
                # pylint: disable=protected-access
                sourcefiles.append(file.stream._file)
                totalsize += sourcefiles[-1].getbuffer().nbytes

            # No source files…
            if not sourcefiles:
                flash(
                    _("No valid PDF files found. Try uploading a valid PDF file."),
                    "files",
                )
                return smart_redirect("/")

            # Impose file
            try:
                destfile = io.BytesIO()
                layout.impose(
                    request.form["layout"],
                    infile=sourcefiles[0],  # Right now, we only handle one single file.
                    outfile=destfile,
                    arguments=request.form.to_dict(),
                )
            except pdfimpose.UserError as error:
                flash(  #  pylint: disable=consider-using-f-string
                    _("Error while imposing files: %s") % error,
                    category="impose",
                )
                return smart_redirect("/")

            # Imposition succeeded. Log it in the database
            database.add(totalsize, layout=request.form["layout"])

            # Everything went right!
            return destfile.getvalue(), {
                "Content-type": "application/pdf",
                "Content-Disposition": f'attachment; filename="{destname}"',
            }

        # Method GET (or anything but POST)
        if "noscript" in request.args:
            template = "noscript.html"
        else:
            template = "index.html"
        response = make_response(render_template(template))

        if request.args.get("language", default=None) in get_languages(babel):
            # Store preferred language in cookies
            response.set_cookie("language", request.args["language"])

        return response

    @app.errorhandler(413)
    def error413(error):
        #  pylint: disable=unused-argument
        flash(
            _(
                "Error: File is too big: maximum size is %s.",
            )
            % database.prettyprint_size(
                app.config["MAX_CONTENT_LENGTH"], round_func=round
            ),
            "files",
        )
        return render_template("index.html"), 413

    return app
