"""Message Model Tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

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
class MessageModelTestCase(TestCase):
    """Test views for Mesasages."""

    def setUp(self):
        """Set up Test Users and Data before Tests"""

        db.drop_all()
        db.create_all()

        self.testid = 1357
        test = User.signup("test", "test@yahoo.com", "password", None)
        test.id = self.testid
        db.session.commit()

        self.test = User.query.get(self.testid)

        self.client = app.test_client()

    def tearDown(self):
        """Completed after each test"""

        r = super().tearDown()
        db.session.rollback()
        return redirects
    
    def test_Message_Model(self):
        """Creates a Message"""

        mess = Message(text="This is a Warble", user_id=self.testid)

        db.session.add(mess)
        db.session.commit()

        # Test if there is only one message for the user
        self.assertEqual(len(self.test.messages), 1)

        # Test if the one message has the correct text
        self.assertEqual(self.test.messages[0].text, "This is a Warble")

    def test_message_likes(self):
        """Check the Like Function on a Warble"""

        mess1 = Message(text="First Warble", user_id=self.testid)
        mess2 = Message(text="Second Warble", user_id=self.testid)

        test2 = User.signup("Test2", "Test2@yahoo.com", "password", None)
        test2id = 2468
        test2.id = test2id
        db.session.add([mess1, mess2, test2])
        db.session.commit()

        test2.likes.append(mess1)

        db.session.commit()

        lk = Likes.query.filter(Likes.user_id == test2id).all()

        # Check that their is only one like for the User
        self.assertEqual(len(lk), 1)

        # Check that correct Message is Liked
        self.assertEqual(l[0].message_id, mess1.id)

