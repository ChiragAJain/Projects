import requests as re
import hashlib
import sys

def req_api_data(query_char):
    url='https://api.pwnedpasswords.com/range/' + query_char
    res=re.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res

def get_psw_leaks_count(hashes, hash_to_check):
    hashes=(line.split(':') for line in hashes.text.splitlines())
    for h,count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    head5,tail = sha1password[:5],sha1password[5:]
    response=req_api_data(head5)
    return get_psw_leaks_count(response,tail)

def main(args):
    for password in args:
        count=pwned_api_check(password)
        if count:
            print(f'{password} was found {count} time.... you should change your password')
        else:
            print(f'{password} was not found.... you can carry on with this password')
    return 'Checked!'

if __name__=='__main__':
    sys.exit(main(sys.argv[1:]))
