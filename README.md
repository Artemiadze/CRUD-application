# CRUP application on Fast API

## How to use
1. Create the virtual environment:

```bash
python -m venv <title_venv>
```

2. Launch the virtual environment:

Windows:
```bash
. .\<title_venv>\Scripts\Activate.ps1
```

Linux\MacOS:
```bash
source <venv>/bin/activate
```

3. Install the requirement:
```bash
pip install -r requirements.txt
```

4. Write to console:
```bash
uvicorn src.main:app --reload
```

5. Open the browser and go to:
```bash
http://127.0.0.1:8000/docs
```

6. For example, enter in request body in the field 'POST: Create User':
```json
{
  "first_name": "string",
  "last_name": "string",
  "patronymic": "string",
  "phone_number": "string"
}
```

- and in 'POST: create Passport':
```json
{
  "birth_date": "2025-09-18",
  "passport_series": "string",
  "passport_number": "string",
  "receipt_date": "2025-09-18",
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```

7. Command GET User give all information about Users, including passport's data
