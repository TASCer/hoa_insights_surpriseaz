from datetime import datetime
# from sqlalchemy import ForeignKey
from sqlalchemy import String, INTEGER, DATE, Boolean, DOUBLE_PRECISION, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
# from hoa_insights_surpriseaz.database.local_models import 

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


#  WORKS
class last_update(Base):
    __tablename__ = "last_updated"

    _: Mapped[datetime] = mapped_column(TIMESTAMP(6), index=True, primary_key=True)

# TODO Can't determine the inherit condition between inherited table 'rentals' and inheriting table 'registered_rentals';
# class registered_rentals(Rentals):
#     __tablename__ = "registered_rentals"
    
#     pass

# TODO SEEMS RO WORK BUT NEED TO SETUP REMOTE DB FOR TESTING
# class Community(Community):
#     __tablename__ = "communities"


# if __name__ == "__main__":
#     c = Community()
#     print(c, type(c))