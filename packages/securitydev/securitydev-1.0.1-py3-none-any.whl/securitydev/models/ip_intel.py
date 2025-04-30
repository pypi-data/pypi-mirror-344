"""Pydantic models for the IP Intel API endpoints."""

from typing import List, Optional

from pydantic import BaseModel, Field


class City(BaseModel):
    name: Optional[str] = None


class Continent(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None


class Country(BaseModel):
    iso_code: Optional[str] = None
    name: Optional[str] = None


class Location(BaseModel):
    accuracy_radius: Optional[int] = Field(default=None, ge=0)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    time_zone: Optional[str] = None


class Postal(BaseModel):
    code: Optional[str] = None


class Subdivision(BaseModel):
    iso_code: Optional[str] = None
    name: Optional[str] = None


class GeoIpLookupData(BaseModel):
    city: City = Field(default_factory=City)
    continent: Continent = Field(default_factory=Continent)
    country: Country = Field(default_factory=Country)
    location: Location = Field(default_factory=Location)
    postal: Postal = Field(default_factory=Postal)
    registered_country: Country = Field(default_factory=Country)
    subdivisions: Optional[List[Subdivision]] = None


class ReputationData(BaseModel):
    is_abuser: Optional[bool] = None
    is_proxy: Optional[bool] = None
    is_tor_exit: Optional[bool] = None
