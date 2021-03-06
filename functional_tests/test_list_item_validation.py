from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Mayra goes to the home page and accidentally tries to submit an empty
        # list item. She hits Enter on the empty input box
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')

        # The home page refreshes, and there is an error message saying that
        # list items cannot be blank
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # She tries again with some text for the item, which now works
        self.get_item_input_box().send_keys('Learn CSS\n')
        self.check_for_row_in_list_table('1: Learn CSS')

        # Perversely, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys('\n')

        # She recieves a similar warning on the list page
        self.check_for_row_in_list_table('1: Learn CSS')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys('Learn JS\n')
        self.check_for_row_in_list_table('1: Learn CSS')
        self.check_for_row_in_list_table('2: Learn JS')

    def test_cannot_add_duplicate_items(self):
        # Mayra goes to the home page and starts a new list
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Meet with AEA\n')
        self.check_for_row_in_list_table('1: Meet with AEA')

        # Distracted, she accidentally tries to enter a duplicate item
        self.get_item_input_box().send_keys('Meet with AEA\n')

        # She sees a helpful error message
        self.check_for_row_in_list_table('1: Meet with AEA')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You've already got this in your list")
