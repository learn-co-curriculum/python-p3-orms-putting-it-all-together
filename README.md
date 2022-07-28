# Putting it All Together: ORMs Lab

## Learning Goals

- Create Python objects using SQL database records.
- Create SQL database records using Python objects.

***

## Key Vocab

- **Object-Relational Mapping (ORM)**: a technique used to convert database
records into objects in an object-oriented language.

***

## Instructions

This is a **test-driven lab**. Run `pipenv install` to create your virtual
environment and `pipenv shell` to enter the virtual environment. Then run
`pytest -x` to run your tests. Use these instructions and `pytest`'s error
messages to complete your work in the `lib/` folder.

This lab involves building a basic ORM for a Dog object. The `Dog` class
defined in `lib/dog.py` implements behaviors of a basic ORM.

### **Environment**

Our environment is going to be generated in `lib/__init__.py` using a series
of imports and instantiations. Here we will generate a `sqlite3.Connection`
object, `CONN`, and a `sqlite3.Cursor` object, `CURSOR` to be used throughout
the lab.

***

## Solving The Lab: The `pytest` Suite

### Attributes

The first test is concerned solely with making sure that our dogs have all the
required attributes and that they are readable and writable.

The `__init__` method takes `name` and `breed` as arguments and saves them as
instance attributes. `__init__` should also create an `id` instance attribute.

### `create_table()`

Create a `create_table()` class method that will create the `dogs` table if it
does not already exist. The table should have columns for an id, a name, and a
breed.

### `drop_table()`

This class method should drop the `dogs` table if it does exist- pretty much
the opposite of `create_table()`.

### `save()`

Create an instance method `save()` that saves a `Dog` object to your database.

### `create()`

This is a class method that should:

- Create a new row in the database.
- Return a new instance of the `Dog` class.

Think about how you can re-use the `save()` method to help with this one.

### `new_from_db()`

This is an interesting method. Ultimately, the database is going to return an
array representing a dog's data. We need a way to cast that data into the
appropriate attributes of a dog. This method encapsulates that functionality.
You can even think of it as `new_from_array()` (though don't name it that- your
tests will fail!) Methods like this, that return instances of the class, are
known as constructors, just like calling the class itself, except that they
extend that functionality without overwriting `__init__`.

### `get_all()`

This class method should return a list of `Dog` instances for every record in
the `dogs` table.

### `find_by_name()`

The test for this method will first insert a dog into the database and then
attempt to find it by calling the `find_by_name()` method. The expectations are
that an instance of the dog class that has all the properties of a dog is
returned, not primitive data.

Internally, what will the `find_by_name()` method do to find a dog; which SQL
statement must it run? Additionally, what might `find_by_name()` do internally
to quickly take a row and create an instance to represent that data?

**Note**: You may be tempted to use the `get_all()` method to help solve this
one. While we applaud your intuition to try and keep your code DRY, in this
case, reusing that code is actually not the best approach. Why? Remember, with
`get_all()`, we're loading all the records from the `dogs` table and converting
them to an array of Python objects, which are stored in our program's memory.
What if our `dogs` table had 10,000 rows? That's a lot of extra Python objects!
In cases like these, it's better to use SQL to only return the dogs we're
looking for, since SQL is extremely well-equipped to work with large sets of data.

### `find_by_id()`

This class method takes in an ID, and should return a single `Dog` instance for
the corresponding record in the `dogs` table with that same ID. It behaves
similarly to the `find_by_name()` method above.

## Bonus Methods

In addition to the methods described above, there are a few bonus methods if
you'd like to build out more features. The tests for these methods are commented
out in the `pytest` file. Comment them back in to run the tests for these methods.

### `find_or_create_by()`

This method takes a name and a breed as arguments. If there is already a
dog in the database with the name and breed provided, it returns that dog.
Otherwise, it inserts a new dog into the database, and returns the newly created
dog. It may be useful to use the [`lastrowid` attribute](https://stackoverflow.com/questions/6242756/how-to-retrieve-inserted-id-after-inserting-row-in-sqlite-using-python)
of your `sqlite3.Cursor` object.

### `save()` (again)

Wait, didn't we already make a `save()` method? Well, yes, but we're going to expand
its functionality! You should change it so that iff called on a `Dog` instance
that doesn't have an ID assigned, it inserts a new row into the database,
updates the instance's ID, and returns the saved `Dog` instance.

### `update()`

The test for this method will create and insert a dog, and afterwards, it will
change the name of the dog instance and call update. The expectations are that
after this operation, there is no dog left in the database with the old name. If
we query the database for a dog with the new name, we should find that dog and
the ID of that dog should be the same as the original, signifying this is the
same dog, they just changed their name.

The SQL you'll need to write for this method will involve using the `UPDATE`
keyword.

***

## Resources

- [sqlite3 - DB-API 2.0 interface for SQLite databases - Python](https://docs.python.org/3/library/sqlite3.html)
- [What is an ORM, how does it work, and how should I use one? - Stack Overflow](https://stackoverflow.com/questions/1279613/what-is-an-orm-how-does-it-work-and-how-should-i-use-one)
