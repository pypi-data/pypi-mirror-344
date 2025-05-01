import datetime
from collections import defaultdict
from typing import Dict, List, Union

from ipo_premium_client.mapper import build_ipo
from ipo_premium_client.models import IPOSubscriptionCategory, IPO, IPOType, Subscription
from ipo_premium_client.utils import parse_table_from_url, parse_tables_from_url, parse_row_based_table_from_url, \
    parse_float


class IpoPremiumClient:
    BASE_URL = 'https://ipopremium.in/'
    IPO_DETAILS_URL = 'https://ipopremium.in/view/ipo/{ipo_id}'
    IPO_TABLE_XPATH = '//*[@id="table"]'
    IPO_DETAILS_XPATH = '/html/body/div/div[1]/div[2]/div/div/div[2]/div[2]/div[2]/div[2]/table[1]'
    SHARES_WISE_BREAKUP_XPATH = '/html/body/div/div[1]/div[2]/div/div/div[2]/div[1]/div[2]/div/table[1]'
    APPLICATION_WISE_BREAKUP_XPATH = '/html/body/div/div[1]/div[2]/div/div/div[2]/div[1]/div[2]/div/table[2]'
    AMOUNT_WISE_BREAKUP_XPATH = '/html/body/div/div[1]/div[2]/div/div/div[2]/div[1]/div[2]/div/table[3]'
    IPO_TABLE_DATE_FORMAT = '%b %d, %Y'

    live_subscription_category_mapping = {
        'QIBs': IPOSubscriptionCategory.QIB,
        'HNIs': IPOSubscriptionCategory.NII,
        'HNIs 10+': IPOSubscriptionCategory.BHNI,
        'HNIs (10L+)': IPOSubscriptionCategory.BHNI,
        'HNIs 2+': IPOSubscriptionCategory.SHNI,
        'HNIs (2-10L)': IPOSubscriptionCategory.SHNI,
        'Retail': IPOSubscriptionCategory.Retail,
        'Employees': IPOSubscriptionCategory.Employee,
        'Total': IPOSubscriptionCategory.Total,
    }

    def get_live_subscription(self, ipo_id: Union[str, int]) -> Dict[str, Subscription]:
        xpaths = [self.SHARES_WISE_BREAKUP_XPATH, self.APPLICATION_WISE_BREAKUP_XPATH, self.AMOUNT_WISE_BREAKUP_XPATH]
        shares_applied_wise_breakup, application_wise_break_up, amount_wise_break_up = parse_tables_from_url(
            self.IPO_DETAILS_URL.format(ipo_id=ipo_id), xpaths)
        subscription_raw_data = defaultdict(dict)
        subscription_data = {}

        for category, subscription in shares_applied_wise_breakup.items():
            mapped_category = self.live_subscription_category_mapping.get(category)
            if mapped_category is None:
                continue

            subscription_raw_data[mapped_category]['shared_offered'] = parse_float(subscription['Offered'])
            subscription_raw_data[mapped_category]['shares_applied'] = parse_float(subscription['Applied'])

        for category, subscription in application_wise_break_up.items():
            mapped_category = self.live_subscription_category_mapping.get(category)
            if mapped_category is None:
                continue

            subscription_raw_data[mapped_category]['application_reserved'] = parse_float(subscription['Reserved'])
            subscription_raw_data[mapped_category]['application_applied'] = parse_float(subscription['Applied'])

        for category, subscription in amount_wise_break_up.items():
            mapped_category = self.live_subscription_category_mapping.get(category)
            if mapped_category is None:
                continue

            subscription_raw_data[mapped_category]['amount_offered'] = parse_float(subscription['Offered'])
            subscription_raw_data[mapped_category]['amount_applied'] = parse_float(subscription['Demand'])

        for category, subscription in subscription_raw_data.items():
            subscription_data[category] = Subscription(
                shared_offered=subscription['shared_offered'],
                shares_applied=subscription['shares_applied'],
                application_reserved=subscription.get('application_reserved'),
                application_applied=subscription.get('application_applied'),
                bid_amount=subscription['amount_applied'],
            )

        return subscription_data

    def get_mainboard_ipos(self) -> List[IPO]:
        data = parse_table_from_url(self.BASE_URL, self.IPO_TABLE_XPATH)
        ipos = []
        for name, data in data.items():
            if 'mainboard' not in name.lower():
                continue

            name = name[:name.rindex('(') - 1]
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

            if ipo.listing_date < datetime.date.today() - datetime.timedelta(days=30):
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
