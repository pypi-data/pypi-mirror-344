import requests
from bs4 import BeautifulSoup

def ekstraksi_data():
    url = f'https://www.cnnindonesia.com'
    ge = requests.get(url).text
    soup = BeautifulSoup(ge, 'html.parser')
    li = soup.find('div', {'class': "overflow-y-auto relative h-[322px]"})
    lin = li.find_all('article',{'class': "pl-9 mb-4 relative"})

    i = 0
    for y in lin:
        if i == 0:
            judul1 = y.find('h2', {'class': "text-base text-cnn_black_light group-hover:text-cnn_red"})
            kategori1 = y.find('span', {'class': "text-xs text-cnn_red"})
            link1 = y.find('a')['href']
        elif i == 1:
            judul2 = y.find('h2', {'class': "text-base text-cnn_black_light group-hover:text-cnn_red"})
            kategori2 = y.find('span', {'class': "text-xs text-cnn_red"})
            link2 = y.find('a')['href']
        elif i == 2:
            judul3 = y.find('h2', {'class': "text-base text-cnn_black_light group-hover:text-cnn_red"})
            kategori3 = y.find('span', {'class': "text-xs text-cnn_red"})
            link3 = y.find('a')['href']
        elif i == 3:
            judul4 = y.find('h2', {'class': "text-base text-cnn_black_light group-hover:text-cnn_red"})
            kategori4 = y.find('span', {'class': "text-xs text-cnn_red"})
            link4 = y.find('a')['href']
        elif i == 4:
            judul5 = y.find('h2', {'class': "text-base text-cnn_black_light group-hover:text-cnn_red"})
            kategori5 = y.find('span', {'class': "text-xs text-cnn_red"})
            link5 = y.find('a')['href']
        elif i == 5:
            judul6 = y.find('h2', {'class': "text-base text-cnn_black_light group-hover:text-cnn_red"})
            kategori6 = y.find('span', {'class': "text-xs text-cnn_red"})
            link6 = y.find('a')['href']
        i = i + 1


    y = dict()
    y["judul1"] = judul1.text
    y["kategori1"] = kategori1.text
    y["link1"] = link1
    y["judul2"] = judul2.text
    y["kategori2"] = kategori2.text
    y["link2"] = link2
    y["judul3"] = judul3.text
    y["kategori3"] = kategori3.text
    y["link3"] = link3
    y["judul4"] = judul4.text
    y["kategori4"] = kategori4.text
    y["link4"] = link4
    y["judul5"] = judul5.text
    y["kategori5"] = kategori5.text
    y["link5"] = link5
    y["judul6"] = judul6.text
    y["kategori6"] = kategori6.text
    y["link6"] = link6
    return y

def tampilkan_data(result):
        if result is None:
            return 'pass'
        print('6 Berita Terpopuler CNN Indonesia')
        print(f'Judul: {result["judul1"]}')
        print(f'Kategori: {result["kategori1"]}')
        print(f'Link Berita: {result["link1"]}')
        print(f'Judul: {result["judul2"]}')
        print(f'Kategori: {result["kategori2"]}')
        print(f'Link Berita: {result["link2"]}')
        print(f'Judul: {result["judul3"]}')
        print(f'Kategori: {result["kategori3"]}')
        print(f'Link Berita: {result["link3"]}')
        print(f'Judul: {result["judul4"]}')
        print(f'Kategori: {result["kategori4"]}')
        print(f'Link Berita: {result["link4"]}')
        print(f'Judul: {result["judul5"]}')
        print(f'Kategori: {result["kategori5"]}')
        print(f'Link Berita: {result["link5"]}')
        print(f'Judul: {result["judul6"]}')
        print(f'Kategori: {result["kategori6"]}')
        print(f'Link Berita: {result["link6"]}')

if __name__ == '__main__':
    result = ekstraksi_data()
    tampilkan_data(result)