# FreelanceHub Backend

## Setup

1. Create a python virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # windows: .venv\Scripts\activate
```

````

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create `.env` from `.env.example` and set `JWT_SECRET_KEY` and `MONGO_URI`.

4. Start MongoDB (local or Atlas) and ensure `MONGO_URI` is reachable.

5. Run the app

```bash
python app.py
```

Default server: `http://localhost:5000`

## Notes

- Upload files are stored in `storage/` by default.
- Admin endpoints require a JWT token whose `role` claim is `admin`.
- This is a starter backend designed to satisfy the project MVP and to be extended during sprints.

````
