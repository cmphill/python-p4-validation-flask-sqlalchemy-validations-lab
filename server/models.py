from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String, )
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    @validates('name')
    def validates_name(self, key, name):
        names = db.session.query(Author.name).all()
        if name == '':
            raise ValueError("must include a name")
        elif name in names:
            raise ValueError("names must be unique")
        
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10:
            raise ValueError("Phone number is not 10 digits")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validates_title(self, key, title):
        clickbait_phrases=["Won't Believe", "Secret", "Top", "Guess"]
        if not title:
            raise ValueError('Title must not be empty.')
        
        elif not any (substring in title for substring in clickbait_phrases):
            raise ValueError('not clickbait enough')
        return title

    @validates('content')
    def validates_content(self, key, content):
        if len(content) <= 250:
            raise ValueError('content must be at least 250 characters.')
        return content
    
    @validates('summary')
    def validates_summary(self, key, summary):
        if len(summary) >= 250:
            raise ValueError('summary is too long.')
        else:
            return summary
    
    @validates('category')
    def validates_category(self, key, category):
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError('Not a valid category')
        return category
    
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
