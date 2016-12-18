from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expectc
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime
from selenium import webdriver
from Flights.FlightPath import FlightPath


class FlightBrowser:

    def __init__(self, fly_from, fly_to, fly_on):
        self.fly_from_airport = fly_from
        self.fly_to_airport = fly_to
        self.fly_date = self.normalize_leave_date(fly_on)
        self.request_string = "http://www.momondo.co.uk/flightsearch/?Search=true&TripType=1&SegNo=1&" \
                              "SO0={0}&" \
                              "SD0={1}&" \
                              "SDP0={2}&" \
                              "AD=1&" \
                              "TK=ECO&" \
                              "DO=false&" \
                              "NA=false".format(self.fly_from_airport, self.fly_to_airport, self.fly_date)

    def normalize_leave_date(self, leave_date):
        date = datetime.strptime(leave_date, "%Y-%m-%d")
        return date.strftime("%d-%m-%Y") # comply with the momondo url request string format

    def reset_browser_state(self):
        self.fly_from_airport = None
        self.fly_to_airport = None
        self.fly_date = None
        self.request_string = "http://www.momondo.co.uk/flightsearch/?Search=true&TripType=1&SegNo=1&" \
                              "SO0={0}&" \
                              "SD0={1}&" \
                              "SDP0={2}&" \
                              "AD=1&" \
                              "TK=ECO&" \
                              "DO=false&" \
                              "NA=false"

    def get_a_to_b_flight_price(self, flight_record):
        return flight_record.find_element_by_xpath("//span[@class='value']").text

    def get_a_to_b_airlines(self, flight_record, recurse_counter=1):
        try:
            first_segment_airlines = \
                flight_record.find_element_by_xpath(
                    "//div[@class='segment segment0']"
                    "//div[@class='segment-inner']"
                    "//div[@class='airlines _{0}']"  # Formating magic to correctly get the airlines and not crash given >1 airline
                    "//div[@class='names']".format(str(recurse_counter)))
        except NoSuchElementException:
            print("We were supplied more than 1 airline")
            recurse_counter += 1
            print("Trying for {0} airlines...".format(recurse_counter))
            return self.get_a_to_b_airlines(flight_record, recurse_counter=recurse_counter)
        return first_segment_airlines

    def get_a_to_b_flight_data(self, flight_record):
        web_data = {}

        first_segment_airlines = self.get_a_to_b_airlines(flight_record)
        first_segment_outbound_airport = \
            flight_record.find_element_by_xpath(
                "//div[@class='segment segment0']//div[@class='segment-inner']//div[@class='departure ']//div[@class='inner']//div[@class='iata-time']//span[@class='iata']")
        first_segment_outbound_time = \
            flight_record.find_element_by_xpath(
                "//div[@class='segment segment0']//div[@class='segment-inner']//div[@class='departure ']//div[@class='inner']//div[@class='iata-time']//span[@class='time']")
        first_segment_inbound_time = \
            flight_record.find_element_by_xpath(
                "//div[@class='segment segment0']//div[@class='segment-inner']//div[@class='destination ']//div[@class='inner']//div[@class='iata-time']//span[@class='time']")
        first_segment_inbound_airport = \
            flight_record.find_element_by_xpath(
                "//div[@class='segment segment0']//div[@class='segment-inner']//div[@class='destination ']//div[@class='inner']//div[@class='iata-time']//span[@class='iata']")

        web_data["Airlines"] = first_segment_airlines.text
        web_data["FromAirport"] = first_segment_outbound_airport.text
        web_data["ToAirport"] = first_segment_inbound_airport.text
        web_data["OutboundTime"] = first_segment_outbound_time.text
        web_data["InboundTime"] = first_segment_inbound_time.text

        return web_data

    def execute_request(self):
        flight_path = None

        print("Using request string: " + self.request_string)

        sdriver = webdriver.PhantomJS()
        sdriver.set_window_size(1120, 550)  # bypass the nasty phantomjs bug
        sdriver.get(self.request_string)  # Execute the request for the given string

        try:
            WebDriverWait(sdriver, 90). \
                until(expectc.text_to_be_present_in_element((By.ID, "searchProgressText"), "Search complete"))  # Wait
            #  until javascript fully loads
            flight_record_result = sdriver.find_element_by_xpath("//div[@data-flight-pos='0']")

            web_request_data = self.get_a_to_b_flight_data(flight_record_result)
            web_request_data["Price"] = self.get_a_to_b_flight_price(flight_record_result)
            web_request_data["TravelDate"] = self.fly_date
            flight_path = FlightPath(web_request_data)
        except TimeoutException:
            print("Timeout on request:")
            print(self.request_string)
        finally:
            sdriver.quit()
            self.reset_browser_state()

        return flight_path
