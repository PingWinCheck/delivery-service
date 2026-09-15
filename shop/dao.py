from core.dao_base import DAOBase
from shop.models import Shop, ShopVersion, Address

class ShopDAO(DAOBase[Shop]):
    model = Shop


class ShopVersionDAO(DAOBase[ShopVersion]):
    model = ShopVersion


class AddressDAO(DAOBase[Address]):
    model = Address

