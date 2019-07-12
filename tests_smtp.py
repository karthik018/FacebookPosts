import pytest
import smtplib

@pytest.fixture(scope="module",
                params=["smtp.gmail.com", "mail.python.org"])
def smtp_connection(request):
    smtp_connection = smtplib.SMTP(request.param, 587, timeout=5)
    yield smtp_connection
    print("finalizing %s" % smtp_connection)
    smtp_connection.close()


def test_showhelo(smtp_connection):
    response, msg = smtp_connection.helo()
    assert response != 250
    assert smtp_connection.helo()
    # assert 0
