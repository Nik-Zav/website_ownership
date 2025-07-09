import os
import django
import pytest


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website_ownership.settings')
django.setup()

from ownership_checker.models import Organization, WebsiteAnalysis

@pytest.fixture
def test_organization():
    return Organization.objects.create(
        name="Тестовая Организация",
        ogrn="1234567890123",
        phone="+79991234567",
        director_name="Иванов Иван Иванович"
    )

@pytest.fixture
def test_analysis(test_organization):
    return WebsiteAnalysis.objects.create(
        organization=test_organization,
        url="https://example.com",
        ownership_score=0.75,
        details={
            "domain_info": {"score": 0.8},
            "org_name": {"score": 0.7},
            "details": {"score": 0.8},
            "contacts": {"score": 0.7}
        }
    )