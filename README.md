# SQLAlchemy-Catalyst
SQLAlchemy-Catalyst is a collection of helper methods for base SQLAlchemy classes.

## Installation
You can install the package using pip:
```
pip install SQLAlchemy-Catalyst
```

## Usage
### Importing
`database.py`:
```
from SQLAlchemy_Catalyst import Catalyst
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///example.db')
Session = sessionmaker(bind=engine)

class ExampleModel(Catalyst):
  __tablename__ = 'example_table'

  id = Column(Integer, primary_key=True)
  name = Column(String(50))
  age = Column(Integer)

```  
### Implementing
`implementation.py`:
```
from database import ExampleModel, Session
example = ExampleModel(name='John', age=30)
session = Session()
session.add(example)
session.commit()

# Call the methods on the example instance
example.add_if_new(session, ['name'], {'name': 'Mary'})
example.add_or_update(session, {'name': 'Mary'}, {'age': 40})
example.update_if_empty(session, {'name': 'Mary'}, {'age': 40})
example.merge_records_attributes(session, {'name': 'Mary'}, {'age': 40})
example.bulk_upsert(session, {'name': 'Mary'}, {'age': 40})
example.increment_column(session, {'name': 'Mary'}, 'age', 10)
example.decrement_column(session, {'name': 'Mary'}, 'age', 5)

```

## Methods available
### add_if_new(session, column_names, values)
Adds a new record to the database if no record exists with the provided values.

* `session`: An active database session object.
* `column_names`: A list of column names that need to be checked.
* `values`: A dictionary of column names and values to be added.

### add_or_update(session, filters, values)
Adds a new record to the database or updates an existing record.

* `session`: An active database session object.
* `filters`: A dictionary of column names and values to be checked for an existing record.
* `values`: A dictionary of column names and values to be added/updated.

### update_if_empty(session, filters, values)
Updates an existing record in the database if the specified columns are empty.

* `session`: An active database session object.
* `filters`: A dictionary of column names and values to be checked for an existing record.
* `values`: A dictionary of column names and values to be updated.

### merge_records_attributes(session, filters, values)
Merges the attributes of two records into one.

* `session`: An active database session object.
* `filters`: A dictionary of column names and values to be checked for an existing record.
* `values`: A dictionary of column names and values to be merged.

### bulk_upsert(session, filters, values)
Updates existing records in the database or inserts new records.

* `session`: An active database session object.
* `filters`: A dictionary of column names and values to be checked for existing records.
* `values`: A dictionary of column names and values to be updated/added.

### increment_column(session, filters, column_name, value)
Increments a numeric column in an existing record.

* `session`: An active database session object.
* `filters`: A dictionary of column names and values to be checked for an existing record.
* `column_name`: The name of the numeric column to be incremented.
* `value`: The value to increment the column by (default is 1).

### decrement_column(session, filters, column_name, value)
Decrements a numeric column in an existing record.

* `session`: An active database session object.
* `filters`: A dictionary of column names and values to be checked for an existing record.
* `column_name`: The name of the numeric column to be decremented.
* `value`: The value to decrement the column by (default is 1).


## License
This project is licensed under the **MIT License** - see the [LICENSE](https://mit-license.org/) file for details.