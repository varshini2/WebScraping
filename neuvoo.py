# Data Source: https://neuvoo.ca
# Dependencies: BeautifulSoup
import requests
import re
from decimal import Decimal
from bs4 import BeautifulSoup


class Neuvoo:
    start_url = 'https://neuvoo.ca/'

    def __init__(self):
        self.job_salaries = self._get_job_salaries()


    def show_job_salaries(self):
        salaries = self._get_job_salaries()
        for job in sorted(salaries, key=salaries.get, reverse=True):
            yield job, salaries[job]

    def _get_job_salaries(self):
        url = ''.join([self.start_url, 'salary/'])
        self._salary_page = BeautifulSoup(
            requests.get(url).content, 'html.parser'
        )

        job_elements = self._salary_page.find_all(class_='card--infoList--li')
        salaries = {}
        for element in job_elements:
            try:
                job_title = element.find(class_='truncate').text.strip()
                job_salary = Decimal(
                    re.sub(
                        r'[^\d.]', '',
                        element.find(class_='card--infoList--li--perYear timeBased').text.strip()
                    )
                )
                salaries[job_title] = job_salary
            except:
                continue
        return salaries


if __name__ == '__main__':
    neuvoo = Neuvoo()
    for title, salary in neuvoo.show_job_salaries():
        print('{job:>35}: {salary:>8,}'.format(job=title, salary=salary))