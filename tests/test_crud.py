from src import crud, schema

def test_create_item(db_session):
    user_in = schema.UsersCreate(full_name="Alice", phone_number="89306152516", birth_date="1990-01-01", passport="1111 111111")
    user = crud.create_user(db_session, user_in)

    assert user.full_name == "Alice"
    assert user.phone_number == "89306152516"
    assert user.birth_date.isoformat() == "1990-01-01"
    assert user.passport == "1111 111111"

def test_get_user(db_session):
    user_in = schema.UsersCreate(full_name="Bob", phone_number="+79201156515", birth_date="1985-05-05", passport="2222 222222")
    create = crud.create_user(db_session, user_in)
    fetched = crud.get_user(db_session, create.id)

    assert fetched.id == create.id

def test_get_user_by_name(db_session):
    user_in = schema.UsersCreate(full_name="Andrew", phone_number="+79201894515", birth_date="2005-09-05", passport="3333 333333")
    create = crud.create_user(db_session, user_in)
    fetched = crud.get_user_by_name(db_session, create.full_name)

    assert fetched.full_name == create.full_name

def test_update_user(db_session):
    user_in = schema.UsersCreate(full_name="Charlie", phone_number="+79201234567", birth_date="1970-12-12", passport="4444 444444")
    create = crud.create_user(db_session, user_in)

    user_update = schema.UsersUpdate(phone_number="+79207654321")
    updated = crud.update_user(db_session, create.id, user_update)

    assert updated.phone_number == "+79207654321"
    assert updated.full_name == "Charlie"  # unchanged

def test_delete_user(db_session):
    user_in = schema.UsersCreate(full_name="Diana", phone_number="89306152516", birth_date="1995-03-03", passport="5555 555555")
    create = crud.create_user(db_session, user_in)

    result = crud.delete_user(db_session, create.id)
    assert result is True

    deleted = crud.get_user(db_session, create.id)
    assert deleted is None