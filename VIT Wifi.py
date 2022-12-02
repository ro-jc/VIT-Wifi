import requests
from subprocess import check_output
from time import sleep


vit_ssids = ['VIT5G', 'VIT2.4G', 'test']

login_url = "http://phc.prontonetworks.com/cgi-bin/authlogin"
logout_url = 'http://phc.prontonetworks.com/cgi-bin/authlogout'

reg_no = ''
password = ''


def login(ssid):
    for _ in range(5):
        try:
            r = requests.post(login_url, data = {'userId': reg_no, 'password': password,
                        'serviceName': 'ProntoAuthentication', 'Submit22': 'Login'}, timeout=2)
            if r.ok:
                print(f'You have been successfully logged in to {ssid}')
                input()
                return True
        except requests.exceptions.ConnectionError:
            sleep(0.5)
    return False


check_status = check_output('netsh wlan show interface')
check_status = check_status.decode().split('\r\n')

network_status = dict()
for line in check_status:
    if ':' in line:
        split = line.split(':')
        network_status[split[0].strip()] = split[1].strip()


if 'SSID' in network_status:
    connected_ssid = network_status['SSID']

    if connected_ssid in vit_ssids:
        try:
            logged_in = requests.get('https://1.1.1.1').ok
        
            for _ in range(5):
                try:
                    if requests.get(logout_url, timeout=2).ok:
                        print(f'You have been successfully logged out of {connected_ssid}')
                        sleep(1)
                        disconnect_output = check_output('netsh wlan disconnect').decode()
                        print(disconnect_output, end='')
                        input()
                        break
                except requests.exceptions.ConnectionError:
                    sleep(0.5)
            else:
                print(f'Logout Failed. Try going to "{logout_url}"')
                input()
    
        except requests.exceptions.SSLError:
            login(connected_ssid)
    else:
        print(f'You may be connected to another wifi network.')
        input()

else:
    for ssid in vit_ssids:
        connection_output = check_output(f'netsh wlan connect {ssid}', shell=True).decode()
        print(connection_output, end='')
        
        if login(ssid): break

    else:
        print(f'Connection/Login failed. Try going to "{login_url}"')
        input()