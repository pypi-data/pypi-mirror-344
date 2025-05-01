class IPO:
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.open_date = kwargs.get('open_date')
        self.close_date = kwargs.get('close_date')
        self.type = kwargs.get('ipo_type')
        self.issue_price = kwargs.get('issue_price')
        self.issue_size = kwargs.get('issue_size')
        self.listing_date = kwargs.get('listing_date')
        self.allotment_date = kwargs.get('allotment_date')
        self.gmp = kwargs.get('gmp')

    @property
    def gmp_percentage(self):
        if self.gmp and self.issue_price:
            return round(100 * self.gmp / self.issue_price, 2)

        return ''

class Subscription:
    def __init__(self, shared_offered: int, shared_bid_for: int, bid_amount: float) -> None:
        super().__init__()
        self.shared_offered = shared_offered
        self.shared_bid_for = shared_bid_for
        self.bid_amount = bid_amount

    @property
    def subscription_percentage(self):
        return round(self.shared_bid_for / self.shared_offered, 2)


class IPOType:
    EQUITY = 'equity'
    DEBT = 'debt'
    SME = 'sme'


class IPOSubscriptionCategory:
    QIB = 'QIB'
    NII = 'NII'
    BHNI = 'BHNI'
    SHNI = 'SHNI'
    Retail = 'Retail'
    Employee = 'Employee'
    Total = 'Total'
