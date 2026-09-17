from shop.services import ServiceShop, RabbitMailService
from shop.dao import ShopDAO, ShopVersionDAO
from core import rabbit_broker

rabbit_mail_service = RabbitMailService(broker=rabbit_broker)

service_shop = ServiceShop(repository_shop=ShopDAO,
                           repository_shop_history=ShopVersionDAO,
                           mail_service=rabbit_mail_service)