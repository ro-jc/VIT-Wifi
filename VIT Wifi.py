import requests
from subprocess import check_output
from time import sleep


vit_ssids = ['VIT5G', 'VIT2.4G']

login_url = "http://phc.prontonetworks.com/cgi-bin/authlogin"
logout_url = 'http://phc.prontonetworks.com/cgi-bin/authlogout'

reg_no = ''
password = ''


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
        c = 0
        while c <= 5:
            if requests.get(logout_url).ok:
                print(f'You have been successfully logged out of {connected_ssid}')
                sleep(1)
                disconnect_output = check_output('netsh wlan disconnect').decode()
                print(disconnect_output, end='')
                input()
                break
            sleep(0.5)
    else:
        print(f'Logout Failed. May be connected to another wifi network. Try going to "{logout_url}" if you really want to logout')
        input()

else:
    for ssid in vit_ssids:
        connection_output = check_output(f'netsh wlan connect {ssid}', shell=True).decode()
        print(connection_output, end='')
        sleep(0.5)
        c = 0
        while c <= 5:
            r = requests.post(login_url, data = {'userId': reg_no, 'password': password,
                            'serviceName': 'ProntoAuthentication', 'Submit22': 'Login'})
            if r.ok:
                print(f'You have been successfully logged in to {ssid}')
                input()
                break
            sleep(0.5)
            c += 1
        else:
            continue
        break
    else:
        print(f'Login failed. Try going to "{login_url}"')
        input()
