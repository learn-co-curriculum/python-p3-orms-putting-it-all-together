import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__ (self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed

    # Create a create_table() class method that will create the dogs table if it does not already exist. The table should have columns for an id, a name, and a breed.
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        
        CURSOR.execute(sql)
        CONN.commit()
    
    # This class method should drop the dogs table if it does exist- pretty much the opposite of create_table().
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        
        CURSOR.execute(sql)
        CONN.commit()
        
    # Create an instance method save() that saves a Dog object to your database.
    def save(self):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()
    
        # solution for bonus methods
        self.id = CURSOR.lastrowid
    
    # Create a new row in the database.
    # Return a new instance of the Dog class.    
    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        
        # note that this dog will not have an id
        # the id is created for the database record, not the instance
        # the update() bonus method will not work correctly
            # [SOLUTION]: changed it so that if called on a Dog instance that doesn't have an ID assigned, it inserts a new row into the database, updates the instance's ID, and returns the saved Dog instance
        return dog
    
    # Methods like new_from_db (below), that return instances of the class, are known as constructors, just like calling the class itself, except that they extend that functionality without overwriting __init__.
    @classmethod
    def new_from_db(cls, row):
        dog = cls(
            name=row[1],
            breed=row[2],
            id=row[0]
        )

        return dog
    
    # This class method should return a list of Dog instances for every record in the dogs table.
    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM dogs
        """

        return [cls.new_from_db(row) for row in CURSOR.execute(sql).fetchall()]
    
    # The test for this method will first insert a dog into the database and then attempt to find it by calling the find_by_name() method. The expectations are that an instance of the dog class that has all the properties of a dog is returned, not primitive data.
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM dogs
            WHERE name = ?
            LIMIT 1
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        if not row:
            return None

        return Dog(
            name=row[1],
            breed=row[2],
            id=row[0]
        )

    # This class method takes in an ID, and should return a single Dog instance for the corresponding record in the dogs table with that same ID. It behaves similarly to the find_by_name() method above.
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM dogs
            WHERE id = ?
            LIMIT 1
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        if not row:
            return None

        return Dog(
            name=row[1],
            breed=row[2],
            id=row[0]
        )

    # This method takes a name and a breed as arguments. If there is already a dog in the database with the name and breed provided, it returns that dog. Otherwise, it inserts a new dog into the database, and returns the newly created dog.
    @classmethod
    def find_or_create_by(cls, name=None, breed=None):
        sql = """
            SELECT * FROM dogs
            WHERE (name, breed) = (?, ?)
            LIMIT 1
        """

        row = CURSOR.execute(sql, (name, breed)).fetchone()
        if not row:
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            """

            CURSOR.execute(sql, (name, breed))
            return Dog(
                name=name,
                breed=breed,
                id=CURSOR.lastrowid
            )

        return Dog(
            name=row[1],
            breed=row[2],
            id=row[0]
        )

    # The test for this method will create and insert a dog, and afterwards, it will change the name of the dog instance and call update. The expectations are that after this operation, there is no dog left in the database with the old name. If we query the database for a dog with the new name, we should find that dog and the ID of that dog should be the same as the original, signifying this is the same dog, they just changed their name.
    def update(self):
        sql = """
            UPDATE dogs
            SET name = ?,
                breed = ?
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()