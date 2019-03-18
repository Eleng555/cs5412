import os
import random
import string

from googleapiclient.discovery import build
from googleapiclient.errors import Error

# https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/jobs/v3/api_client

client_service = build('jobs', 'v3')
parent = 'projects/' + os.environ['GOOGLE_CLOUD_PROJECT']

def generate_company(name, address):
    # external id should be a unique Id in your system.
    external_id = name + ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(16))

    display_name = name
    headquarters_address = address

    company = {
        'display_name': display_name,
        'external_id': external_id,
        'headquarters_address': headquarters_address
    }
    print('Company generated: %s' % company)
    return company

def create_company(client_service, company_to_be_created):
    try:
        request = {'company': company_to_be_created}
        company_created = client_service.projects().companies().create(
            parent=parent, body=request).execute()
        print('Company created: %s' % company_created)
        return company_created
    except Error as e:
        print('Got exception while creating company')
        raise e
        
def get_company(client_service, company_name):
    try:
        company_existed = client_service.projects().companies().get(
            name=company_name).execute()
        print('Company existed: %s' % company_existed)
        return company_existed
    except Error as e:
        print('Got exception while getting company')
        raise e
        
def update_company(client_service, company_name, company_to_be_updated):
    try:
        request = {'company': company_to_be_updated}
        company_updated = client_service.projects().companies().patch(
            name=company_name, body=request).execute()
        print('Company updated: %s' % company_updated)
        return company_updated
    except Error as e:
        print('Got exception while updating company')
        raise e

def update_company_with_field_mask(client_service, company_name,
                                   company_to_be_updated, field_mask):
    try:
        request = {
            'company': company_to_be_updated,
            'update_mask': field_mask
        }
        company_updated = client_service.projects().companies().patch(
            name=company_name,
            body=request).execute()
        print('Company updated: %s' % company_updated)
        return company_updated
    except Error as e:
        print('Got exception while updating company with field mask')
        raise e
        
def delete_company(client_service, company_name):
    try:
        client_service.projects().companies().delete(
            name=company_name).execute()
        print('Company deleted')
    except Error as e:
        print('Got exception while deleting company')
        raise e

def create_job(client_service, job_to_be_created):
    try:
        request = {'job': job_to_be_created}
        job_created = client_service.projects().jobs().create(
            parent=parent, body=request).execute()
        print('Job created: %s' % job_created)
        return job_created
    except Error as e:
        print('Got exception while creating job')
        raise e
        
def get_job(client_service, job_name):
    try:
        job_existed = client_service.projects().jobs().get(
            name=job_name).execute()
        print('Job existed: %s' % job_existed)
        return job_existed
    except Error as e:
        print('Got exception while getting job')
        raise e
        
def update_job(client_service, job_name, job_to_be_updated):
    try:
        request = {'job': job_to_be_updated}
        job_updated = client_service.projects().jobs().patch(
            name=job_name, body=request).execute()
        print('Job updated: %s' % job_updated)
        return job_updated
    except Error as e:
        print('Got exception while updating job')
        raise e

def update_job_with_field_mask(client_service, job_name, job_to_be_updated,
                               field_mask):
    try:
        request = {'job': job_to_be_updated, 'update_mask': field_mask}
        job_updated = client_service.projects().jobs().patch(
            name=job_name, body=request).execute()
        print('Job updated: %s' % job_updated)
        return job_updated
    except Error as e:
        print('Got exception while updating job with field mask')
        raise e
        
def delete_job(client_service, job_name):
    try:
        client_service.projects().jobs().delete(name=job_name).execute()
        print('Job deleted')
    except Error as e:
        print('Got exception while deleting job')
        raise e
        
def generate_job_with_required_fields(company_name, job_title, application_uri, description):
    # Requisition id should be a unique Id in your system.
    requisition_id = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(16))

    job_title = job_title
    application_uris = [application_uri]
    description = (''+description)

    job = {
        'requisition_id': requisition_id,
        'title': job_title,
        'application_info': {'uris': application_uris},
        'description': description,
        'company_name': company_name
    }
    print('Job generated: %s' % job)
    return job
        

def run_sample():
    try:
        project_id = 'projects/' + os.environ['GOOGLE_CLOUD_PROJECT']
        #delete_company(client_service, "projects/zippy-folio-234822/companies/b3682c32-f231-4881-87c4-107f3b4b884e")
        #google_init = generate_company("Google", "San Francisco, CA")
        #google = create_company(client_service, google_init)
        google_job_init = generate_job_with_required_fields("Google", "Software Engineer", "Google.com", "test")
        google_job = create_job(client_service, google_job_init)
        response = client_service.projects().companies().list(
            parent=project_id).execute()
        print('Request Id: %s' %
              response.get('metadata').get('requestId'))
        print('Companies:')
        for company in response.get('companies'):
            print('%s' % company.get('name'))
        print('')
        #for job in response.get('jobs'):
        #    print('%s' % job.get('name'))
        #print('')

    except Error as e:
        print('Got exception while listing companies')
        raise e


if __name__ == '__main__':
    run_sample()