import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    CONN = sqlite3.connect('lib/dogs.db')  
    CURSOR = CONN.cursor()

    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        cls.CURSOR.execute('''
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        ''')
        cls.CONN.commit()

    @classmethod
    def drop_table(cls):
        cls.CURSOR.execute('DROP TABLE IF EXISTS dogs')
        cls.CONN.commit()

    def save(self):
        if self.id is None:
            self.__class__.CURSOR.execute('''
                INSERT INTO dogs (name, breed) VALUES (?, ?)
            ''', (self.name, self.breed))
            self.id = self.__class__.CURSOR.lastrowid
        else:
            self.__class__.CURSOR.execute('''
                UPDATE dogs SET name=?, breed=? WHERE id=?
            ''', (self.name, self.breed, self.id))
        self.__class__.CONN.commit()

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog

    @classmethod
    def get_all(cls):
        cls.CURSOR.execute('SELECT * FROM dogs')
        rows = cls.CURSOR.fetchall()
        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        cls.CURSOR.execute('SELECT * FROM dogs WHERE name=?', (name,))
        row = cls.CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        return None

    @classmethod
    def find_by_id(cls, dog_id):
        cls.CURSOR.execute('SELECT * FROM dogs WHERE id=?', (dog_id,))
        row = cls.CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        return None

    # Bonus Methods

    @classmethod
    def find_or_create_by(cls, name, breed):
        existing_dog = cls.find_by_name(name)
        if existing_dog:
            return existing_dog
        else:
            return cls.create(name, breed)

    def update(self):
        # Assuming you have changed the name attribute of the Dog instance
        self.save()
