from shop.services import ServiceShop
from shop.dao import ShopDAO, ShopVersionDAO

service_shop = ServiceShop(ShopDAO, ShopVersionDAO)