from nextpy.psx import psx, component, register_component


@component
def DatabaseGuide(props):
    return psx("""
        <section id="database" class="space-y-6">
            <div class="pb-3 border-b border-gray-800">
                <h2 class="text-2xl font-bold text-gray-100">Database Integration</h2>
                <p class="mt-2 text-gray-400">
                    Connect your NextPy applications to databases with built-in support for popular ORMs and raw SQL.
                </p>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-green-400">Database Support</h3>
                <p class="mt-2 text-sm text-green-300">
                    NextPy works seamlessly with SQLAlchemy, PostgreSQL, MySQL, SQLite, and other databases. Use the built-in db module for quick setup or integrate your preferred ORM.
                </p>
            </div>

            <div class="grid gap-6 lg:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Built-in Database</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">from nextpy.db import Database

# Initialize database
db = Database("sqlite:///app.db")

# Define models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)

# Create tables
db.create_all()

# Query data
users = db.session.query(User).all()
user = db.session.query(User).filter_by(id=1).first()</pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">SQLAlchemy Integration</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup
engine = create_engine("postgresql://user:pass@localhost/db")
Session = sessionmaker(bind=engine)
session = Session()

# Query
users = session.query(User).filter(User.active == True).all()

# Create
new_user = User(name="John", email="john@example.com")
session.add(new_user)
session.commit()</pre>
                </div>
            </div>

            <div class="grid gap-6 lg:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Database in API Routes</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400"># pages/api/users.py

from nextpy.db import Database

db = Database("sqlite:///app.db")

async def get(request, params):
    users = db.session.query(User).all()
    return {
        "users": [{"id": u.id, "name": u.name} for u in users]
    }

async def post(request, params):
    data = await request.json()
    user = User(name=data["name"], email=data["email"])
    db.session.add(user)
    db.session.commit()
    return {"user": {"id": user.id}}</pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Environment Configuration</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">import os
from nextpy.db import Database

# Use environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///app.db"
)

db = Database(DATABASE_URL)

# Production setup
if os.getenv("ENV") == "production":
    db = Database(
        "postgresql://user:pass@host/db",
        pool_size=10,
        max_overflow=20
    )</pre>
                </div>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-gray-100">Database Best Practices</h3>
                <ul class="pl-5 mt-3 space-y-2 text-sm text-gray-400 list-disc">
                    <li>Use environment variables for database credentials</li>
                    <li>Implement connection pooling for production</li>
                    <li>Use transactions for data consistency</li>
                    <li>Add indexes for frequently queried columns</li>
                    <li>Implement proper error handling for database operations</li>
                    <li>Use migrations for schema changes (Alembic)</li>
                    <li>Consider read replicas for high-traffic applications</li>
                </ul>
            </div>
        </section>
    """)
