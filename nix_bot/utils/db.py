from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Wallet  # Assuming models are defined separately

engine = create_engine('sqlite:///nix_tracker.db')
Session = sessionmaker(bind=engine)

def get_user(user_id):
    with Session() as session:
        return session.query(User).filter_by(id=user_id).first()

def update_user_subscription(user_id, active):
    with Session() as session:
        user = session.query(User).get(user_id)
        user.subscription_status = active
        session.commit()

def get_tracked_wallets(user_id):
    # Define a function to get wallets based on user preferences
    pass
