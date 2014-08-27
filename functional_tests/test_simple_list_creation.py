from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisiterTest(FunctionalTest):

    def test_can_start_list_and_retrieve_later(self):
        # Jocelyn has heard we are writing a cool new online to-do app.
        # She goes to check out its homepage...
        self.browser.get(self.server_url)

        # She notices the page title and header mention to-do lists.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away.
        inputbox = self.get_item_input_box()
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
        inputbox = self.get_item_input_box()
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
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(first_text, page_text)
        self.assertNotIn(second_text, page_text)

        # Mayra starts a new list by entering a new item.
        inputbox = self.get_item_input_box()
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
