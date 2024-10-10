class RBUser:
    def __init__(self, username: str | None = None,
                 Fname: str | None = None,
                 Lname: str | None = None,
                 sex: str | None = None,
                 email: str | None = None,
                 phone: str | None = None):
        self.username = username
        self.Fname = Fname
        self.Lname = Lname
        self.sex = sex
        self.email = email
        self.phone = phone
        
    def to_dict(self) -> dict:
        data = {'username': self.username, 'Fname': self.Fname, 'Lname': self.Lname, 'sex': self.sex,
                'email': self.email, 'phone': self.phone}

        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data