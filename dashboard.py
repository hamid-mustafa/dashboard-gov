import os
import time
from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from RPA.PDF import PDF
import re


class DashboardGov(object):

    def __init__(self, home_page_link, download_in, agency):
        """
        It will perform the challenge task
        """
        # check weather the DOWNLOAD_IN Exist or not
        if not os.path.exists(download_in):
            os.mkdir(download_in)

        self.uii_pdf_links = []
        self.download_in = download_in
        self.home_page_link = home_page_link
        self.table_headers = []
        self.agencies_profile_data = []
        self.investment_details_table_data = {}
        self.browser = Selenium()
        self.lib = Files()
        self.pdf = PDF()
        self.browser.set_download_directory(os.path.join(os.getcwd(), f"{download_in}/"))
        self.browser.open_available_browser(home_page_link)
        self.searching_and_scraping_agencies()
        self.click_open_scrap_agency(agency)
        self.compare_all_pdf_with_title_write_pdf()
        self.browser.close_all_browsers()

    def searching_and_scraping_agencies(self):
        """
        getting and scrapping the agencies from the web page.
        :return:
        """
        self.browser.wait_until_page_contains("DIVE IN")
        self.browser.find_element('//a[@class="btn btn-default btn-lg-2x trend_sans_oneregular"]').click()
        time.sleep(1)
        self.browser.wait_until_page_contains('To get started,')
        agencies = self.browser.find_elements(
            '//div[@id="agency-tiles-widget"]//div[@class="col-sm-4 text-center noUnderline"]')
        self.agencies_profile_data = {'Companies': [], 'Amount': []}
        for agency in agencies:
            agency_split = agency.text.split("\n")
            self.agencies_profile_data['Companies'].append(agency_split[0])
            self.agencies_profile_data['Amount'].append(agency_split[2])
        wb = self.lib.create_workbook(f"{self.download_in}/Agencies.xlsx")
        wb.set_cell_value(1, 1, "Companies")
        wb.set_cell_value(1, 2, "Amount")
        wb.append_worksheet("Sheet", self.agencies_profile_data, header=True, start=1)
        wb.save()

    def get_table_header(self):
        """
        It will scrap the investment tables headers.
        :return:
        """
        while True:
            try:
                all_heads = self.browser.find_element(
                    '//table[@class="datasource-table usa-table-borderless dataTable no-footer"]').find_element_by_tag_name(
                    "thead").find_elements_by_tag_name("tr")[1].find_elements_by_tag_name("th")
                if all_heads:
                    break
            except:
                time.sleep(1)
        for head in all_heads:
            self.table_headers.append(head.text)
        self.table_headers.append("Investment Title Matched")
        self.table_headers.append("UII Matched")

    def get_uii_links(self):
        """
        It will read the investment table rows and get the uii associated links and Investment Title.
        :return:
        """
        table_rows = self.browser.find_elements('//tr[@role="row"]')
        for single_row in table_rows[2:]:
            td_elements = single_row.find_elements_by_tag_name('td')
            try:
                a_tag = single_row.find_element_by_tag_name('a').get_attribute("href")
            except:
                a_tag = ''
            if a_tag:
                self.uii_pdf_links.append(
                    {"link": a_tag, "investment_title": td_elements[2].text, "uii": td_elements[0].text}
                )

    def click_open_scrap_agency(self, agency):
        """
        It will open the agency page provided in params
        :param: agency
        :return:
        """
        try:
            self.browser.find_elements(
                '//div[@id="agency-tiles-widget"]//div[@class="col-sm-4 text-center noUnderline"]//div[@class="row top-gutter-20"]//div[@class="col-sm-12"]')[
                agency].click()
        except Exception as e:
            print(e)
            return
        self.get_table_header()
        for head in self.table_headers:
            self.investment_details_table_data[head] = []
        while True:
            current_label = self.browser.find_element("investments-table-object_info").text
            all_rows = self.browser.find_element("investments-table-object").\
                find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
            for row in all_rows:
                for i, data in enumerate(row.find_elements_by_tag_name("td")):
                    try:
                        self.investment_details_table_data[self.table_headers[i]].append(data.text)
                    except:
                        self.investment_details_table_data[self.table_headers[i]].append("")
            self.get_uii_links()
            if self.browser.find_element('investments-table-object_next').get_attribute(
                    "class") == 'paginate_button next disabled':
                break
            else:
                self.browser.find_element('investments-table-object_next').click()
                while True:
                    if current_label != self.browser.find_element("investments-table-object_info").text:
                        break
                    time.sleep(1)

        self.downloading_pdfs()

    def write_investment_data_to_excel(self):
        """
        It will write the investment table excel file into output folder
        :return:
        """
        w = self.lib.create_workbook(f"{self.download_in}/Investment.xlsx")
        for i, head in enumerate(self.table_headers):
            w.set_cell_value(1, i + 1, head)
        w.append_worksheet("Sheet", self.investment_details_table_data, header=True, start=1)
        w.save()

    def compare_all_pdf_with_title_write_pdf(self):
        """
        It will read the column name Investment title from the investment data and compare it with all the pdfs
        makes a list of pdf names in which the investment title is matched and appends the list to the investment data sheet
        Same it does with the Investment UII
        :return:
        """

        self.browser.go_to(self.home_page_link)
        pdfs_data = {}
        for link in self.uii_pdf_links:
            try:
                file_name = f'{self.download_in}/{link["uii"]}.pdf'
                new_text = self.pdf.get_text_from_pdf(file_name, 1)
                new_string = re.split(r'Bureau:|Section B', new_text[1])[1]
                pdfs_data.update({link["uii"]: new_string})
            except Exception as e:
                print(e)
        for i, value in enumerate(self.investment_details_table_data['Investment Title']):
            title_matched_string = ''
            uii_matched_string = ''
            for key, text in pdfs_data.items():
                if self.investment_details_table_data['Investment Title'][i] in text:
                    title_matched_string = title_matched_string + f'{key}'
                if self.investment_details_table_data['UII'][i] in text:
                    uii_matched_string = uii_matched_string + f'{key}'
            self.investment_details_table_data['Investment Title Matched'].append("Not Matched in any PDF" if not title_matched_string else title_matched_string)
            self.investment_details_table_data['UII Matched'].append("Not Matched in any PDF" if not uii_matched_string else uii_matched_string)
        self.write_investment_data_to_excel()

    def downloading_pdfs(self):
        """
        It will get all uii links from the webpage and download the PDF's available on those links
        :return:
        """
        for url in self.uii_pdf_links:
            self.browser.go_to(url["link"])
            terminate_interval = time.time() + 10
            while True:
                try:
                    if terminate_interval <= time.time():
                        break
                    pdf_link = self.browser.find_element('//*[contains(@id,"business-case-pdf")]//a').get_attribute(
                        "href")
                    if pdf_link:
                        self.browser.find_element('//div[@id="business-case-pdf"]').click()
                        time.sleep(1)
                        self.browser.wait_until_page_contains('Generating PDF')
                        self.browser.wait_until_page_does_not_contain('Generating PDF')
                        break
                    break
                except Exception as e:
                    time.sleep(1)


if __name__ == "__main__":
    dashboard = DashboardGov("https://itdashboard.gov/", "output", 1)
