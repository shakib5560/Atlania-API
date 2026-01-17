from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.blog import User, Category, Post
from app.core.settings import settings

def seed():
    db = SessionLocal()
    
    # Check if categories already exist
    if db.query(Category).first():
        print("Database already seeded.")
        db.close()
        return

    # 1. Create Categories
    categories_data = [
        {"name": "Technologies", "slug": "technologies"},
        {"name": "Digital marketing", "slug": "digital-marketing"},
        {"name": "Business", "slug": "business"},
        {"name": "Blockchain", "slug": "blockchain"},
        {"name": "Android Dev", "slug": "android-dev"},
        {"name": "Gadget", "slug": "gadget"}
    ]
    
    db_categories = []
    for cat in categories_data:
        db_cat = Category(**cat)
        db.add(db_cat)
        db_categories.append(db_cat)
    
    db.commit()
    print(f"Added {len(db_categories)} categories.")

    # 2. Create a default Admin user
    admin_user = User(
        email="admin@atlania.studio",
        hashed_password="hashed_password_placeholder", # In a real app, use pwd_context.hash()
        full_name="System Admin",
        is_admin=True
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    print(f"Added admin user: {admin_user.email}")

    # 3. Create initial Post
    post = Post(
        title="The Future of Artificial Intelligence: Trends and Implications",
        slug="the-future-of-ai",
        excerpt="An in-depth look at how AI is shaping our world and what to expect in the coming years.",
        content="<p>Full content for the AI article...</p>",
        image="https://images.unsplash.com/photo-1620712943543-bcc4688e7485?q=80&w=2665&auto=format&fit=crop",
        read_time="5 min read",
        featured=True,
        author_id=admin_user.id,
        category_id=db_categories[0].id
    )
    db.add(post)
    db.commit()
    print(f"Added initial post: {post.title}")

    db.close()

if __name__ == "__main__":
    seed()
