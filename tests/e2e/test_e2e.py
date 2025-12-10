import pytest
from playwright.sync_api import Page, expect
import time

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context"""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
    }

class TestAuthenticationFlow:
    
    def test_user_registration(self, page: Page):
        """Test user registration flow"""
        page.goto(BASE_URL)
        
        # Click register link
        page.click("#toggle-auth-link")
        
        # Wait for form to update
        time.sleep(0.5)
        
        # Fill registration form
        timestamp = int(time.time())
        page.fill("#username", f"testuser{timestamp}")
        page.fill("#email", f"testuser{timestamp}@example.com")
        page.fill("#password", "testpassword123")
        
        # Submit form
        page.click("#auth-submit-btn")
        
        # Wait for success message
        time.sleep(1)
        
        # Verify success message appears
        success_message = page.locator(".success")
        expect(success_message).to_be_visible()
    
    def test_user_login(self, page: Page):
        """Test user login flow"""
        page.goto(BASE_URL)
        
        # Register a user first
        page.click("#toggle-auth-link")
        time.sleep(0.5)
        
        timestamp = int(time.time())
        username = f"logintest{timestamp}"
        password = "testpassword123"
        
        page.fill("#username", username)
        page.fill("#email", f"{username}@example.com")
        page.fill("#password", password)
        page.click("#auth-submit-btn")
        
        time.sleep(1)
        
        # Now login
        page.click("#toggle-auth-link")
        time.sleep(0.5)
        
        page.fill("#username", username)
        page.fill("#password", password)
        page.click("#auth-submit-btn")
        
        # Wait for calculator to appear
        time.sleep(1)
        
        # Verify calculator section is visible
        calculator = page.locator("#calculator-section")
        expect(calculator).to_be_visible()
        
        # Verify logout button is visible
        logout_btn = page.locator("#logout-btn")
        expect(logout_btn).to_be_visible()
    
    def test_login_with_wrong_credentials(self, page: Page):
        """Test login with incorrect credentials"""
        page.goto(BASE_URL)
        
        page.fill("#username", "nonexistentuser")
        page.fill("#password", "wrongpassword")
        page.click("#auth-submit-btn")
        
        # Wait for error message
        time.sleep(1)
        
        # Verify error message appears
        error_message = page.locator(".error")
        expect(error_message).to_be_visible()

class TestCalculatorFlow:
    
    @pytest.fixture(autouse=True)
    def setup_logged_in_user(self, page: Page):
        """Setup: Create and login user before each test"""
        page.goto(BASE_URL)
        
        # Register
        page.click("#toggle-auth-link")
        time.sleep(0.5)
        
        timestamp = int(time.time())
        self.username = f"calctest{timestamp}"
        self.password = "testpassword123"
        
        page.fill("#username", self.username)
        page.fill("#email", f"{self.username}@example.com")
        page.fill("#password", self.password)
        page.click("#auth-submit-btn")
        
        time.sleep(1)
        
        # Login
        page.click("#toggle-auth-link")
        time.sleep(0.5)
        
        page.fill("#username", self.username)
        page.fill("#password", self.password)
        page.click("#auth-submit-btn")
        
        time.sleep(1)
    
    def test_perform_addition(self, page: Page):
        """Test performing an addition calculation"""
        # Select addition operation
        page.select_option("#operation", "add")
        
        # Enter operands
        page.fill("#operand1", "15")
        page.fill("#operand2", "25")
        
        # Submit calculation
        page.click("button[type='submit']")
        
        # Wait for result
        time.sleep(1)
        
        # Verify result is displayed
        result = page.locator("#result")
        expect(result).to_be_visible()
        
        result_value = page.locator("#result-value")
        expect(result_value).to_contain_text("40")
    
    def test_perform_subtraction(self, page: Page):
        """Test performing a subtraction calculation"""
        page.select_option("#operation", "subtract")
        page.fill("#operand1", "50")
        page.fill("#operand2", "20")
        page.click("button[type='submit']")
        
        time.sleep(1)
        
        result_value = page.locator("#result-value")
        expect(result_value).to_contain_text("30")
    
    def test_perform_multiplication(self, page: Page):
        """Test performing a multiplication calculation"""
        page.select_option("#operation", "multiply")
        page.fill("#operand1", "7")
        page.fill("#operand2", "8")
        page.click("button[type='submit']")
        
        time.sleep(1)
        
        result_value = page.locator("#result-value")
        expect(result_value).to_contain_text("56")
    
    def test_perform_division(self, page: Page):
        """Test performing a division calculation"""
        page.select_option("#operation", "divide")
        page.fill("#operand1", "100")
        page.fill("#operand2", "5")
        page.click("button[type='submit']")
        
        time.sleep(1)
        
        result_value = page.locator("#result-value")
        expect(result_value).to_contain_text("20")
    
    def test_calculation_appears_in_recent(self, page: Page):
        """Test that calculation appears in recent calculations"""
        # Perform a calculation
        page.select_option("#operation", "add")
        page.fill("#operand1", "12")
        page.fill("#operand2", "8")
        page.click("button[type='submit']")
        
        time.sleep(1)
        
        # Verify calculation appears in recent calculations
        recent_calc = page.locator("#recent-calculations .calculation-item").first
        expect(recent_calc).to_be_visible()
        expect(recent_calc).to_contain_text("12")
        expect(recent_calc).to_contain_text("8")
        expect(recent_calc).to_contain_text("20")
    
    def test_delete_calculation(self, page: Page):
        """Test deleting a calculation"""
        # Perform a calculation
        page.select_option("#operation", "add")
        page.fill("#operand1", "5")
        page.fill("#operand2", "3")
        page.click("button[type='submit']")
        
        time.sleep(1)
        
        # Click delete button
        page.click(".btn-danger")
        
        # Handle confirmation dialog
        page.on("dialog", lambda dialog: dialog.accept())
        
        time.sleep(1)
        
        # Verify success message
        success_message = page.locator(".success")
        expect(success_message).to_be_visible()

class TestLogoutFlow:
    
    def test_user_logout(self, page: Page):
        """Test user logout flow"""
        page.goto(BASE_URL)
        
        # Register and login
        page.click("#toggle-auth-link")
        time.sleep(0.5)
        
        timestamp = int(time.time())
        username = f"logouttest{timestamp}"
        
        page.fill("#username", username)
        page.fill("#email", f"{username}@example.com")
        page.fill("#password", "testpassword123")
        page.click("#auth-submit-btn")
        
        time.sleep(1)
        
        # Login
        page.click("#toggle-auth-link")
        time.sleep(0.5)
        
        page.fill("#username", username)
        page.fill("#password", "testpassword123")
        page.click("#auth-submit-btn")
        
        time.sleep(1)
        
        # Click logout
        page.click("#logout-btn")
        
        time.sleep(1)
        
        # Verify auth section is visible again
        auth_section = page.locator("#auth-section")
        expect(auth_section).to_be_visible()
        
        # Verify calculator section is hidden
        calculator_section = page.locator("#calculator-section")
        expect(calculator_section).not_to_be_visible()
