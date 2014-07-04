from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisiterTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

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
        inputbox.send_keys('Finish Khan Academy intro to programming')

        # When she hits enter, the page updates, and now the page lists:
        # "1: Finish Khan Academy intro to programming." as an item in a
        # to-do list.
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
                any(row.text == '1: Finish Khan Academy intro to programming'
                    for row in rows), "New to-do item did not appear in table"
        )

        # There is still a text box inviting her to add another item. She
        # enters: "Complete Code Academy jQuery course."
        self.fail('Finish the test!')

        # The page updates again, and now shows both items on her list.

        # Jocelyn wonders whether the site will remember her list. Then she
        # sees that the site has generated a unique URL for her site -- there
        # is some explanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep.


if __name__ == '__main__':
    unittest.main(warnings='ignore')
