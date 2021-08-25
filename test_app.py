from flask.wrappers import Request
import app
import pytest
import json
from flask import request, Response






@pytest.fixture


def test_add_link_guest():
   
    data = {
        'url': 'updatedpassword'
    }
    url = '/guest'
    Request = app.delete(url,data=json.dumps(data))
    assert response.status_code == 200
