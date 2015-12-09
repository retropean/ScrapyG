from sqlalchemy.orm import sessionmaker
from models import Fares, db_connect, create_fares_table

class GhPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_fares_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        fare = Fares(**item)

        try:
            session.add(fare)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item