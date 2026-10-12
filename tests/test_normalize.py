import pytest

from honeymap.normalize import ParseError, parse_line

GOOD_SSH = '{"dst_host": "10.0.0.5", "dst_port": 2222, "logdata": {"USERNAME": "root", "PASSWORD": "toor"}, "logtype": 4002, "node_id": "honeymap-01", "src_host": "45.1.2.3", "src_port": 51000, "utc_time": "2026-10-12 12:00:00.000001"}'


def test_ssh_login_becomes_event():
    event = parse_line(GOOD_SSH)
    assert event.src_ip == "45.1.2.3"
    assert event.service == "ssh"
    assert event.username == "root"
    assert event.password == "toor"


def test_status_message_is_skipped():
    line = '{"logtype": 1001, "logdata": {"msg": "Canary running"}}'
    assert parse_line(line) is None


def test_cut_off_line_is_rejected():
    with pytest.raises(ParseError):
        parse_line('{"dst_port": 2222, "logtype": 4002, "src_ho')

def test_missing_fields_is_rejected():
    with pytest.raises(ParseError):
        parse_line('{"logtype": 4002}')

def test_http_page_load_is_http_service():
    line = '{"dst_host": "172.18.0.2", "dst_port": 8080, "logdata": {"HOSTNAME": "localhost", "PATH": "/index.html", "SKIN": "nasLogin"}, "logtype": 3000, "node_id": "honeymap-01", "src_host": "172.18.0.1", "src_port": 51804, "utc_time": "2026-10-12 08:55:10.798497"}'
    event = parse_line(line)
    assert event.service == "http"
    assert event.username is None