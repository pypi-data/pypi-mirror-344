# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
# Copyright (C) 2022 Northwestern University.
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Tests for user profile views."""

from flask import url_for
from flask_security import url_for_security
from helpers import login, sign_up
from invenio_accounts.models import User
from test_validators import test_usernames

from invenio_userprofiles import InvenioUserProfiles
from invenio_userprofiles.ext import finalize_app
from invenio_userprofiles.views import create_blueprint


def prefix(name, data):
    """Prefix all keys with value."""
    data = {"{0}-{1}".format(name, k): v for (k, v) in data.items()}
    data["submit"] = name
    return data


def test_profile_in_registration(base_app):
    """Test accounts registration form."""
    base_app.config.update(USERPROFILES_EXTEND_SECURITY_FORMS=True)
    InvenioUserProfiles(base_app)
    base_app.register_blueprint(create_blueprint(base_app))
    with base_app.app_context():
        finalize_app(base_app)
    app = base_app

    with app.test_request_context():
        register_url = url_for_security("register")

    with app.test_client() as client:
        resp = client.get(register_url)
        assert "profile.username" in resp.get_data(as_text=True)
        assert "profile.full_name" in resp.get_data(as_text=True)

        data = {
            "email": "test_user@test.org",
            "password": "test_password",
            "profile.username": "TestUser",
            "profile.full_name": "Test C. User",
            "profile.affiliations": "Test Org",
        }
        resp = client.post(register_url, data=data, follow_redirects=True)

    with app.test_request_context():
        user = User.query.filter_by(email="test_user@test.org").one()
        assert user.username == "TestUser"
        assert user.user_profile["full_name"] == "Test C. User"
        assert user.user_profile["affiliations"] == "Test Org"

    with app.test_client() as client:
        resp = client.get(register_url)
        data = {
            "email": "newuser@test.org",
            "password": "test_password",
            "profile.username": "TestUser",
            "profile.full_name": "Same Username",
        }
        resp = client.post(register_url, data=data)
        assert resp.status_code == 200
        assert "profile.username" in resp.get_data(as_text=True)


def test_profile_view_not_accessible_without_login(app):
    """Test the user can't access profile settings page without logging in."""
    with app.test_request_context():
        profile_url = url_for("invenio_userprofiles.profile")

    with app.test_client() as client:
        resp = client.get(profile_url, follow_redirects=True)
        assert resp.status_code == 200
        assert 'name="login_user_form"' in str(resp.data)


def test_profile_view(app):
    """Test the profile view."""
    app.config["USERPROFILES_EMAIL_ENABLED"] = False
    with app.test_request_context():
        profile_url = url_for("invenio_userprofiles.profile")

    with app.test_client() as client:
        sign_up(app, client)
        login(app, client)
        resp = client.get(profile_url)
        assert resp.status_code == 200
        assert 'name="profile_form"' in str(resp.data)

        # Valid submission should work
        resp = client.post(
            profile_url,
            data=prefix(
                "profile",
                dict(
                    username=test_usernames["valid"],
                    full_name="Valid Name",
                    affiliations="Aff",
                ),
            ),
            follow_redirects=True,
        )

        assert resp.status_code == 200
        data = resp.get_data(as_text=True)
        assert test_usernames["valid"] in data
        assert "Valid" in data
        assert "Name" in data
        assert "Aff" in data

        # Invalid submission should not save data
        resp = client.post(
            profile_url,
            data=prefix(
                "profile",
                dict(
                    username=test_usernames["invalid_characters"],
                    full_name="Valid Name",
                    affiliations="Aff",
                ),
            ),
            follow_redirects=True,
        )

        assert resp.status_code == 200
        assert test_usernames["invalid_characters"] in resp.get_data(as_text=True)

        resp = client.get(profile_url)
        assert resp.status_code == 200
        assert test_usernames["valid"] in resp.get_data(as_text=True)

        # Whitespace should be trimmed
        client.post(
            profile_url,
            data=prefix(
                "profile",
                dict(
                    username="{0} ".format(test_usernames["valid"]),
                    full_name="Valid Name ",
                    affiliations=" Aff ",
                ),
            ),
            follow_redirects=True,
        )
        resp = client.get(profile_url)

        assert resp.status_code == 200
        data = resp.get_data(as_text=True)
        assert test_usernames["valid"] in data
        assert "Valid Name " not in data
        assert " Aff " not in data


