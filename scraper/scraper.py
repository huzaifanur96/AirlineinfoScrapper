from bs4 import BeautifulSoup
import requests
import time
import xlsxwriter


def generate_alphabetical_urls(base_url):
        alpha_url_list = []
        #ASCII value of uppercase alphabets – 65 to 90
        for c in range(65, 91): 
            temp = "{}/{}".format(base_url, chr(c))
            alpha_url_list.append(temp)
        temp = "{}/{}".format(base_url, '9')
        alpha_url_list.append(temp)
        return alpha_url_list

def generate_final_target_urls(alphabetic_url,num_pages):
        final_target_urls = []
        for c in range(1,num_pages+1): 
            temp = "{}/{}".format(alphabetic_url,c)
            final_target_urls.append(temp)
        return final_target_urls

def get_num_pages(url):
    try:
        user_agent = 'Chrome/35.0.1916.47'
        header = {'user-agent': user_agent}
        response = requests.get(url, headers=header)
        time.sleep(0.2)
        x = response.status_code
        if x != 200:
            print('Number of Pages could n0t be retrieved')
        #Find number of pages for each alphabet
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find(class_='pages')
        links_list = str(links.get_text()).split()
        num_pages = len(links_list)
        return num_pages
    except:
        return 1

def generate_sheet(target_url_list):
    user_agent = 'Chrome/35.0.1916.47'
    header = {'user-agent': user_agent}
    row = 0
    for url in target_url_list:
        response = requests.get(url, headers=header)
        time.sleep(0.2)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all(class_='dt-td')
        col = 0
        for link in links:
            temp = (link.get_text().strip('\n'))
            if col > 7:
                row +=1
                col = 0
            worksheet.write(row, col, temp)
            col += 1 
    

if __name__ == '__main__':
#Driver Code

workbook = xlsxwriter.Workbook('Airlinesdata.xlsx')
work_sheet_name = 65
base_urls_list = generate_alphabetical_urls('https://www.planespotters.net/airlines')
for url in base_urls_list:
    worksheet = workbook.add_worksheet()
    work_sheet_name +=1
    num_pages = get_num_pages(url)
    target_url_list = generate_final_target_urls(url,num_pages)
    generate_sheet(target_url_list)
workbook.close()
