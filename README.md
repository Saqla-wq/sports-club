# Cricket Registration Project

A small Flask web app for registering players for sports events.

## Features

- Clean registration form UI
- Server-side validation
- Error messages shown on the form
- Registration data saved to `data/registrations.csv`
- Responsive design for desktop and mobile

## Run Locally

1. Create a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app:

```bash
python app.py
```

4. Open `http://127.0.0.1:8080`

## Environment Variables

- `PORT`: app port, default `8080`
- `FLASK_DEBUG`: `true` or `false`
- `SECRET_KEY`: set this to a secure value outside development

## Project Structure

- `app.py` - Flask application
- `templates/` - HTML templates
- `static/style.css` - styling
- `data/registrations.csv` - saved registrations
