from lxml import html
import requests
import re
import whois
import datetime
import phonenumbers
from urllib.parse import urlparse


def analyze_website_ownership(url, org_data):
    score = 0
    details = {'errors': []}

    try:
        domain_info = get_domain_info(url, org_data)
        details.update(domain_info)
        score += 0.25 * domain_info.get('domain_match_score', 0)
        name_results = search_org_name_on_site(url, org_data['name'])
        details.update(name_results)
        score += 0.25 * name_results.get('org_name_score', 0)
        details_results = search_org_details_on_site(url, org_data)
        details.update(details_results)
        score += 0.25 * details_results.get('details_score', 0)
        contacts_results = search_contacts_on_site(url, org_data)
        details.update(contacts_results)
        score += 0.25 * contacts_results.get('contacts_score', 0)

    except Exception as e:
        details['errors'].append(str(e))
    score = max(0, min(1, score))
    details['final_score'] = score
    return score, details


def get_current_time():
    return datetime.now()


def get_domain_info(url, org_data):
    result = {
        'domain_match_score': 0,
        'org_name_in_whois': False,
        'domain_age_days': 0,
        'error': None
    }

    try:
        domain = urlparse(url).netloc
        if not domain:
            raise ValueError("Invalid URL")
        w = whois.whois(domain)
        creation_date = getattr(w, 'creation_date', None)
        if isinstance(creation_date, list):
            creation_date = creation_date[0] if creation_date else None
        if creation_date:
            result['domain_age_days'] = (datetime.now() - creation_date).days
        org_name = org_data['name'].lower()
        result['org_name_in_whois'] = (
            (hasattr(w, 'org') and w.org and org_name in str(w.org).lower()) or
            (hasattr(w, 'name') and w.name and org_name in str(w.name).lower()) or
            (org_name in str(w).lower())
        )
        age_score = min(result['domain_age_days'] / 365, 1) if result['domain_age_days'] > 0 else 0
        name_score = 1 if result['org_name_in_whois'] else 0.2
        result['domain_match_score'] = 0.5 * age_score + 0.5 * name_score
    except Exception as e:
        result['error'] = f"WHOIS error: {str(e)}"

    return result


def search_org_name_on_site(url, org_name):
    result = {'org_name_score': 0}
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        tree = html.fromstring(response.content)
        text = tree.text_content().lower()

        variants = [
            org_name.lower(),
            org_name.lower().replace('"', ''),
            org_name.lower().replace('ооо', 'общество с ограниченной ответственностью')
        ]

        found = [v for v in variants if v in text]
        result['found_variants'] = found
        result['org_name_score'] = min(0.3*len(found), 1)
    except Exception as e:
        result['error'] = f"Name search error: {str(e)}"
    return result


def search_org_details_on_site(url, org_data):
    result = {'details_score': 0}
    try:
        response = requests.get(url, timeout=10)
        tree = html.fromstring(response.content)
        text = tree.text_content()
        ogrn_found = org_data['ogrn'] in re.findall(r'\b\d{13}\b', text)
        result['ogrn_found'] = ogrn_found
        found_inn = set(re.findall(r'\b\d{10,12}\b', text))
        result['found_inn'] = list(found_inn)
        address_found = any(k in text.lower() for k in ['адрес', 'юридический адрес'])
        result['address_found'] = address_found
        result['details_score'] = (0.5*ogrn_found + 0.3*(len(found_inn)>0) + 0.2*address_found)
    except Exception as e:
        result['error'] = f"Details error: {str(e)}"
    return result


def search_contacts_on_site(url, org_data):
    result = {'contacts_score': 0}
    try:
        response = requests.get(url, timeout=10)
        tree = html.fromstring(response.content)
        text = tree.text_content() 
        phones = set(re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text))
        result['found_phones'] = list(phones)
        if org_data.get('phone'):
            org_phone = phonenumbers.parse(org_data['phone'], 'RU')
            for p in phones:
                try:
                    if phonenumbers.format_number(
                        phonenumbers.parse(p, 'RU'),
                        phonenumbers.PhoneNumberFormat.E164
                    ) == phonenumbers.format_number(org_phone, phonenumbers.PhoneNumberFormat.E164):
                        result['phone_match'] = True
                        break
                except: continue
        
        emails = set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
        result['found_emails'] = list(emails)
        
        if org_data.get('director_name'):
            result['director_found'] = org_data['director_name'].lower() in text.lower()
        
        result['contacts_score'] = (
            0.5*result.get('phone_match', False) + 
            0.3*(len(emails)>0) + 
            0.2*result.get('director_found', False)
        )
    except Exception as e:
        result['error'] = f"Contacts error: {str(e)}"
    return result