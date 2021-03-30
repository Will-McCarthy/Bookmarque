class User():
    id = None
    email = None
    password = None
    name = None

    def __init__(self, id, email, password, fname, lname):
        self.id = id
        self.email = email
        self.password = password
        self.fname = fname
        self.lname = fname