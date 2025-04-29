from PlaywrightScraper import scrape

def test_example_com():
    html = scrape("example.com")
    assert "<title>Example Domain</title>" in html