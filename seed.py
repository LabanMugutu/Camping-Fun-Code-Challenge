from server import create_app, db
from server.models import Camper, Activity

app = create_app()
app.app_context().push()

# Create tables
db.create_all()

# Seed campers
c1 = Camper(name="Alice", age=10)
c2 = Camper(name="Bob", age=12)
c3 = Camper(name="Charlie", age=14)

# Seed activities
a1 = Activity(name="Archery", difficulty=2)
a2 = Activity(name="Swimming", difficulty=3)
a3 = Activity(name="Hiking", difficulty=1)

db.session.add_all([c1, c2, c3, a1, a2, a3])
db.session.commit()

print("Seeded campers and activities!")

