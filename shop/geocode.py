from geopy import Photon, Location
from geopy.adapters import AioHTTPAdapter



async def get_geocode(address_raw: str) -> Location:
    async with Photon(adapter_factory=AioHTTPAdapter,
                      timeout=10) as geocoder:
        geocode: Location = await geocoder.geocode(address_raw)
    return geocode

# def get_geocode(address_raw: str) -> Location:
#     geocoder = Photon()
#     geocode: Location = geocoder.geocode(address_raw)
#     return geocode