from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError('Phone number must be exactly 10 digits')
        
    @validates('name')
    def validate_name(self, key, name):
        if not name :
            raise ValueError('Author name cannot be empty')
        author_name = db.session.query(Author.id).filter_by(name=name).first()
        if author_name is not None:
            raise ValueError('Author name must be unique')
        return name

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('title')
    def validate_title(self, key, title):
        best_titles =["Won't Believe", "Secret", "Top", "Guess"]
        if not title:
            raise ValueError('Post title cannot be empty')
        for word in best_titles:
            if word in title:
                return title
        raise ValueError('title must contain values above')

            
    @validates('content')
    def validate_content(self, key, content):
        if not content:
            raise ValueError('Post content cannot be empty')
        if len(content) < 250:
            raise ValueError('Post content must be at least 250 characters long')
        return content
    @validates('summary')
    def validate_summary(self, key, summary):
        if not summary:
            raise ValueError('Post summary cannot be empty')
        if len(summary) > 250:
            raise ValueError('Post summary must be less than or equal to 250 characters long')
        return summary
    @validates('category')
    def validate_category(self, key, category):
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError('Post category must be either Fiction or Non-Fiction')
        return category
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
