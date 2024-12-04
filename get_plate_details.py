import requests
from bs4 import BeautifulSoup

def get_plate_details(plate):
    url = f'https://www.carinfo.app/rc-details/{plate}'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    labels = ['Owner Name','Number','Registered RTO','City','State','RTO Phone Number','RTO Email']

    details = soup.find_all('p',class_='MuiTypography-root MuiTypography-body1 css-1ub436g')
    while len(labels) != len(details):
        details.append('')
    labels.insert(2,'Vehicle')
    labels.append('Insurance Info')
    vehicle = soup.find_all('p',class_='MuiTypography-root MuiTypography-body1 css-1rs44m9')[1]
    insurance = soup.find('p',class_='MuiTypography-root MuiTypography-body1 css-1kjcsnr')

    if insurance.contents[0] == 'Sell Car on Spinny':
        insurance.contents[0] = 'Insurance has not expired'
    details.append(insurance)
    details.insert(2,vehicle);
            
            
    print("\n---------------PLATE DETAILS---------------")
    for i in range(len(labels)):
        if details[i] != '' and len(details[i].contents) > 0:
            print(f"{labels[i]} : {details[i].contents[0]}")
        else:
            print(f"{labels[i]} : 'Informantion Not Available'")