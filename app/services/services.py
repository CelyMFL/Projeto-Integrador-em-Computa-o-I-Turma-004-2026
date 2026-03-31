import sqlalchemy


class SQLAlchemyService:
    def __init__(self, database_url):
        self.engine = sqlalchemy.create_engine(database_url)

    def get_data(self, query):
        with self.engine.connect() as connection:
            result = connection.execute(sqlalchemy.text(query))
            return result.fetchall()
        
    def update_data(self, query):
        with self.engine.connect() as connection:
            connection.execute(sqlalchemy.text(query))
            connection.commit()

    def delete_data(self, query):
        with self.engine.connect() as connection:
            connection.execute(sqlalchemy.text(query))
            connection.commit()
    
    def insert_data(self, query):
        with self.engine.connect() as connection:
            connection.execute(sqlalchemy.text(query))
            connection.commit()

    