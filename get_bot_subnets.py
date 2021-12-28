import os
import json
import urllib.request


def googlebot_ips(update='no'):
    """ Get Googlebot IPs ranges """
    path = 'data/ips/googlebot.json'

    if update == 'yes':
        url = 'https://www.gstatic.com/ipranges/goog.json'
        with urllib.request.urlopen(url) as data:
            resp = json.loads(data.read().decode())['prefixes']

        google_ips = {'ipv4Prefix': [], 'ipv6Prefix': []}
        for elem in resp:
            [google_ips[key].append(elem[key]) for key in elem.keys()]

        with open(path, 'w') as f:
            f.write(json.dumps(google_ips))

    elif update == 'no':
        with open(path, 'r') as f:
            google_ips = [val for val in json.load(f).values()][0]

    else:
        print('Wrong update arg value')
        exit()

    return google_ips


if __name__ == '__main__':
    googlebot_ips(update='yes')
