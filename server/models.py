from dataclasses import dataclass

@dataclass
class User:
    id: int
    username: str
    email: str
    otp: str
    fullname: str

    def to_json(self, include_otp=False, include_id=False):
        result = {
            'username': self.username,
            'email': self.email,
            'fullname': self.fullname,
        }
        if include_id:
            result['id'] = self.id
        if include_otp:
            result['otp'] = self.otp
        return result

    @classmethod
    def from_query(cls, query_result):
        return cls(*query_result)