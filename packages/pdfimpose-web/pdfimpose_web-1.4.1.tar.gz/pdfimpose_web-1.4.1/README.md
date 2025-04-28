# pdfimpose-web 📕 The code powering https://pdfimpose.it

## Installation

```sh
python3 -m pip install pdfimpose-web
```

## Run the application

Run the application using the following command.

```sh
python3 -m flask --app pdfimposeweb run
```

You can now use pdfimpose-web at: http://localhost:5000.

Note that you might want to configure the application using the settings described in the following section.

## Settings

This application can be run with default settings (but with default settings, data might be reset if you restart it).

To configure it:

- download file [`pdfimposeweb/settings/default.py`](https://framagit.org/spalax/pdfimpose-web/-/raw/main/pdfimposeweb/settings/default.py?inline=false) to your disk,
- change it (it is self-documented),
- tell `pdfimpose-web` to use it:

  ```sh
  export PDFIMPOSEWEB_SETTINGS=/path/to/settings.py
  python3 -m flask --app pdfimposeweb run
  ```

## Database migration

Some new versions of pdfimpose-web requires to upgrate the database. See [migration](migration/README.md) to get mor information about it.

## Resizing a PDF

This repository also includes the experimental script `pdfresize`, a command line script to resize a PDF file. It is installed together with `pdfimpose-web` (`python -m pip install pdfimpose-web`). Run `pdfresize --help` for more information.
