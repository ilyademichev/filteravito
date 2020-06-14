class RealtyApartmentPage(BasePage):
    """Home Page of Amazon India"""
    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get(TestData.BASE_URL)

    def search(self):
        self.driver.find_element(*Locators.SEARCH_TEXTBOX).clear()
        self.enter_text(Locators.SEARCH_TEXTBOX, TestData.SEARCH_TERM)
        self.click(Locators.SEARCH_SUBMIT_BUTTON)