from __future__ import annotations

from typing import Iterator, List

from licitpy.entities.purchase_order import PurchaseOrder
from licitpy.types.purchase_order import Status


class PurchaseOrders:
    def __init__(self, purchase_orders: List[PurchaseOrder]):

        self._purchase_orders = purchase_orders

    def with_status(self, status: Status) -> PurchaseOrders:
        """
        Filters the purchase orders by status.
        """

        purchase_orders = [
            purchase_order
            for purchase_order in self._purchase_orders
            if purchase_order.status == status
        ]

        return PurchaseOrders(purchase_orders)

    @classmethod
    def from_tender(cls, codes: List[str]) -> PurchaseOrders:
        """
        Creates a `PurchaseOrders` instance from a list of purchase order codes.

        This method is designed to generate purchase order entities based solely on the codes
        obtained from a tender. Each code is used to create a `PurchaseOrder` instance, representing
        a purchase order with its associated code.

        These initial entities only contain the code and can later be used to retrieve or populate
        additional attributes as needed.

        Args:
            codes (List[str]): A list of strings representing the purchase order codes.

        Returns:
            PurchaseOrders: An instance of `PurchaseOrders` containing a list of `PurchaseOrder`
            entities created from the provided codes.
        """

        return cls([PurchaseOrder(code) for code in codes])

    def limit(self, limit: int) -> PurchaseOrders:
        """
        Limits the number of purchase orders.
        """

        return PurchaseOrders(self._purchase_orders[:limit])

    def count(self) -> int:
        """
        Returns the number of purchase orders.
        """

        return len(self._purchase_orders)

    def __iter__(self) -> Iterator[PurchaseOrder]:
        """
        Iterates over the purchase orders.
        """

        return iter(self._purchase_orders)

    def __getitem__(self, index: int) -> PurchaseOrder:
        """
        Gets a purchase order by index.
        """

        return self._purchase_orders[index]
