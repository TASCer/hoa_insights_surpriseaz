# from datetime import datetime
# from sqlalchemy import ForeignKey
# from sqlalchemy import String, INTEGER, DATE, Boolean, DOUBLE_PRECISION, TIMESTAMP
# from sqlalchemy.orm import DeclarativeBase
# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column
# from hoa_insights_surpriseaz.database.local_models import Rentals, Community

# class Base(DeclarativeBase):
#     pass

# class last_update(Base):
#     __tablename__ = "last_updated"

#     _: Mapped[datetime] = mapped_column(TIMESTAMP(6), index=True)


# class registered_rentals(Rentals):
#     __tablename__ = "registered_rentals"
    
#     pass

# TODO SEEMS RO WORK BUT NEED TO SETUP REMOTE DB FOR TESTING
# class communities(Community):
#     __tablename__ = "communities"
    