# CRUP application on Fast API

## How to use
1. Start the virtual environment:

Windows:
```bash
. .\<venv>\Scripts\Activate.ps1
```

Linux\MacOS:
```bash
source <venv>/bin/activate
```

2. Install the requirement:
```bash
pip install -r requirements.txt
```

3. Write to console:
```bash
uvicorn app.main:app --reload
```

4. Open the browser and go to:
```bash
http://127.0.0.1:8000/docs
```

5. For example, enter in request body in the field 'POST: Create User':
```json
{
  "full_name": "Иванов Иван Петрович",
  "phone_number": "+79995553322",
  "birth_date": "1984-01-01",
  "passport": "4321 987654"
}
```