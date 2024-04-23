import folium
import openpyxl
from typing import Generator

from folium.plugins import MarkerCluster
from geopy import Nominatim
from geopy.exc import GeocoderUnavailable

LocationCache = {} #use dictionary as lookup cache
def get_data(filename:str)->Generator:
    excel_file = openpyxl.load_workbook(filename)
    jobs_sheet = excel_file["JobsInfo"]
    data = jobs_sheet.iter_rows(min_row=1)
    return data


def map_jobs(jobs_data:Generator):
    geolocator = Nominatim(user_agent="1230 class")
    # using Cincinnati becuase free Nominatim times out on smaller towns
    map_center = geolocator.geocode("Cincinnati, OH")
    LocationCache["Cincinnati, OH"] = map_center
    demo_map = folium.Map(
        location=[map_center.latitude, map_center.longitude], zoom_start=13
    )
    map_groups = MarkerCluster().add_to(demo_map)
    for job in jobs_data:
        job_city = job[4].value
        job_company = job[0].value
        job_location = None
        if job_city in LocationCache:
            job_location = LocationCache[job_city]
            print(f"LocationCache contains {len(LocationCache)} entries")
        else:
            try:
                job_location = geolocator.geocode(job_city)
            except GeocoderUnavailable:
                continue
            LocationCache[job_city] = job_location
        map_marker = folium.Marker(
            location=[job_location.latitude, job_location.longitude],
            popup=job_company
        )
        map_marker.add_to(map_groups)
    demo_map.save("TeachingDemo.html")


def main():
    jobs_data = get_data("JobData.xlsx")
    map_jobs(jobs_data)

if __name__ == '__main__':
    main()