# News-Feed CNN Indonesia
This package will get 6 Popular news from CNN Indonesia

## HOW IT WORK?
This package will scrape from [CNN Indonesia](https://www.cnnindonesia.com/) to get 6 most popular news from it website.
This package will use Requests and BeautifulSoup4, to produce output in the form of JSON that is ready use in web or mobile applications

## HOW TO USE?
''
{
import berita_terbaru_cnn

if __name__ == "__main__":
    print("Berita CNN Indonesia")
    result = berita_terbaru_cnn.ekstraksi_data()
    berita_terbaru_cnn.tampilkan_data(result)
}
'''
