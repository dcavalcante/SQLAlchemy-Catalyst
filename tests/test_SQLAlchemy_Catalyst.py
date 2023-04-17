import pytest
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from SQLAlchemy_Catalyst.SQLAlchemy_Catalyst import Catalyst

# define a database engine
engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)

# define a test model as a fixture
@pytest.fixture(scope="module")
def TestModel():
  class TestModel(Catalyst):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(Integer)

  # create the table
  TestModel.metadata.create_all(engine)
  
  return TestModel

# define a test function that uses the TestModel fixture
def test_add_if_new(TestModel):
  # test add_if_new
  session = Session()
  values = {"name": "Test", "value": 10}
  values_2 = {"name": "Test", "value": 20}

  # add a new record with name "Test"
  test_record = TestModel.add_if_new(session, ["name"], values)
  assert test_record.id == 1
  assert test_record.name == "Test"
  assert test_record.value == 10

  # try adding another record with the same name "Test"
  # and retrieves the existing record instead
  existing_record = TestModel.add_if_new(session, ["name"], values_2)
  assert existing_record.id == 1
  assert existing_record.name == "Test"
  assert existing_record.value == 10

def test_add_or_update(TestModel):
  session = Session()

  # add a new record
  values = {"name": "Test", "value": 10}
  TestModel.add_or_update(session, {"name": "Test"}, values)

  # update the existing record with new values
  new_values = {"name": "Test", "value": 20}
  existing_record = TestModel.add_or_update(session, {"name": "Test"}, new_values)

  # check if the record has been updated
  assert existing_record.id == 1
  assert existing_record.name == "Test"
  assert existing_record.value == 20

  # add a new record with a different name
  values_2 = {"name": "Test 2", "value": 30}
  TestModel.add_or_update(session, {"name": "Test 2"}, values_2)

  # check if the new record has been added
  new_record = session.query(TestModel).filter_by(name="Test 2").first()
  assert new_record.id == 2
  assert new_record.name == "Test 2"
  assert new_record.value == 30

def test_update_if_empty(TestModel):
  session = Session()
  values = {"name": "Empty Test", "value": None}

  # Add a new record with a null value for the "value" column
  test_record = TestModel.add_if_new(session, ["name"], values)
  assert test_record.name == "Empty Test"
  assert test_record.value is None

  # Update the existing record with a non-null value for the "value" column
  values_2 = {"name": "Empty Test", "value": 20}
  updated_record = TestModel.update_if_empty(session, {"name": "Empty Test"}, values_2)
  assert updated_record.name == "Empty Test"
  assert updated_record.value == 20

def test_merge_records_attributes(TestModel):
  session = Session()

  # add a record to merge into
  values = {"name": "Test", "value": 10}
  existing_record = TestModel.add_if_new(session, ["name"], values)

  # merge in new attributes
  new_values = {"value": 20}
  merged_record = TestModel.merge_records_attributes(session, {"name": "Test"}, new_values)

  # check if the attributes have been merged
  assert merged_record.id == 1
  assert merged_record.name == "Test"
  assert merged_record.value == 20

  # add a new record to merge into
  values_2 = {"name": "Test 2", "value": 30}
  existing_record_2 = TestModel.add_if_new(session, ["name"], values_2)

  # merge in new attributes with a different filter
  new_values_2 = {"value": 40}
  merged_record_2 = TestModel.merge_records_attributes(session, {"name": "Test 2"}, new_values_2)

  # check if the new attributes have been merged
  assert merged_record_2.id == 2
  assert merged_record_2.name == "Test 2"
  assert merged_record_2.value == 40

def test_increment_column(TestModel):
  session = Session()

  # create a new record with value 5
  values = {"name": "Increment Test", "value": 10}
  TestModel.add_if_new(session, ["name"], values)

  # increment the value of the "value" column
  TestModel.increment_column(session, {"name": "Increment Test"}, "value", 5)

  # check if the value has been incremented
  test_record = session.query(TestModel).filter_by(name="Increment Test").first()
  assert test_record.name == "Increment Test"
  assert test_record.value == 15


def test_decrement_column(TestModel):
  session = Session()

  # create a new record with value 5
  values = {"name": "Decrement Test", "value": 10}
  TestModel.add_if_new(session, ["name"], values)

  # decrement the value of the "value" column
  TestModel.decrement_column(session, {"name": "Decrement Test"}, "value", 5)

  # check if the value has been decremented
  test_record = session.query(TestModel).filter_by(name="Decrement Test").first()
  assert test_record.name == "Decrement Test"
  assert test_record.value == 5