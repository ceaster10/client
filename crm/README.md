# Basic CRM App

This directory contains a minimal CRM application built with Flask and SQLite.

## Setup

Install the dependencies (including Flask):

```bash
pip install -r requirements.txt
```

## Running

Start the server with:

```bash
python crm/app.py
```

The application exposes the following endpoints:

- `GET /customers` – list all customers
- `POST /customers` – create a customer (`name`, `email`, `phone` JSON fields)
- `GET /customers/<id>` – retrieve a specific customer
- `PUT /customers/<id>` – update a customer
- `DELETE /customers/<id>` – delete a customer

The SQLite database file (`crm.db`) will be created automatically in this directory.
