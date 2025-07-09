from unittest.mock import patch
from ownership_checker.utils.analysis import (
    search_org_name_on_site,
    search_org_details_on_site,
    search_contacts_on_site
)


def test_search_org_name_on_site(mocker):
    mock_response = mocker.Mock()
    mock_response.content = b'<html><body>Test Org</body></html>'
    mocker.patch('requests.get', return_value=mock_response)
    result = search_org_name_on_site("http://example.com", "Test Org")
    assert result['org_name_score'] > 0


def test_search_org_details_on_site(mocker):
    mock_response = mocker.Mock()
    mock_response.content = b'<html><body>OGRN 1234567890123</body></html>'
    mocker.patch('requests.get', return_value=mock_response)
    result = search_org_details_on_site("http://example.com", {"ogrn": "1234567890123"})
    assert result['ogrn_found'] is True


def test_search_contacts_on_site(mocker):
    mock_response = mocker.Mock()
    mock_response.content = b'<html><body>Phone: +79991234567</body></html>'
    mocker.patch('requests.get', return_value=mock_response)
    result = search_contacts_on_site("http://example.com", {"phone": "+79991234567"})
    assert result.get('phone_match', False) is True