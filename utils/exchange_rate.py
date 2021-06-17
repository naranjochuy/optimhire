from bs4 import BeautifulSoup
from datetime import datetime
from decimal import Decimal
from django.conf import settings
from requests.exceptions import Timeout
import json
import requests
import xml.etree.ElementTree as ET


class ER:

    fixer_errors = {
        '101': 'No API Key was specified or an invalid API Key was specified.',
        '102': 'The account this API request is coming from is inactive.',
        '103': 'The requested API endpoint does not exist.',
        '104': 'The maximum allowed API amount of monthly API requests has been reached.',
        '105': 'The current subscription plan does not support this API endpoint.',
        '106': 'The current request did not return any results.',
        '201': 'An invalid base currency has been entered.',
        '202': 'One or more invalid symbols have been specified.',
        '301': 'No date has been specified. [historical]',
        '302': 'An invalid date has been specified. [historical, convert]',
        '403': 'No or an invalid amount has been specified. [convert]',
        '404': 'The requested resource does not exist.',
        '501': 'No or an invalid timeframe has been specified. [timeseries]',
        '502': 'No or an invalid "start_date" has been specified. [timeseries, fluctuation]',
        '503': 'No or an invalid "end_date" has been specified. [timeseries, fluctuation]',
        '504': 'An invalid timeframe has been specified. [timeseries, fluctuation]',
        '505': 'The specified timeframe is too long, exceeding 365 days. [timeseries, fluctuation]'
    }

    prov_changed_resp = {
        'error': True,
        'message': 'The provider changed the response.'
    }

    ex_not_available = {
        'error': True,
        'message': 'The exchange rate is not yet available.'
    }

    timeout_error = {
        'error': True,
        'message': 'Error de connection timeout.'
    }

    def get_data(self, today):
        dof = self.get_er_dof(today.strftime('%d/%m/%Y'))
        fixer = self.get_er_fixer(today.strftime('%Y-%m-%d'))
        banxico = self.get_er_banxico(today.strftime('%Y-%m-%d'))

        return {
            'dof': dof,
            'fixer': fixer,
            'banxico': banxico
        }

    def get_er_banxico(self, today):
        url = f'{settings.BANXICO_URL}{today}/{today}'
        headers = {
            'Bmx-Token': settings.BANXICO_TOKEN,
            'Accept': 'application/xml'
        }
        try:
            response = requests.get(url, headers=headers, timeout=settings.TIMEOUT).text
        except Timeout:
            return self.timeout_error
        except Exception as e:
            return {'error': True, 'message': str(e)}

        try:
            node_root = ET.fromstring(response)
            node_serie = node_root.find('serie')
        except Exception as e:
            return self.prov_changed_resp

        node_obs = node_serie.find('Obs')

        if not node_obs:
            return self.ex_not_available

        try:
            node_dato = node_obs.find('dato')
            dato = node_dato.text
            exchange_rate = Decimal(dato)
        except Exception as e:
            return self.prov_changed_resp

        return {'error': False, 'exchange_rate': exchange_rate}

    def get_er_fixer(self, date):
        today = datetime.today().strftime('%Y-%m-%d')
        url = f'{settings.FIXER_URL}{today}'
        params = {
            'access_key': settings.FIXER_TOKEN,
            'symbols': 'MXN',
            'base': 'USD'
        }

        try:
            response = requests.get(url, params=params, timeout=settings.TIMEOUT).text
        except Timeout:
            return self.timeout_error
        except Exception as e:
            return {'error': True, 'message': str(e)}

        try:
            resp = json.loads(response)
            success = resp.get('success')
            if success:
                rates = resp.get('rates')
                if not rates:
                    return self.prov_changed_resp

                exchange_rate = rates.get('MXN')
                if not exchange_rate:
                    return self.prov_changed_resp

                return {'error': False, 'exchange_rate': exchange_rate}
            else:
                error = resp.get('error')
                if not error:
                    return self.prov_changed_resp

                code = error.get('code')
                if not code:
                    return self.prov_changed_resp

                message = self.fixer_errors.get(str(code))
                if not message:
                    return self.prov_changed_resp

                return {'error': True, 'message': message}

        except Exception as e:
            return {'error': True, 'message': str(e)}

    def get_er_dof(self, today):
        url = settings.DOF_URL
        try:
            page = requests.get(url, timeout=settings.TIMEOUT)
        except Timeout:
            return self.timeout_error
        except Exception as e:
            return {'error': True, 'message': str(e)}

        try:
            soup = BeautifulSoup(page.content, 'html.parser')
            rows = [row for row in soup.find_all('tr')]
            tds = rows[14].find_all('td')
            values = [td.text.strip() for td in tds]
            date = values[0]
            ex_rate = values[1]
            datetime.strptime(date, '%d/%m/%Y')
        except Exception as e:
            return self.prov_changed_resp

        if not date == today:
            return self.ex_not_available

        try:
            exchange_rate = Decimal(ex_rate)
        except Exception as e:
            return self.ex_not_available

        return {'error': False, 'exchange_rate': exchange_rate}
