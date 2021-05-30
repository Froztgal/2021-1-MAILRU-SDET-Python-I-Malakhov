from sql_models.models import TestUsers


class MySQLBuilder:

    def __init__(self, client):
        self.client = client

    def create_user(self, username, password, email, access=1, active=0, start_active_time=None):
        user = TestUsers(
            username=username,
            password=password,
            email=email,
            access=access,
            active=active,
            start_active_time=start_active_time
        )
        self.client.session.add(user)
        self.client.session.commit()  # no need if sessionmaker autocommit=True
        return user
