Migrate database of pdfimpose-web
=================================

You are reading this because you upgraded [pdfimpose-web](https://framagit.org/spalax/pdfimpose-web), and you were notified to migrate the database.

## Tutorial

1. Install `alembic`:

   ~~~sh
   python -m pip install alembic
   ~~~

2. Open the `alembic.ini` file in this directory, and set `sqlalchemy.url` to your database URL (note: it is the very same URL that is used in the `settings.py` file of `pdfimpose-web`.

3. Run `alembic`:

   ~~~sh
   alembic upgrade head
   ~~~

4. If you are migrating from pdfimpose-web version 1.3.0 (or earlier) to version 1.4.0 (or later), you have to manually set that column `layout` of table `daily_stat` is a primary key. To do so, run the following SQL query:

   ~~~SQL
   ALTER TABLE daily_stat
       DROP PRIMARY KEY,
       ADD PRIMARY KEY (date, layout);
   ~~~

That's all, folks!
