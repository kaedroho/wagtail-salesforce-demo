from django.conf import settings
from django.utils import timezone
from simple_salesforce import Salesforce as BaseSalesforce, SalesforceResourceNotFound


class Salesforce(BaseSalesforce):
    def get_or_create_doc(self, doc):
        try:
            return self.WagtailDocument__c.get('WagtailID__c/' + str(doc.id))
        except SalesforceResourceNotFound:
            self.WagtailDocument__c.create({
                'WagtailID__c': doc.id,
                'Name': doc.title,
            })
            return self.WagtailDocument__c.get('WagtailID__c/' + str(doc.id))

    def get_or_create_user(self, user):
        try:
            return self.WagtailUser__c.get('WagtailID__c/' + str(user.id))
        except SalesforceResourceNotFound:
            self.WagtailUser__c.create({
                'WagtailID__c': user.id,
                'Name': str(user),
            })
            return self.WagtailUser__c.get('WagtailID__c/' + str(user.id))

    def log_doc_serve(self, doc):
        # Get document
        doc_sf = self.get_or_create_doc(doc)

        # Increment download count
        self.WagtailDocument__c.update(doc_sf['Id'], {
            'Downloads__c': (doc_sf['Downloads__c'] or 0) + 1,
        })

        print doc_sf['Downloads__c']

    def log_user_logged_in(self, user):
        # Get user
        user_sf = self.get_or_create_user(user)
        print user_sf

        # Increment login count and set last login
        self.WagtailUser__c.update(user_sf['Id'], {
            'Logins__c': (user_sf['Logins__c'] or 0) + 1,
            'LastLogin__c': timezone.now().strftime('%Y-%m-%dT%H:%M:%S'),
        })


def get_salesforce():
    return Salesforce(
        instance_url=settings.SALESFORCE_INSTANCE_URL,
        username=settings.SALESFORCE_USERNAME,
        password=settings.SALESFORCE_PASSWORD,
        security_token=settings.SALESFORCE_TOKEN,
        sandbox=settings.SALESFORCE_SANDBOX,
    )
