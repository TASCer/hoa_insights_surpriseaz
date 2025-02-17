from datetime import datetime
from sqlalchemy import String, INTEGER, DOUBLE_PRECISION, TIMESTAMP, ForeignKey
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


class last_update(Base):
    __tablename__ = "last_updated"

    TS: Mapped[datetime] = mapped_column(TIMESTAMP(6), index=True, primary_key=True)

# TESTING


# # TODO Can't determine the inherit condition between inherited table 'rentals' and inheriting table 'registered_rentals';
class RegisteredRentals(Base):
    __tablename__ = "registered_rentals"
    APN: Mapped[str] = mapped_column(String(11), primary_key=True)
    OWNER: Mapped[str] = mapped_column(String(120), index=True)
    OWNER_TYPE: Mapped[str] = mapped_column(String(40))
    LEGAL_CODE: Mapped[str] = mapped_column(String(3))
    CONTACT: Mapped[str] = mapped_column(String(120))
    CONTACT_ADX: Mapped[str] = mapped_column(String(120))
    CONTACT_PH: Mapped[str] = mapped_column(String(120))
    LAT: Mapped[float] = mapped_column(DOUBLE_PRECISION, primary_key=True)
    LONG: Mapped[float] = mapped_column(DOUBLE_PRECISION, primary_key=True)
    SITUS: Mapped[str] = mapped_column(String(100))
    

class ClassedRentals(Base):
    __tablename__ = "classed_rentals"
    OWNER: Mapped[str] = mapped_column(String(120), index=True)
    LEGAL_CODE: Mapped[str] = mapped_column(String(3))
    LAT: Mapped[float] = mapped_column(DOUBLE_PRECISION, primary_key=True)
    LONG: Mapped[float] = mapped_column(DOUBLE_PRECISION, primary_key=True)
    SITUS: Mapped[str] = mapped_column(String(100))
    APN: Mapped[str] = mapped_column(String(11), primary_key=True)
    COMMUNITY: Mapped[str] = mapped_column(String(100))



#     pass

# TODO SEEMS RO WORK BUT NEED TO SETUP REMOTE DB FOR TESTING
# class Community(Community):
#     __tablename__ = "communities"


# if __name__ == "__main__":
#     c = Community()
#     print(c, type(c))