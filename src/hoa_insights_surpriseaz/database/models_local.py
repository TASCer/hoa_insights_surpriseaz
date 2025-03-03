from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy import String, INTEGER, DATE, Boolean, DOUBLE_PRECISION, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Community(Base):
    __tablename__ = "communities"
    COMMUNITY: Mapped[str] = mapped_column(String(100), primary_key=True, index=True)
    COUNT: Mapped[int] = mapped_column(INTEGER)
    LAT: Mapped[float] = mapped_column(DOUBLE_PRECISION, primary_key=True)
    LONG: Mapped[float] = mapped_column(DOUBLE_PRECISION, primary_key=True)
    MANAGED_ID: Mapped[int] = mapped_column(INTEGER)


class CommunityManagement(Base):
    __tablename__ = "community_managers"
    ID: Mapped[int] = mapped_column(
        INTEGER, autoincrement=True, primary_key=True, index=True
    )
    COMMUNITY: Mapped[str] = mapped_column(String(100), index=True)
    BOARD_SITUS: Mapped[str] = mapped_column(String(60), nullable=True)
    BOARD_CITY: Mapped[str] = mapped_column(String(60), nullable=True)
    MANAGER: Mapped[str] = mapped_column(String(100), nullable=True)
    CONTACT_ADX: Mapped[str] = mapped_column(String(120), nullable=True)
    CONTACT_PH: Mapped[str] = mapped_column(String(120), nullable=True)


class Parcel(Base):
    __tablename__ = "parcels"
    APN: Mapped[str] = mapped_column(String(11), primary_key=True)
    COMMUNITY: Mapped[str] = mapped_column(String(100))
    SITUS: Mapped[str] = mapped_column(String(100))
    LAT: Mapped[float] = mapped_column(DOUBLE_PRECISION, primary_key=True)
    LONG: Mapped[float] = mapped_column(DOUBLE_PRECISION, primary_key=True)


class Owner(Base):
    __tablename__ = "owners"
    APN: Mapped[str] = mapped_column(ForeignKey("parcels.APN"), primary_key=True)
    OWNER: Mapped[str] = mapped_column(String(120))
    MAIL_ADX: Mapped[str] = mapped_column(String(120))
    SALE_DATE: Mapped[datetime] = mapped_column(DATE)
    SALE_PRICE: Mapped[int] = mapped_column(INTEGER)
    DEED_DATE: Mapped[datetime] = mapped_column(DATE)
    DEED_TYPE: Mapped[str] = mapped_column(String(3))
    LEGAL_CODE: Mapped[str] = mapped_column(String(3))
    RENTAL: Mapped[bool] = mapped_column(Boolean, index=True)

    def __repr__(self) -> str:
        return f"APN={self.APN!r}, OWNER={self.owner!r}, MAIL_ADX={self.mail_adx!r})"


class Rentals(Base):
    __tablename__ = "rentals"
    APN: Mapped[str] = mapped_column(
        ForeignKey("owners.APN"), primary_key=True, nullable=False
    )
    OWNER: Mapped[str] = mapped_column(String(120), index=True)
    OWNER_TYPE: Mapped[str] = mapped_column(String(40))
    CONTACT: Mapped[str] = mapped_column(String(120))
    CONTACT_ADX: Mapped[str] = mapped_column(String(120))
    CONTACT_PH: Mapped[str] = mapped_column(String(120))


class HistoricalSales(Base):
    __tablename__ = "historical_sales"
    APN: Mapped[str] = mapped_column(
        ForeignKey("owners.APN"), primary_key=True, nullable=False
    )
    SALE_DATE: Mapped[datetime] = mapped_column(
        DATE, primary_key=True, default="1901-01-01", index=True
    )
    SALE_PRICE: Mapped[int] = mapped_column(INTEGER)
    TS: Mapped[datetime] = mapped_column(TIMESTAMP(6), index=True)


class HistoricalOwmers(Base):
    __tablename__ = "historical_owners"
    APN: Mapped[str] = mapped_column(
        ForeignKey("owners.APN"), primary_key=True, nullable=False
    )
    OWNER: Mapped[str] = mapped_column(String(255), primary_key=True)
    DEED_DATE: Mapped[datetime] = mapped_column(DATE, index=True)
    DEED_TYPE: Mapped[str] = mapped_column(String(20))
    TS: Mapped[datetime] = mapped_column(TIMESTAMP(6), index=True)


class HistoricalManagers(Base):
    __tablename__ = "historical_managers"
    ID: Mapped[int] = mapped_column(
        INTEGER, autoincrement=True, primary_key=True, index=True
    )
    COMMUNITY: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    BOARD_SITUS: Mapped[str] = mapped_column(String(60), nullable=True)
    BOARD_CITY: Mapped[str] = mapped_column(String(60), nullable=True)
    MANAGER: Mapped[str] = mapped_column(String(100), nullable=True)
    CONTACT_ADX: Mapped[str] = mapped_column(String(120), nullable=True)
    CONTACT_PH: Mapped[str] = mapped_column(String(120), nullable=True)
    TS: Mapped[datetime] = mapped_column(TIMESTAMP(6), index=True)
