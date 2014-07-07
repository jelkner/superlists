from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisiterTest(unittest.TestCase):

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
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention to-do lists.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )

        # She types "Finish Khan Academy intro to programming." into a
        # text box.
        first_text = "Finish Khan Academy intro to programming."
        inputbox.send_keys(first_text)

        # When she hits enter, the page updates, and now the page lists:
        # "1: Finish Khan Academy intro to programming." as an item in a
        # to-do list.
        inputbox.send_keys(Keys.ENTER)
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


        # Jocelyn wonders whether the site will remember her list. Then she
        # sees that the site has generated a unique URL for her site -- there
        # is some explanatory text to that effect.
        self.fail('Finish the test!')

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep.


if __name__ == '__main__':
    unittest.main(warnings='ignore')
