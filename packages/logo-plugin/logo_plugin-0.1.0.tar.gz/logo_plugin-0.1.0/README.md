```markdown
# Logo Plugin

A Python plugin that, given a root domain, fetches its logo via API, stores it in MongoDB GridFS, and immediately retrieves it to a local file.

## Installation
```bash
pip install .
```

## Configuration

Set environment variables before use:

- `MONGO_URI`: MongoDB connection string (default: `mongodb://localhost:27017/`)
- `DB_NAME`: Database name (default: `company_logos`)
- `API_BASE_URL`: Base URL for the logo API (default: `https://img.logo.dev`)
- `LOGO_API_PATH_TOKEN`: Logo API path token
- `API_KEY`: Logo API bearer key

## Usage

### CLI
```bash
# Provide a root domain; plugin fetches, stores, and retrieves the logo automatically:
logo-fetch example.com
```

- On success you'll see a stored `file_id` and a local file `example.com_logo.png`.
```
