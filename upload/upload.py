from __future__ import print_function
import httplib2
import os
import StringIO
import argparse
import timeit

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import apiclient

try:
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument('src_group_id')
    parser.add_argument('dest_group_email')
    flags = parser.parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/groupsmigration-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/apps.groups.migration'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'G Suite Groups Migration API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'groupsmigration-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials


def read_file(path):
    message_file = open(path, 'r')
    message = message_file.read()
    message_file.close()
    return message


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('groupsmigration', 'v1', http=http)

    group_email = flags.dest_group_email
    print('Emails will be inserted into the group ' + group_email)

    messages_dir = '../data/' + flags.src_group_id + '/mbox'
    total = 0
    success = 0
    start_time = timeit.default_timer()
    for filename in os.listdir(messages_dir):
        total += 1
        stream = StringIO.StringIO()
        message = read_file(os.path.join(messages_dir, filename))
        stream.write(message)
        media = apiclient.http.MediaIoBaseUpload(stream, mimetype='message/rfc822')
        result = service.archive().insert(groupId=group_email, media_body=media).execute()
        print(result['responseCode'] + ' - ' + filename)
        if result['responseCode'] == 'SUCCESS':
            success += 1

    elapsed = timeit.default_timer() - start_time
    print('Total messages {}, failed messages {}, execution time {} sec'.format(total, total - success, elapsed))


if __name__ == '__main__':
    main()
