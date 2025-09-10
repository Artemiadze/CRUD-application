# CRUP application on Fast API

## How to use
1. Write to console:
```bash
uvicorn app.main:app --reload
```

2. Open the browser and go to:
```bash
http://127.0.0.1:8000/docs
```

3. For example, enter in request body in the field 'POST: Create User':
```json
{
  "full_name": "Иванов Иван Петрович",
  "phone_number": "+79995553322",
  "birth_date": "1984-01-01",
  "passport": "4321 987654"
}
```