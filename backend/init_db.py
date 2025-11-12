from models.database import Base, engine
from models.tables import Country, Indicator, DataPoint

Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
