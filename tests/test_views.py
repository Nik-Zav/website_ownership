import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_index_view(client):
    response = client.get(reverse('ownership_checker:index'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_analyze_view_get(client):
    response = client.get(reverse('ownership_checker:analyze'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_analyze_view_post_valid(client):
    response = client.post(reverse('ownership_checker:analyze'), {
        'url': 'http://example.com',
        'org_name': 'Test Org',
        'ogrn': '1234567890123'
    }, follow=False)

    assert response.status_code == 302
    assert response.url == reverse('ownership_checker:results')


@pytest.mark.django_db
def test_analyze_view_post_invalid(client):
    response = client.post(reverse('ownership_checker:analyze'), {
        'url': 'invalid'
    })
    assert response.status_code == 200