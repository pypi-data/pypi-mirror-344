import datetime
from typing import Dict, List, Union

from ipo_premium_client.exceptions import ElementNotFound
from ipo_premium_client.mapper import build_ipo
from ipo_premium_client.models import IPOSubscriptionCategory, IPO, IPOType, Subscription
from ipo_premium_client.utils import parse_table_from_url, parse_row_based_table_from_url, parse_float


class IpoPremiumClient:
    BASE_URL = 'https://ipopremium.in/'
    IPO_TABLE_XPATH = '//*[@id="table"]'
    IPO_DETAILS_XPATH = '/html/body/div/div[1]/div[2]/div/div/div[2]/div[2]/div[2]/div[2]/table[1]'
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
            if 'mainboard' not in name.lower():
                continue

            issue_size = self.get_issue_size(data['url'])
            ipo = build_ipo(
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
                issue_size=issue_size,
            )

            if ipo.close_date < datetime.date.today():
                break
            ipos.append(ipo)
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

    def get_issue_size(self, url) -> str:
        keys = ['Issue Size']
        data = parse_row_based_table_from_url(url, self.IPO_DETAILS_XPATH)
        for key in keys:
            if key in data:
                issue_size_info = data[key]
                return parse_float(issue_size_info.split()[-2])
        return ''

