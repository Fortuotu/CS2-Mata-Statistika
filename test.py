from scrape import scrape_data_with_html, try_get_skin_data, parse_skin_name
from pprint import pprint

def test_scrape_data():
    with open('testing.html') as f:
        html = f.read()
    
    data = scrape_data_with_html(html)

    pprint(data)

def test_scrape_data_online():
    data = try_get_skin_data('P250 | Cassette')

    pprint(data)

def test_parse_skin_name():
    parsed = parse_skin_name('M4A4 | 龍王 (Dragon King)')
    print(parsed)

    parsed = parse_skin_name("AWP | Man-o'-war")
    print(parsed)

if __name__ == '__main__':
    #test_scrape_data()
    #test_scrape_data_online()
    test_parse_skin_name()

    pass
