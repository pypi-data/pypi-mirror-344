from typing import Dict, List, Union

from mapper import build_ipo
from models import IPOSubscriptionCategory, IPO, IPOType, Subscription
from utils import parse_table_from_url


class IpoPremiumClient:
    BASE_URL = 'https://ipopremium.in/'
    IPO_TABLE_XPATH = '//*[@id="table"]'
    IPO_TABLE_DATE_FORMAT = '%b %d, %Y'

    live_subscription_category_mapping = {
        'Qualified Institutions': IPOSubscriptionCategory.QIB,
        'Non-Institutional Buyers': IPOSubscriptionCategory.NII,
        'bNII (bids above 10L)': IPOSubscriptionCategory.BHNI,
        'sNII (bids below 10L)': IPOSubscriptionCategory.SHNI,
        'Retail Investors': IPOSubscriptionCategory.Retail,
        'Employees': IPOSubscriptionCategory.Employee,
        'Total': IPOSubscriptionCategory.Total,
    }

    def get_live_subscription(self, ipo_id: Union[str, int]) -> Dict[str, Subscription]:
        table = parse_table_from_url(self.SUBSCRIPTION_URL.format(ipo_id=ipo_id), self.SUBSCRIPTION_XPATH)
        subscription_data = {}

        for category, subscription in table.items():
            mapped_category = None
            for k, v in self.live_subscription_category_mapping.items():
                if category.startswith(k):
                    mapped_category = v

            if mapped_category is None:
                continue

            subscription_data[mapped_category] = Subscription(
                shared_offered=int(subscription['Shares Offered*'].replace(',', '')),
                shared_bid_for=int(subscription['Shares bid for'].replace(',', '')),
                bid_amount=float(subscription['Total Amount (Rs Cr.)*'].replace(',', '')),
            )

        return subscription_data

    def get_mainboard_ipos(self) -> List[IPO]:
        data = parse_table_from_url(self.BASE_URL, self.IPO_TABLE_XPATH)
        ipos = []
        for name, data in data.items():
            ipos.append(build_ipo(
                url=data['url'],
                name=name,
                open_date=data['Open'],
                close_date=data['Close'],
                issue_prices=data['Price'],
                ipo_type=IPOType.EQUITY,
                date_format=self.IPO_TABLE_DATE_FORMAT,
                gmp=data['Premium'],
                allotment_date=data['Allotment Date'],
                listing_date=data['Listing Date'],
            ))
        return ipos

    def get_sme_ipos(self) -> List[IPO]:
        data = parse_table_from_url(self.SME_IPO_PAGE_URL, self.SME_IPO_TABLE_XPATH)
        ipos = []
        for name, data in data.items():
            ipos.append(build_ipo(
                url=data['url'],
                name=name,
                open_date=data['Open Date'],
                close_date=data['Close Date'],
                issue_prices=data['Issue Price (Rs)'],
                issue_size=data['Issue Size (Rs Cr.)'],
                ipo_type=IPOType.SME,
                date_format=self.MAIN_BOARD_IPO_DATE_FORMAT,
            ))
        return ipos
