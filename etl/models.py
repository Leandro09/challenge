from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, Boolean, TIMESTAMP, BIGINT, TEXT, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from sqlalchemy.orm import relationship


Base = declarative_base()

# Define the SQLAlchemy models to validate data types in the SQL tables
class LaunchModelOrm(Base):
    __tablename__ = 'launches'

    id = Column(String(50), primary_key=True)
    name = Column(String(255))
    date_utc = Column(TIMESTAMP)
    date_unix = Column(BIGINT)
    date_local = Column(TIMESTAMP)
    date_precision = Column(String(50))
    static_fire_date_utc = Column(TIMESTAMP)
    static_fire_date_unix = Column(BIGINT)
    net = Column(Boolean)
    window = Column(Integer)
    success = Column(Boolean)
    details = Column(TEXT)
    webcast = Column(String(255))
    youtube_id = Column(String(50))
    article = Column(String(255))
    wikipedia = Column(String(255))
    auto_update = Column(Boolean)
    tbd = Column(Boolean)
    rocket = Column(String(50))
    flight_number = Column(Integer)
    launchpad = Column(String(50))
    launch_library_id = Column(String(50))
    upcoming = Column(Boolean)
    
    # Establish a bidirectional relationship between FailureModelOrm, CoreModelOrm and LaunchModelOrm
    cores = relationship('CoreModelOrm', back_populates='launch')
    failures = relationship('FailureModelOrm', back_populates='launch')
    

# Define FailureModelOrm to store failures
class FailureModelOrm(Base):
    __tablename__ = 'failures'

    id = Column(Integer, primary_key=True)
    time = Column(Integer)
    altitude = Column(Integer)
    reason = Column(String)

    launch_id = Column(String(50), ForeignKey('launches.id'))
    launch = relationship('LaunchModelOrm', back_populates='failures')


# Define CoreModelOrm to store cores data
class CoreModelOrm(Base):
    __tablename__ = 'cores'

    id = Column(Integer, primary_key=True)
    core = Column(String(50))
    flight = Column(Integer)
    gridfins = Column(Boolean)
    legs = Column(Boolean)
    reused = Column(Boolean)
    landing_attempt = Column(Boolean)
    landing_success = Column(Boolean)
    landing_type = Column(String(50))
    landpad = Column(String(50))

    launch_id = Column(String(50), ForeignKey('launches.id'))
    launch = relationship('LaunchModelOrm', back_populates='cores')

# Define models to handle data to avoid issues with data types

class CoresModel(BaseModel):
    core: Optional[str]
    flight: Optional[int]
    gridfins: Optional[bool]
    legs: Optional[bool]
    reused: Optional[bool]
    landing_attempt: Optional[bool]
    landing_success: Optional[bool]
    landing_type: Optional[str]
    landpad: Optional[str]


class FailureModel(BaseModel):
    time: Optional[int] = Field(None, ge=0)
    altitude: Optional[int] = Field(None, ge=0) #avoid negative values
    reason: str
    
class LaunchModel(BaseModel):
    id: str
    name: str = Field(None, max_length=255)
    date_utc: str
    date_unix: int
    date_local: str
    date_precision: str = Field(None, max_length=50)
    static_fire_date_utc: Optional[str] = Field(None, max_length=50)
    static_fire_date_unix: Optional[int]
    net: bool
    window: Optional[int]
    success: Optional[bool]
    details: Optional[str] = Field(None)
    webcast: Optional[str] = Field(None, max_length=255)
    youtube_id: Optional[str] = Field(None, max_length=50)
    article: Optional[str] = Field(None, max_length=255)
    wikipedia: Optional[str] = Field(None, max_length=255)
    auto_update: bool
    tbd: bool
    launch_library_id: Optional[str] = Field(None, max_length=50)
    rocket: str
    launchpad: str
    flight_number: int
    failures: List[FailureModel] = []
    cores: List[CoresModel] = []
    upcoming: bool