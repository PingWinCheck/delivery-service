from core.dao_base import DAOBase
from shop.models import Shop, ShopVersion, Address

class ShopDAO(DAOBase):
    model = Shop


class ShopVersionDAO(DAOBase):
    model = ShopVersion


class AddressDAO(DAOBase):
    model = Address