def test_profile_name_exists(app):
    """Test the profile view."""
    app.config["USERPROFILES_EMAIL_ENABLED"] = False
    error_msg = "Username is not available."

    with app.app_context():
        profile_url = url_for("invenio_userprofiles.profile")

    # Create an existing user
    email1 = "exiting@test.org"
    password1 = "123456"
    with app.test_client() as client:
        sign_up(app, client, email=email1, password=password1)
        login(app, client, email=email1, password=password1)
        assert client.get(profile_url).status_code == 200
        resp = client.post(
            profile_url,
            data=prefix(
                "profile",
                dict(username="ExistingName", full_name="Valid Name", affiliations=""),
            ),
        )
        assert error_msg not in resp.get_data(as_text=True)

    # Create another user and try setting username to same as above user with a different case.
    with app.test_client() as client:
        sign_up(app, client)
        login(app, client)
        resp = client.get(profile_url)
        assert resp.status_code == 200

        resp = client.post(
            profile_url,
            data=prefix(
                "profile",
                dict(
                    username="eXISTINGnAME", full_name="Another name", affiliations=""
                ),
            ),
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert error_msg in resp.get_data(as_text=True)


def test_profile_case_change(app):
    """Test the profile view."""
    app.config["USERPROFILES_EMAIL_ENABLED"] = False
    error_msg = "Username already exists."

    with app.app_context():
        profile_url = url_for("invenio_userprofiles.profile")

    with app.test_client() as client:
        # Create a user
        sign_up(app, client)
        login(app, client)
        resp = client.get(profile_url)
        assert resp.status_code == 200

        data = prefix(
            "profile", dict(username="valid", full_name="Another name", affiliations="")
        )

        # Set the name first time
        resp = client.post(profile_url, data=data, follow_redirects=True)
        assert resp.status_code == 200
        assert error_msg not in resp.get_data(as_text=True)

        # Set the name second time
        resp = client.post(profile_url, data=data, follow_redirects=True)
        assert resp.status_code == 200
        assert error_msg not in resp.get_data(as_text=True)

        # Change case of the username
        data = prefix(
            "profile", dict(username="Valid", full_name="Another name", affiliations="")
        )

        resp = client.post(profile_url, data=data, follow_redirects=True)
        assert resp.status_code == 200
        assert error_msg not in resp.get_data(as_text=True)


def test_send_verification_form(app):
    """Test send verification form."""
    mail = app.extensions["mail"]

    with app.test_request_context():
        profile_url = url_for("invenio_userprofiles.profile")

    with app.test_client() as client:
        sign_up(app, client)
        login(app, client)
        resp = client.get(profile_url)
        assert resp.status_code == 200
        assert "You have not yet verified your email address" in resp.get_data(
            as_text=True
        )

        with mail.record_messages() as outbox:
            assert len(outbox) == 0
            resp = client.post(
                profile_url,
                data=prefix("verification", dict(send_verification_email="Title")),
            )
            assert len(outbox) == 1


def test_change_email(app):
    """Test send verification form."""
    mail = app.extensions["mail"]
    error_msg = "Username already exists."

    with app.test_request_context():
        profile_url = url_for("invenio_userprofiles.profile")

    # Create an existing user
    email1 = "exiting@test.org"
    password1 = "123456"
    with app.test_client() as client:
        sign_up(app, client, email=email1, password=password1)
        login(app, client, email=email1, password=password1)
        assert client.get(profile_url).status_code == 200

    with app.test_client() as client:
        sign_up(app, client)
        login(app, client)
        resp = client.get(profile_url)
        assert resp.status_code == 200

        data = prefix(
            "profile",
            dict(
                username="test",
                full_name="Test User",
                affiliations="",
                email=app.config["TEST_USER_EMAIL"],
                email_repeat=app.config["TEST_USER_EMAIL"],
            ),
        )

        # Test existing email of another user.
        data["profile-email_repeat"] = data["profile-email"] = email1
        resp = client.post(profile_url, data=data, follow_redirects=True)
        assert (
            "exiting@test.org is already associated with an account."
            in resp.get_data(as_text=True)
        )

        # Test empty email
        data["profile-email_repeat"] = data["profile-email"] = ""
        resp = client.post(profile_url, data=data)
        assert "Email not provided" in resp.get_data(as_text=True)

        # Test not an email
        data["profile-email_repeat"] = data["profile-email"] = "sadfsdfs"
        resp = client.post(profile_url, data=data)
        assert "Invalid email address" in resp.get_data(as_text=True)

        # Test different emails
        data["profile-email_repeat"] = "typo@test.org"
        data["profile-email"] = "new@test.org"
        resp = client.post(profile_url, data=data)
        assert "Email addresses do not match." in resp.get_data(as_text=True)


def test_change_email_whitespace(app):
    """Test send verification form."""
    mail = app.extensions["mail"]

    with app.test_request_context():
        profile_url = url_for("invenio_userprofiles.profile")

    with app.test_client() as client:
        sign_up(app, client)
        login(app, client)
        resp = client.get(profile_url)
        assert resp.status_code == 200

        data = prefix(
            "profile",
            dict(
                username="test",
                full_name="Test User",
                affiliations="",
                email=app.config["TEST_USER_EMAIL"],
                email_repeat=app.config["TEST_USER_EMAIL"],
            ),
        )

        with mail.record_messages() as outbox:
            assert len(outbox) == 0
            data["profile-email_repeat"] = data["profile-email"] = "new@ex.org"
            resp = client.post(profile_url, data=data)
            assert "Invalid email address" not in resp.get_data(as_text=True)
            # Email was sent for email address confirmation.
            assert len(outbox) == 1
