from requests import get
from src.write_sheet import write_sheet
from pandas import DataFrame
from json import loads

def etlGYGdata(ss: str, gsheet_dict: dict) -> None:

    """
    Extract, tranforms and loads the GetYourGuide tourist data
    from the web server into a readable format in Gsheet to pivot data
    """

    print("Processing Top Cities")
    top_cities = get(url="https://travelers-api.getyourguide.com/home/top-cities")
    top_cities = loads(top_cities.content)
    top_cities = DataFrame.from_dict(top_cities['topCities']['items'])
    write_sheet(
        df=top_cities,
        sheet="Top Cities",
        service_account_dict=gsheet_dict,
        ss=ss,
        overwrite=True)

    print("Processing Points of Interest")
    top_pois = get(url="https://travelers-api.getyourguide.com/home/top-pois")
    top_pois = loads(top_pois.content)
    top_pois = DataFrame.from_dict(top_pois['topPois'])
    write_sheet(
        df=top_pois,
        sheet="Top PoI",
        service_account_dict=gsheet_dict,
        ss=ss,
        overwrite=True)

    seo_links = get(url="https://travelers-api.getyourguide.com/home/seo-links")
    seo_links = loads(seo_links.content)

    print("Processing Countries")
    top_countries = DataFrame.from_dict(seo_links['topCountries']['linkSection']['items'])
    write_sheet(
        df=top_countries,
        sheet="Top Countries",
        service_account_dict=gsheet_dict,
        ss=ss,
        overwrite=True)

    print("Processing Destinations")
    top_destinations = DataFrame.from_dict(seo_links['topDestinations']['linkSection']['items'])
    write_sheet(
        df=top_destinations,
        sheet="Top Destinations",
        service_account_dict=gsheet_dict,
        ss=ss,
        overwrite=True)
