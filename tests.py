import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase
from app import app, db, User, Post


class AppTestCase(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True

    def create_app(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = self.SQLALCHEMY_DATABASE_URI
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_page(self):
        response = self.client.get("/users")
        self.assert200(response)

    def test_new_user(self):
        response = self.client.post(
            "/user/new",
            data=dict(
                first_name="John",
                last_name="Doe",
                username="johndoe",
                image_url="https://example.com/johndoe.jpg"
            )
        )
        self.assertRedirects(response, "/user/1", status_code=302)

    def test_edit_user(self):
        response = self.client.get("/user/1/edit")
        self.assert200(response)

    def test_delete_user(self):
        response = self.client.post("/user/1/delete")
        self.assertRedirects(response, "/users", status_code=302)

    def test_add_post(self):
        response = self.client.post(
            "/user/1/add_post",
            data=dict(
                post_title="My Post",
                post_body="This is my first post"
            )
        )
        self.assertRedirects(response, "/post/1", status_code=302)

    def test_delete_post(self):
        response = self.client.post("/post/1/delete")
        self.assertRedirects(response, "/", status_code=302)

    def test_show_posts(self):
        response = self.client.get("/")
        self.assert200(response)

    def test_show_post(self):
        response = self.client.get("/post/1")
        self.assert200(response)


if __name__ == "__main__":
    unittest.main()
