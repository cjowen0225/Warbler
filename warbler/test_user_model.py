"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Set up Test Users and Data before Tests"""

        db.drop_all()
        db.create_all()

        TestUser1 = User.signup("test1", "test1@yahoo.com", "test1", None)
        TestUser2 = User.signup("test2", "test2@yahoo.com", "test2", None)
        TestUser1.id = 1234
        TestUser2.id = 5678

        db.session.commit()

        TestUser1 = User.query.get(1234)
        TestUser2 = User.query.get(5678)

        self.u1 = TestUser1
        self.u2 = TestUser2
        self.u1id = 1234
        self.u2id = 5678

        self.client = app.test_client()

    def tearDown(self):
        """This is cmopleted after each test"""

        r = super().tearDown()
        db.session.rollback()
        return r

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_follows(self):
        """Test if the User Following Feature works"""

        self.u1.following.append(self.u2)
        db.session.commit()

        self.assertEqual(len(self.u1.followers), 0)
        self.assertEqual(len(self.u1.following), 1)
        self.assertEqual(len(self.u2.followers), 1)
        self.assertEqual(len(self.u2.following), 0)
        self.assertEqual(self.u1.following[0].id, self.u2.id)
        self.assertEqual(self.u2.followers[0].id, self.u1.id)

    def test_signup(self):
        """Test a correct Signup"""

        testUser = User.signup("TestU", "user@yahoo.com", "IamUser", None)
        tid = 1236
        testUser.id = tid
        db.session.commit()

        testUser = User.query.get(tid)
        self.assertEqual(testUser.username, "TestU")
        self.assertEqual(testUser.email, "user@yahoo.com")
        self.assertNotEqual(testUser.password, "IamUser")
        self.assertTrue(testUser.password.startswith("$2b$"))

    def test_username_error(self):
        """Test a signup with an incorrect username"""

        bad = User.signup(None, "bad@yahoo.com", "badUser", None)
        bid = 9876
        bad.id = bid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_email_error(self):
        """Test a Signup with an incorrect email"""

    bad = User.signup("Bad", None, "badUser", None)
        bid = 9865
        bad.id = bid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_password_error(self):
        """Test a Signup with a password error"""

        with self.assertRaises(ValueError) as context:
            User.signup("1Tester", "1t@yahoo.com", "", None)

        with self.assertRaises(ValueError) as context:
            User.signup("2Tester", "2t@yahoo.com", None, None)

    def test_authentication(self):
        """Test the User Authentication"""

        userX = User.authenticate(self.u1.username, "test1")
        self.assertisNotNone(userX)
        self.assertEqual(userX.id, self.u1id)

    def test_username_auth_error(self):
        """Test authentication with a username Error"""

        self.assertFalse(User.authenticate("error", "test1"))

    def test_password_auth_error(self):
        """Test authetication with a password error"""

        self.assertFalse(User.authenticate(self.u1.username, "WrongPassword"))