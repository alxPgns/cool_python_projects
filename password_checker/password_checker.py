import requests
import hashlib
import sys


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'error fetching: {res.status_code}, check the API and try again.')
    return res


def get_password_leaks_count(hashes, hash_to_check):
    clean_hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in clean_hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'Your {password} has been found {count} times. You should be more careful.')
        else:
            print(f'The password: {password} was NOT found. Carry on!')
    return f'%%%{sys.argv[0]} concluded, closing program.%%%'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
