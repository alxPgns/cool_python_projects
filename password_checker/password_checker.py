import requests
import hashlib
import sys

# returns a list with hashes starting with query_char
def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char # this is the form the api expects the query 
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'error fetching: {res.status_code}, check the API and try again.')
    return res

# compare hashes from pwned page with our password hashes, if True count the times each password has been found
def get_password_leaks_count(hashes, hash_to_check):
    clean_hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in clean_hashes:
        if h == hash_to_check:
            return count
    return 0


# hash passwords with sha1, get first 5 hashed digits into function request_api_data
# call get_password_leaks_count to get the number of times a password has been hacked
def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:] 
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)

# user gives any number of passwords and main calls pwned_api_check function to check if these passwords have been pwned
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
