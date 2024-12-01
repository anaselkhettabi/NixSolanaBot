from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Wallet

engine = create_engine('sqlite:///nix_tracker.db')
Session = sessionmaker(bind=engine)

def get_user(chat_id):
    with Session() as session:
        return session.query(User).filter_by(chat_id=chat_id).first()

def update_user_subscription(chat_id, active):
    with Session() as session:
        user = session.query(User).filter_by(chat_id=chat_id).first()
        if user:
            user.subscription_status = active
            session.commit()

def add_user_wallet(username, chat_id, subscription_status, wallet_public_key, wallet_private_key):
    with Session() as session:
        user = session.query(User).filter_by(chat_id=chat_id).first()
        if not user:
            user = User(
                username=username,
                chat_id=chat_id,
                subscription_status=subscription_status,
                wallet_public_key=wallet_public_key, 
                wallet_private_key=wallet_private_key,
            )
            session.add(user)
        else:
            user.username = username
            user.wallet_public_key = wallet_public_key
            user.wallet_private_key = wallet_private_key
        session.commit()
