# tinyjsondb

tinyjsondb is a tiny, JSON-backed, embedded database with an ORM-like API.  
It stores each model in a single `.json` file and provides CRUD operations through familiar Django-style managers.

---

## Requirements
* Python ≥ 3.8  
* [portalocker](https://pypi.org/project/portalocker/) (for cross-platform file locking)

---

## Installation

install latest commit from GitHub
```bash
pip install git+https://github.com/Waland2/tinyjsondb.git
```


## Quick start
```python
from tinyjsondb import Model, IntegerField, StringField

class User(Model):
    path_to_file = "users.json" # store data in users.json
    age  = IntegerField()
    name = StringField(default="Anonymous")

User.sync()  # create or migrate the file

# create
alice = User.objects.create(age=24, name="Alice")

# read
bob = User.objects.get(age=24)

# update
bob.update(name="Bob")

# delete
bob.delete()
```

License
MIT © 2025 Waland2