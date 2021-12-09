import unittest
import requests

class FlaskTest(unittest.TestCase):

    def test_index(self):
        response = requests.get("http://127.0.0.1:5000/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<h1 class = "subtitleFont gradient-text">~ Welcome Niner {{user.full_name}}! ~</h1>' in response.text, True)

    def test_classes(self):
        response = requests.get("http://127.0.0.1:5000/Classes")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<p><label class = "gradient-text">Enter class name </label></p>' in response.text, True)

    def test_classpage(self):
        response = requests.get("http://127.0.0.1:5000/ClassPage/<id>")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<p class = "subHeader gradient-text">Popular Post</p>' in response.text, True)

    def test_classpost(self):
        response = requests.get("http://127.0.0.1:5000/ClassPage/<id>/ClassForum")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<h1 class = "miniSubHeader gradient-text">Current Posts</h1>' in response.text, True)

    def test_displayPost(self):
        response = requests.get("http://127.0.0.1:5000/ClassPage/post/<postid>")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<h1 class = "gradient-text">Welcome {{user}}!</h1>' in response.text, True)

    def test_classesJoin(self):
        response = requests.get("http://127.0.0.1:5000/Classes/join")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<h1 class = "miniSubHeader gradient-text">Current Classes</h1>' in response.text, True)

    def test_post(self):
        response = requests.get("http://127.0.0.1:5000/ClassPage/<id>/post")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<h1 class = "subHeader gradient-text">Create Post</h1>' in response.text, True)

    def test_signup(self):
        response = requests.get("http://127.0.0.1:5000/signup")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<h2 class="title">Register</h2>' in response.text, True)

    def test_login(self):
        response = requests.get("http://127.0.0.1:5000/login")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<h2 class="subHeader gradient-text">Login</h2>' in response.text, True)

if __name__ == " __main__":
    unittest.main()
