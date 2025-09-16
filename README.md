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
  "first_name": "Abe",
  "last_name": "Who",
  "patronymic": "Bea",
  "phone_number": "89204001940",
  "birth_date": "1995-09-16",
  "passport_series": "3333",
  "passport_number": "077777"
}
```