class User():
    id = None
    email = None
    password = None
    fname = None
    lname = None
    is_authenticated = False
    is_active = True


    def __init__(self, id, email, password, fname, lname):
        self.id = id
        self.email = email
        self.password = password
        self.fname = fname
        self.lname = lname

    def get_id(self):
        return self.id