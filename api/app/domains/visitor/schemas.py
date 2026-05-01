from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class VisitorCreate(BaseModel):
    browser_name: str | None = Field(default=None, max_length=50)
    browser_version: str | None = Field(default=None, max_length=30)
    engine_name: str | None = Field(default=None, max_length=50)
    os_name: str | None = Field(default=None, max_length=50)
    os_version: str | None = Field(default=None, max_length=30)
    device_type: str | None = Field(default=None, max_length=20)
    device_vendor: str | None = Field(default=None, max_length=50)
    device_model: str | None = Field(default=None, max_length=50)
    is_mobile: bool | None = None
    is_bot: bool = False

    screen_width: int | None = Field(default=None, ge=0)
    screen_height: int | None = Field(default=None, ge=0)
    pixel_ratio: float | None = Field(default=None, ge=0)
    color_depth: int | None = Field(default=None, ge=0)
    cpu_cores: int | None = Field(default=None, ge=0)
    device_memory: int | None = Field(default=None, ge=0)
    touch_support: bool | None = None

    primary_language: str | None = Field(default=None, max_length=20)
    languages: list[str] | None = None
    timezone: str | None = Field(default=None, max_length=64)

    consent_given: bool = False
    consent_at: datetime | None = None
    consent_version: str | None = Field(default=None, max_length=20)


class SessionCreate(BaseModel):
    ip_address: str | None = Field(default=None, max_length=45)
    isp: str | None = Field(default=None, max_length=255)
    asn: int | None = None
    is_vpn: bool = False
    is_proxy: bool = False
    is_datacenter: bool = False

    country_code: str | None = Field(default=None, min_length=2, max_length=2)
    country_name: str | None = Field(default=None, max_length=100)
    region: str | None = Field(default=None, max_length=100)
    city: str | None = Field(default=None, max_length=100)
    postal_code: str | None = Field(default=None, max_length=20)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    geo_accuracy: str | None = Field(default=None, max_length=20)

    viewport_width: int | None = Field(default=None, ge=0)
    viewport_height: int | None = Field(default=None, ge=0)
    connection_type: str | None = Field(default=None, max_length=20)
    connection_downlink: float | None = Field(default=None, ge=0)

    referer: str | None = None
    referer_domain: str | None = Field(default=None, max_length=255)
    landing_page: str | None = None
    exit_page: str | None = None
    utm_source: str | None = Field(default=None, max_length=100)
    utm_medium: str | None = Field(default=None, max_length=100)
    utm_campaign: str | None = Field(default=None, max_length=100)
    utm_term: str | None = Field(default=None, max_length=100)
    utm_content: str | None = Field(default=None, max_length=100)
    gclid: str | None = Field(default=None, max_length=255)
    fbclid: str | None = Field(default=None, max_length=255)


class VisitorTrackRequest(BaseModel):
    visitor: VisitorCreate
    session: SessionCreate = Field(default_factory=SessionCreate)


class VisitorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    visitor_uid: str
    total_sessions: int
    first_seen_at: datetime
    last_seen_at: datetime
    created_at: datetime


class SessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_uid: str
    visitor_id: int
    started_at: datetime
    created_at: datetime


class VisitorTrackResponse(BaseModel):
    visitor: VisitorRead
    session: SessionRead
