from database import Base, engine
from models import *

print("🔄 Creating all tables...")
Base.metadata.create_all(bind=engine)
print("✅ Done.")