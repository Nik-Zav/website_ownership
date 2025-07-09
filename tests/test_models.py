import pytest
from django.core.exceptions import ValidationError
from ownership_checker.models import Organization, WebsiteAnalysis


@pytest.mark.django_db
def test_organization_creation():
    org = Organization.objects.create(
        name="Test Org",
        ogrn="1234567890123"
    )
    assert org.name == "Test Org"
    assert str(org) == "Test Org"


@pytest.mark.django_db
def test_organization_ogrn_validation():
    with pytest.raises(ValidationError):
        org = Organization(name="Test", ogrn="123")
        org.full_clean()
    try:
        org = Organization(name="Test", ogrn="1234567890123")
        org.full_clean()
    except ValidationError:
        pytest.fail("Valid OGRN should not raise ValidationError")


@pytest.mark.django_db
def test_website_analysis_creation():
    org = Organization.objects.create(
        name="Test Org",
        ogrn="1234567890123"
    )
    analysis = WebsiteAnalysis.objects.create(
        organization=org,
        url="http://example.com",
        ownership_score=0.5,
        details={}
    )
    assert analysis.url == "http://example.com"