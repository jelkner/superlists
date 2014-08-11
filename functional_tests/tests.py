from django.contrib.staticfiles.testing import StaticLiveServerCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisiterTest(StaticLiveServerCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_list_and_retrieve_later(self):
        # Jocelyn has heard we are writing a cool new online to-do app.
        # She goes to check out its homepage...
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item')

        # She types "Finish Khan Academy intro to programming." into a
        # text box.
        first_text = "Finish Khan Academy intro to programming."
        inputbox.send_keys(first_text)

        # When she hits enter, the page updates, and now the page lists:
        # "1: Finish Khan Academy intro to programming." as an item in a
        # to-do list.
        inputbox.send_keys(Keys.ENTER)
        jocelyn_list_url = self.browser.current_url
        self.assertRegex(jocelyn_list_url, '/lists.+')
        self.check_for_row_in_list_table('1: {0}'.format(first_text))

        # There is still a text box inviting her to add another item. She
        # enters: "Complete Code Academy jQuery course."
        inputbox = self.browser.find_element_by_id('id_new_item')
        second_text = "Complete Code Academy jQuery course."
        inputbox.send_keys(second_text)
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list.
        self.check_for_row_in_list_table('1: {0}'.format(first_text))
        self.check_for_row_in_list_table('2: {0}'.format(second_text))

        # Now a new user, Mayra, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Jocelyn's is coming through from cookies etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Mayra visits the home page. There is no sign of Jocelyn's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(first_text, page_text)
        self.assertNotIn(second_text, page_text)

        # Mayra starts a new list by entering a new item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        third_text = 'Arrange Fall 2014 work and school schedule.'
        inputbox.send_keys(third_text)
        inputbox.send_keys(Keys.ENTER)

        # Mayra gets her own unique URL
        mayra_list_url = self.browser.current_url
        self.assertRegex(mayra_list_url, '/lists/.+')
        self.assertNotEqual(jocelyn_list_url, mayra_list_url)

        # Again, there is no trace of Jocelyn's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(first_text, page_text)
        self.assertNotIn(second_text, page_text)

    def test_layout_and_styling(self):
        # Mayra goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

        # She starts a new list and sees the input is nicely centered there too
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )
