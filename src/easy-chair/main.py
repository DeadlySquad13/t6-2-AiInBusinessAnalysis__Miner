import csv
import hashlib
from dataclasses import dataclass
from pathlib import Path
from re import findall
from typing import Any
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

data_path = Path("data")
raw_data_path = data_path / "raw"
processed_data_path = data_path / "processed"

baseurl = "https://easychair.org"
conferences_by_area_baseurl = urljoin(baseurl, "/cfp/")


def get_hash_from_url(url: str):
    return hashlib.md5(url.encode("utf-8")).hexdigest()


def get_filename_from_url(url: str):
    url_hash = get_hash_from_url(url)
    """Generate a safe filename from URL using hash"""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace("www.", "").split(".")[0]
    return f"{domain}_{url_hash}.html"


def fetch_html(url: str, cache_dir=raw_data_path):
    """Fetch HTML content with caching"""
    raw_data_path.mkdir(exist_ok=True)
    filepath = cache_dir / get_filename_from_url(url)

    # Return cached content if available
    if filepath.exists():
        print(f"Using cached version from {filepath}")
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

    # Fetch fresh content if no cache exists
    try:
        print(f"Fetching fresh content from {url}")
        response = requests.get(url)
        response.raise_for_status()

        # Save to cache
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response.text)
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None


@dataclass
class ResearchArea:
    name: str
    url_slug: str
    _index: int = 0
    _url: str = ""
    _fullname: str = ""

    @property
    def url(self) -> str:
        return urljoin(conferences_by_area_baseurl, self.url_slug)

    @property
    def index(self) -> str:
        temp = findall(r"\d+", self.url_slug)
        return int(temp[0])

    @property
    def fullname(self) -> str:
        return f"{self.index}%{self.name}%{get_hash_from_url(self.url)}"


def get_info(td):
    if td.a:
        return ResearchArea(name=td.a.span.contents[0], url_slug=td.a["href"])


def get_research_areas(table: NavigableString | Tag):
    tds = table.find_all("td")
    research_areas = (get_info(td) for td in tds)
    if not research_areas:
        return

    return (area for area in research_areas if area)


def format_topics(cell):
    spans = cell.find_all("span")

    return [span.get_text(strip=True) for span in spans]


HEADERS = [
    {"name": "Acronym", "index": 1},
    {"name": "Name", "index": 2},
    {"name": "Location", "index": 3},
    {"name": "Submission deadline", "index": 4},
    {"name": "Start date", "index": 5},
    {"name": "Topics", "index": 6, "format": format_topics},
]


def get_column_data(index: int, cell) -> str:
    format_callback = HEADERS[index].get(
        "format", lambda cell: cell.get_text(strip=True)
    )

    return format_callback(cell)


def get_research_area_conferences_data(
    table: NavigableString | Tag,
    area: ResearchArea,
    results_dir_path: Path,
    headers: list[dict[str, Any]],
):
    filename = f"{area.fullname}.csv"
    output_file = results_dir_path / filename

    # Prepare CSV writer.
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Write headers.
        writer.writerow([header["name"] for header in headers])

        # Process rows.
        for row in table.find_all("tr")[1:]:  # Skip header row
            cells = row.find_all(["td", "th"])
            if len(cells) >= len(headers):
                # row_data = [cell.get_text(strip=True) for cell in cells[: len(headers)]]
                row_data = [
                    get_column_data(*cell) for cell in enumerate(cells[: len(headers)])
                ]
                writer.writerow(row_data)

    print(f" - {filename}")


def html_table_to_csv(url: str, results_dir_path: Path):
    html_content = fetch_html(url)
    if not html_content:
        return False

    # Parse the HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Find a table that contains all these headers
    table_headers = None
    t = soup.find("table", id="ec:table1")

    if not t:
        return False

    research_areas = get_research_areas(t)
    area = research_areas.__next__()
    print(area.url)

    area_html_content = fetch_html(area.url)
    if not area_html_content:
        return False

    area_soup = BeautifulSoup(area_html_content, "html.parser")
    conferences_t = area_soup.find("table", id="ec:table2")

    if not conferences_t:
        return False

    # print(conferences_t.prettify())
    # print(list(get_research_areas(t)))

    # table_headers = [th.get_text(strip=True) for th in tds]

    # print(table_headers)
    # if not table:
    #     print("Could not find a table with the specified headers")
    #     print(soup.prettify())
    #     return False

    # print(table)

    results_dir_path.mkdir(exist_ok=True)
    print(f"Saving tables to {results_dir_path}:")

    get_research_area_conferences_data(
        conferences_t, area=area, results_dir_path=results_dir_path, headers=HEADERS
    )

    return True


if __name__ == "__main__":
    url = urljoin(conferences_by_area_baseurl, "area.cgi")
    html_table_to_csv(url, processed_data_path / "conferences_by_areas")
