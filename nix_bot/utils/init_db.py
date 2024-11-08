from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Wallet(Base):
    __tablename__ = 'wallets'
    id = Column(Integer, primary_key=True)
    wallet_address = Column(String, unique=True)
    kol_name = Column(String)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    chat_id = Column(String, unique=True)
    subscription_status = Column(Boolean, default=False)
    wallet_public_key = Column(String, unique=True)  # Add this line
    wallet_private_key = Column(String)  # Add this line

# Initialize the database
engine = create_engine('sqlite:///nix_tracker.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def add_kol_wallet(wallet_address, kol_name):
    # Start a session
    with Session() as session:
        # Check if wallet already exists
        existing_wallet = session.query(Wallet).filter_by(wallet_address=wallet_address).first()
        if not existing_wallet:
            new_wallet = Wallet(wallet_address=wallet_address, kol_name=kol_name)
            session.add(new_wallet)
            session.commit()
            print(f"Added KOL: {kol_name} with wallet {wallet_address}")
        else:
            print(f"Wallet {wallet_address} already exists for KOL {existing_wallet.kol_name}.")

# Example usage
add_kol_wallet("4Be9CvxqHW6BYiRAxW9Q3xu1ycTMWaL5z8NX4HR3ha7t", "@idrawline")
add_kol_wallet("AVAZvHLR2PcWpDf8BXY4rVxNHYRBytycHkcB5z5QNXYm", "@blknoiz06")
