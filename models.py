from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AgentDetails(Base):
    __tablename__ = 'agent_details'

    username = Column(String(), primary_key=True)
    password = Column(String())
    name = Column(String())


class Queue(Base):
    __tablename__ = 'queue'

    cust_name = Column(String(), primary_key=True)
    video_file_name = Column(String())
    image_name = Column(String())
    status = Column(String())
    added_date = Column(DateTime())
