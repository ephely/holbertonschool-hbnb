from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User


class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)
    
    def get_user_by_email(self, email):
        """Get a user by email"""
        return self.model.query.filter_by(email=email).first()
    
    def create_user(self, user_data):
        """Create a new user"""
        if self.model.query.filter_by(email=user_data.get('email')).first():
            raise ValueError('Email already registered')

        user = User(**user_data)
        self.add(user)
        return user

    
    def update_user(self, user_id, user_data):
        """Update a user"""
        user = self.model.query.get(user_id)
        if not user:
            return None

        if 'email' in user_data and user_data['email'] != user.email:
            if self.model.query.filter_by(email=user_data['email']).first():
                raise ValueError('Email already registered')

        for key, value in user_data.items():
            setattr(user, key, value)

        self.add(user)
        return user