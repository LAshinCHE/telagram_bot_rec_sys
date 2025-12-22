from app.repositories.models import * 
from app.repositories.database import engine, Base 

def main():
    print("Starting application")

    print("Creating databses tables...")
    Base.metadata.create_all(bind=engine)
    print("Databases tables create!!!!")

    
    pass

if __name__ == '__main__':
    main()