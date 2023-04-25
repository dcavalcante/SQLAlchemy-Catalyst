from sqlalchemy import select, update, insert
from sqlalchemy.orm import Session
from sqlalchemy import Integer, Float, Numeric

class Catalyst:
  __abstract__ = True

  @classmethod
  def add_if_new(cls, session, column_names, values):
    filters = {}
    for column_name in column_names:
      filters[column_name] = values[column_name]

    existing_record = session.execute(select(cls).filter_by(**filters)).scalar_one_or_none()

    if not existing_record:
      item = cls(**values)
      session.add(item)
      session.commit()
      return item
    else:
      return existing_record

  @classmethod
  def add_or_update(cls, session, filters, values):
    existing_record = session.execute(select(cls).filter_by(**filters)).scalar_one_or_none()

    if existing_record:
      for key, value in values.items():
        setattr(existing_record, key, value)
      session.commit()
      return existing_record
    else:
      item = cls(**values)
      session.add(item)
      session.commit()
      return item

  @classmethod
  def update_if_empty(cls, session, filters, values):
    existing_record = session.execute(select(cls).filter_by(**filters)).scalar_one_or_none()

    if existing_record:
      for key, value in values.items():
        if getattr(existing_record, key) is None:
          setattr(existing_record, key, value)
      session.commit()
      return existing_record

    return None

  @classmethod
  def merge_records_attributes(cls, session, filters, values):
    # Merges the attributes of two records into one.
    existing_record = session.execute(select(cls).filter_by(**filters)).scalar_one_or_none()

    if existing_record:
      for key, value in values.items():
        setattr(existing_record, key, value)
      session.commit()
      return existing_record

    item = cls(**values)
    session.add(item)
    session.commit()
    return item

  @classmethod 
  def increment_column(cls, session, filters, column_name, value=1):
    column_type = getattr(cls, column_name).type
    if not isinstance(column_type, (Integer, Float, Numeric)):
      raise ValueError("Column must be a numeric type")

    existing_record = session.execute(select(cls).filter_by(**filters)).scalar_one_or_none()

    if existing_record:
      current_value = getattr(existing_record, column_name)
      setattr(existing_record, column_name, current_value + value)
      session.commit()
      return existing_record

    return None

  @classmethod
  def decrement_column(cls, session, filters, column_name, value=1):
    column_type = getattr(cls, column_name).type
    if not isinstance(column_type, (Integer, Float, Numeric)):
      raise ValueError("Column must be a numeric type")

    existing_record = session.execute(select(cls).filter_by(**filters)).scalar_one_or_none()

    if existing_record:
      current_value = getattr(existing_record, column_name)
      setattr(existing_record, column_name, current_value - value)
      session.commit()
      return existing_record

    return None
