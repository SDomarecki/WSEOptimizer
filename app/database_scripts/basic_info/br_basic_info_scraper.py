from app.database_scripts.company_details import CompanyDetails
from app.database_scripts.page_fetcher import PageFetcher


class BRBasicInfoScraper:
    root_url = "https://www.biznesradar.pl"
    main_list_url = f"{root_url}/gielda/akcje_gpw"
    company_sector_url_base = f"{root_url}/notowania"

    def __init__(self):
        self.page_fetcher = PageFetcher()

    def get_companies(self) -> dict:
        url = BRBasicInfoScraper.main_list_url
        page = self.page_fetcher.fetch_and_parse(url)

        companies = {}
        for a in page.find_all("a", class_="s_tt"):
            name = a["title"]
            ticker = a.text.split(" ")[0]
            link = "/" + a["href"].split("/")[2]
            companies[ticker] = CompanyDetails(name, ticker, link)
        return companies

    def get_sector(self, link: str) -> str:
        url = f"{BRBasicInfoScraper.company_sector_url_base}{link}"
        page = self.page_fetcher.fetch_and_parse(url)
        sector = (
            page.find(text="Sektor:")
            .parent.parent.findNext("td")
            .contents[1]
            .contents[0]
        )
        return sector
