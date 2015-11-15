# app_to_csv.py

# modules
import secret

# third party modules
import csv
import requests

class AppToCSV:

    """Migrate applications from DB to CSV."""

    def __init__(self, app_url, site_user, site_pass, file_name):
        """Constructor."""
        self.application_url = app_url
        self.site_username = site_user
        self.site_password = site_pass
        self.file_name = file_name

    def download_applications(self):
        """Download Wildhacks application json from provided URL."""
        response = requests.get(
            self.application_url,
            auth=(self.site_username, self.site_password)
        )

        response_json = response.json()
        self._handle_statuses(response_json['statuses'])

        return response_json

    def get_accepted_apps(self):
        """Filter only accepted apps from all apps."""
        self.response_json = self.download_applications()
        self.accepted_apps = []

        for key, value in self.response_json.iteritems():
            if len(key) == 64 and key in self.accepted:
                value['hash'] = key
                self.accepted_apps.append(value)

        return self.accepted_apps

    def _handle_statuses(self, statuses):
        """Create sets for accepted, rejected, waitlist students."""
        self.accepted = set()
        self.rejected = set()
        self.waitlist = set()

        for key, value in statuses.iteritems():
            if value == 'accepted':
                self.accepted.add(key)
            elif value == 'rejected':
                self.rejected.add(key)
            elif value == 'waitlist':
                self.waitlist.add(key)

    def create_csv(self):
        """Generate a CSV file using accepted applications."""
        accepted_apps = self.get_accepted_apps()
        with open(self.file_name, 'w') as f:
            header = ['First Name', 'Last Name', 'School', 'Year', '18?', 'Tshirt Size']
            writer = csv.DictWriter(f, header)

            writer.writeheader()

            for app in accepted_apps:
                entry = {
                    'First Name': app.get('first-name', ''),
                    'Last Name': app.get('last-name', ''),
                    'School': app.get('school', ''),
                    'Year': app.get('year', '').strip('\u'),
                    '18?': app.get('18yet', ''),
                    'Tshirt Size': app.get('shirt', '')
                }

                writer.writerow(entry)

        print 'CSV created!'


def main():
    migrator = AppToCSV(
        secret.application_url,
        secret.application_username,
        secret.application_password,
        'wildhacks-attendees.csv'
    )
    apps = migrator.create_csv()

if __name__ == '__main__':
    main()
