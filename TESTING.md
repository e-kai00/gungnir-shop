## Table of Contents

- [Unit Tests](#unit-tests)
- [Responsiveness](#responsiveness)
- [Browser Compatibility](#browser-compatibility)
- [Bugs](#bugs)
- [Lighthouse](#lighthouse)
- [Validators](#validators)
- [User Stories](#user-stories)
- [Features](#features) <br><br>


### Unit Tests

The application includes a set of unit tests designed to validate the functionality of its components.
Below is a synopsis of the unit test outcomes:

**Basket Functionality**

- test_add_to_basket: ensures successful addition of a product to the basket.
- test_update_basket: validates the updating of the basket with the correct quantity.
- test_remove_from_basket: verifies the removal of a product from the basket.

**Coupon Codes Functionality**

- test_apply_coupon: test the application of a valid coupon code. 
- test_apply_invalid_coupon: test the handling of an invalid coupon code.         

<br> 

All tests passed successfully.<br>
To run the unit tests locally, use the following command: `python manage.py test`

### Responsiveness

Testing confirmed that the website adapts to different devices and screen dimensions. From larger desktop monitors to smaller mobile screens, the website seamlessly adjusts its layout and elements to ensure a consistent and engaging user experience.

| Page| Screenshort|
|:-------:|:-------:|
| Home| ![Home Page](/README_docs/testing/responsive-home.png)|
| Product page| ![Product page](/README_docs/testing/responsive-product-details.png)|
| Register page| ![Register page](/README_docs/testing/responsive-register.png)

<br>

### Browser Compatibility

Testing has been conducted, focusing on key browsers such as Chrome, Edge, and Firefox. The outcome demonstrates that the website functions as anticipated across these platforms. This includes:
- correct display of information, 
- flawless functionality for tasks such as:
  - adding products to the basket, 
  - setting quantities, 
  - choosing shipping method, 
  - applying coupon codes, 
  - completing the checkout process, 
  - leaving and updating reviews.

<br>

| Browser| Home page| Product Page| Basket|
|:-------:|:-------:|:--------:|:-------:|
| Chrome|![home](/README_docs/testing/browser-chrome-home.png)|![Chrome](/README_docs/testing/browser-chrome.jpeg)|![basket](/README_docs/testing/browser-chrome-basket.jpeg)|
| Mozilla Firefox|![home](/README_docs/testing/browser-firefox-home.png)| ![Firefox](/README_docs/testing/browser-fireFox.png)| ![basket](/README_docs/testing/browser-firefox-basket.png)|
| Microsoft Edge| ![home](/README_docs/testing/browser-edge-home.jpeg)|![Edge](/README_docs/testing/browser-edge.jpeg)| ![basket](/README_docs/testing/browser-edge-basket.jpeg)|
 


### Bugs

| # | Description | Action | Status |
|--|:-----|:------|:------:|
| 1|Error when connecting Elephantsql database:<br> *"django.db.utils.ProgrammingError: cannot cast type bigint to int4range"*<br> The root cause of the issue: initial model used fields that were not compatible with PostgreSQL. As a result, the initial migration file was generated based on these incompatible field types. Attempts to migrate to PostgreSQL kept referencing the initial migration file, causing a type mismatch during the migration process.| Reset migrations by dropping the database:<br> 1. remove all migrations files, except the `__init__.py`<br> 2. drop the current database<br> 3. create the initial migrations and generate the database schema using commands `python manage.py makemigrations` - `python manage.py migrate`| closed|
| 2|Error at calculating basket Grand total:<br> *"DoesNotExist" exception - the Coupon object you are trying to retrieve using the coupon_id does not exist in the database*<br> The root cause of the issue: code responsible for calculating the Grand Total of the basket handled existing coupon objects and ignored situations when coupon objects were not yet created| Use try-except block around the code| closed|
| 3|Error when updating items quantity in basket:<br> *"builtin_function_or_method' object is not subscriptable"*<br> The root cause of the issue: use of "[]" instead of "()" on `.pop()` method| Correct typo| closed|
| 4|The *search product* function within website demonstrates mostly accurate behavior; however, there are instances where certain search terms yield incorrect results. For example, the search term:<br> - *"ring"* yields 5 results instead of the expected 1,<br> - *"wolf"* produces 3 results instead of the anticipated 6,<br> - *"red"* retrieves 8 results instead of the intended 4.| This issue is yet to be investigated by looking into the search process, data storing, retrieving results | open|
| 5|The announcement section isn't behaving as intended. Specifically:<br> - *"last update date"* gets set correctly when the admin updates it, but it's not consistently displayed across all web browsers;<br> - when the announcement text is updated, it resets to the default text every time the Heroku dynos restart.<br> Currently, the "last updated date" is managed using localStorage, and the announcement text is stored in a file named [announcement.txt](https://github.com/e-kai00/gungnir-shop/tree/main/static/data) within the static folder. The file is processed by functions in [views.py](https://github.com/e-kai00/gungnir-shop/blob/main/home/views.py) of the home app.| The issue is yet to be solved. One potential improvement is to store the announcement data in a database. By doing so, I expect to get better control its functionality.| open|

### Lighthouse

![Lighthouse test](/README_docs/testing/lighthouse.png)


### Validators

#### HTML
- [W3C HTML Validator](https://validator.w3.org/)

  Validation helped identify and rectify several issues. Specifically, missing `<ul>` and duplicating 'id' in navbar, spelling mistakes in one of the `<span> ` tag, duplicated 'for' attribute in labels (checkout page).
  The validation report also highlighted that the 'type' attribute for JavaScript resources was unnecessary and removing it adheres to modern best practices: "Unnecessary 'type' Attribute for JavaScript Resources ". So I removed the  'type' attribute.

  Unrecognized stray `<tr>` tag issue on [basket.html](#basket-page) page: while conducting browser page source code validation, I encountered "stray tag <tr>" error. Despite thorough code inspection, I could not pinpoint the source of these tags. I ran validation of source code, confirming its cleanliness (2 errors in report are due to the W3C not recognizing Django Templating). 
  While the origin of the "stray tag <tr>" issue remains unclear, it does not seem to impact user experience or page functionality.


##### Home page
- 
  <details><summary>index.html</summary>
  <img src="README_docs/testing/validators/w3c_html/home_html.png">
  </details>

##### Product page
- 
  <details><summary>product_detail.html</summary>
  <img src="README_docs/testing/validators/w3c_html/product-detail_html.png">
  </details>

##### Basket page
- 
  <details><summary>basket.html (browser page source code)</summary>
  <img src="README_docs/testing/validators/w3c_html/basket_html.png">
  </details>
  <details><summary>basket.html (source code)</summary>
  <img src="README_docs/testing/validators/w3c_html/basket_local1_html.png">
  </details>

##### Checkout page
- 
  <details><summary>checkout.html</summary>
  <img src="README_docs/testing/validators/w3c_html/checkout_html.png">
  </details>

##### Success page
- 
  <details><summary>success.html</summary>
  <img src="README_docs/testing/validators/w3c_html/success-page_html.png">
  </details>

##### Profile page
- 
  <details><summary>profile.html</summary>
  <img src="README_docs/testing/validators/w3c_html/profile_html.png">
  </details>

<br>

#### CSS
- [W3C CSS Validator](https://jigsaw.w3.org/css-validator/)

  No errors were found.

  <details><summary>base.css</summary>
  <img src="README_docs/testing/validators/w3c_css/base_css.png">
  </details>

  <details><summary>checkout.css</summary>
  <img src="README_docs/testing/validators/w3c_css/checkout_css.png">
  </details>

  <details><summary>product-rating.css</summary>
  <img src="README_docs/testing/validators/w3c_css/product-rating_css.png">
  </details>

<br>

#### JavaScript
- [JShint](https://jshint.com/)

  The validation results were positive, with no errors detected. Some minor warnings were issued regarding missing semicolons, which have been addressed and rectified.

  <details><summary>home app / script.js</summary>
  <img src="README_docs/testing/validators/js_hint/home-script_js.png">
  </details>
  <details><summary>basket app / script.js</summary>
  <img src="README_docs/testing/validators/js_hint/basket-script_js.png">
  </details>
  <details><summary>checkout app / stripe_elements.js</summary>
  <img src="README_docs/testing/validators/js_hint/checkout-stripe-elemets_js.png">
  </details>
  <details><summary>profiles app / script.js</summary>
  <img src="README_docs/testing/validators/js_hint/profiles-script_js.png">
  </details>

<br>

#### Python
- [CI Python Linter](https://pep8ci.herokuapp.com/#)

  All .py files are compliant with the guidelines outlined in PEP8, except one: built-in Django [settings.py](https://github.com/e-kai00/gungnir-shop/blob/main/gungnir_shop/settings.py): E501 line too long (91 > 79 characters) - AUTH_PASSWORD_VALIDATORS (x4)

  - **home app**

    <details><summary>views.py</summary>
    <img src="README_docs/testing/validators/python_linter/home-views_py.png">
    </details><br>

  - **basket app**

    <details><summary>context.py</summary>
    <img src="README_docs/testing/validators/python_linter/basket-context_py.png">
    </details>
    <details><summary>views.py</summary>
    <img src="README_docs/testing/validators/python_linter/basket-views_py.png">
    </details><br>

  - **checkout app**

      <details><summary>forms.py</summary>
      <img src="README_docs/testing/validators/python_linter/checkout-forms_py.png">
      </details>
      <details><summary>models.py</summary>
      <img src="README_docs/testing/validators/python_linter/checkout-models_py.png">
      </details>
      <details><summary>views.py</summary>
      <img src="README_docs/testing/validators/python_linter/checkout-views_py.png">
      </details><br>

  - **coupons app**

    <details><summary>models.py</summary>
    <img src="README_docs/testing/validators/python_linter/coupons-models_py.png">
    </details>
    <details><summary>views.py</summary>
    <img src="README_docs/testing/validators/python_linter/coupons-views_py.png">
    </details><br>

  - **products app**

      <details><summary>forms.py</summary>
      <img src="README_docs/testing/validators/python_linter/products-forms_py.png">
      </details>
      <details><summary>models.py</summary>
      <img src="README_docs/testing/validators/python_linter/products-models_py.png">
      </details>
      <details><summary>views.py</summary>
      <img src="README_docs/testing/validators/python_linter/products-views_py.png">
      </details><br>

  - **profiles app**

      <details><summary>forms.py</summary>
      <img src="README_docs/testing/validators/python_linter/profiles-forms_py.png">
      </details>
      <details><summary>models.py</summary>
      <img src="README_docs/testing/validators/python_linter/profiles-models_py.png">
      </details>
      <details><summary>views.py</summary>
      <img src="README_docs/testing/validators/python_linter/profiles-views_py.png">
      </details><br>

  - **shipping app**

      <details><summary>forms.py</summary>
      <img src="README_docs/testing/validators/python_linter/shipping-forms_py.png">
      </details>
      <details><summary>models.py</summary>
      <img src="README_docs/testing/validators/python_linter/shipping-modals_py.png">
      </details>
      <details><summary>views.py</summary>
      <img src="README_docs/testing/validators/python_linter/shipping-views_py.png">
      </details><br>

### User Stories

"As a User I want to be able to___________________"
- [x] - *successfully implemented*
- [ ] - *yet to be implemented*<br><br>

- [x] As a Shopper I want to be able to *view all products*.
- [x] As a Shopper I want to be able to *view an individual product* details, so that I can get full info about the product.
- [x] As a Shopper I want to be able to *sort the products* by name, price, category and ratings, so that I can easily identify products that are more relevant to my preferences.
- [x] As a Shopper I want to be able to *search for a product* by name or description, so that I can quickly locate and purchase a specific item.
- [x] As a Shopper I want to be able to *view the total amount of my purchases* at any time, so that I am aware of my spendings.
- [x] As a Shopper I want to be able to *select quantity of items* I wish to purchase, so that I can buy the desired quantity with ease.
- [x] As a Shopper I want to be able to *view all items in my Basket* before placing my order , so that I can see the total cost of my purchase and review the items I will receive.
- [x] As a Shopper I want to be able to *select shipping options*, so that I can choose the shipping method that best suits my needs.
- [x] As a Shopper I want to be able to *apply my discount coupon* during checkout, so that I can benefit of the associated discounts.
- [x] As a Shopper I want to be able to easily *make payment*, so that I can checkout quickly and seamlessly.
- [x] As a Shopper I want to be able to *view order confirmation* and summary after checkout, so that I can verify the details and ensure there are no mistakes.
- [x] As a Shopper I want to *receive an email confirmation* after checkout, so that I can have a record of my order details for reference.
- [x] As a Shopper I want to be able to *view product reviews*, so that I can make informed choices and select products that best meet my needs.
- [x] As a Site owner I want to be able to *add a new product*, update existing products and delete outdated products, so that I can effectively manage and maintain an organized and up-to-date shop.
- [x] As a Shop owner I want my website to *have good search engine optimization*, so that I can improve visibility of my shop in Internet and increase the chances of converting visitors into customers.
- [x] As a Shop owner I want to be *able to send Newsletters* to my customers, so that I can share updates, and promote new products or offers.
- [x] As a Site user I want to be able to *easily register for an account*, so that I can store my data and view my orders.
- [x] As a Site user I want to be able to easily *log in and log out*, so that I can access my personal information.
- [ ] As a Site user I want to be able to *sign up and sign in using my social media account*, so that I can conveniently access the site without the need for creating separate login credentials and easily connect with my social media profile.
- [ ] As a Site user I want to be able to easily *recover my password* if I forget it, so that I can recover access to my profile.


### Features

#### User registration and authentication
| Page | User action | Expected result | Status|
|:-----|:------------|:----------------|:-----:|
| *Register* | Enter username | Field will only accept letters, numbers, and @/./+/-/_ characters| pass|
| | Enter valid email| Field will only accept email address format | pass|
| | Enter valid password (x2)| Field will only accept password format: min. 8 characters|pass|
| | Click Sing in link | Redirect to sign-in page|pass|
| | Click Sign up button| Register user and redirect to home page|pass|
|*Sign in*| Enter valid username| Filed only accept valid username|pass|
| | Enter valid password| Field will only accept existing password format|pass|
| | Click Sign up link| Redirect to sign-up page|pass|
| | Click Sign in button| Redirect to home page|pass|
|*Sign out*| Click Sign out link|Redirect to confirmation page|pass|
| | Click Sign out button| Sign out and redirect to Log-in page|pass|

#### Product Browsing and Interaction
| Page | User action | Expected result | Status|
|:-----|:------------|:----------------|:-----:|
|**Sort products**| | | |
| *Home page*| Click sidebar category| Display items of chosen category| pass|
| |1. Click 'sort by' dropdown<br> 2. Choose sort method| Display items by chosen sort method| pass|
|<br>||||
|**Search product**| | | |
| | Enter a word in search bar| Display items with entered word| *pass<br> *[bug #4](#bugs)*|
|<br>||||
|**Scroll to top button**| | | |
| *Home page and basket*| Scroll down| Scroll-to-top button becomes visible| pass|
| | Click button| Page scrolls back to the top| pass|
|<br>||||
|**View product**| | | |
| *Home page* | Click product picture or product title| Redirect to product details page| pass|
|<br>||||
|**Product details**| | | |
| | Click "-" or "+" quantity button| Subtract or add quantity| pass|
| | Click Add to basket button| Add product to basket| pass|
| | Click Keep Shopping button| Redirect to home page| pass|
|<br>||||
|**View Basket**| | | |
| | Click Basket icon| Redirect to basket page| pass|
| | 1. Click "+" or "-"<br> 2. Click "Update" link| Update items quantity| pass|
| | Click Remove link| Remove item| pass|
| | 1. Choose Shipping option from dropdown<br> 2. Click Choose button| Display shipping cost and add it to Grand total| pass|
| | 1. Enter coupon code<br> 2. Click Apply button| Display discount applied and add it to Grand total| pass|
|<br>||||
|**Checkout**| | | |
| | Click Back to Basket button| Redirect to basket page| pass|
| | 1. Fill out form<br> 2. Click Complete Order button| 1. Order processed<br> 2. Redirect to Success page<br> 3. Receive confirmation email| pass|
|<br>||||
|**Profile page**||||
| *Navbar*| Click My Profile| Redirect to Profile page| pass|
| | Click Order Number| Redirect to Success checkout page with order details| pass|
| | Click Update Information button| Update Delivery information form with new details| pass|
|<br>||||
|**Reviews**| | | |
| | Click star icons 1 through 5| Set rating 1 through 5| pass|
| | Click Post your Review button| 1. Publish review<br> 2. Set rating on a product| pass|
| | If product is already reviewed by the user and user submits the review again| Update review| pass|
|<br>||||
|**Subscribe to the newsletter**| | | |
| *Footer*| 1. Enter email address<br> 2. Click subscribe| 1. Display success message<br> 2. Add email address to the list of subscribers| pass|
|<br>||||
|**404 page**| Click Go to Homepage button| Redirect to home page| pass|
|**500 page**| Click Go to Homepage button| Redirect to home page| pass|

#### Admin functionality
| Page | User action | Expected result | Status|
|:-----|:------------|:----------------|:-----:|
| *Navbar*| Choose Product Management| Redirect to Add Product page| pass|
| *Add Product page*| Choose category from dropdown menu| Set category| pass|
| | Click Select Image button| Open window to select image| pass|
| | 1. Fill out form<br> 2. Click Add Product button| Add new product to the shop| pass|
| | Click Cancel button| Redirect to home page| pass|
| *Product detail page*| Click Edit link| Redirect to Edit Product page| pass|
| |Click Select Image button| 1. Open window to select image<br> 2. Replace image| pass|
| | Check Remove image| Remove image on submitting product update| pass|
| | Click Update Product button| Update product| pass|
| | Click Cancel button| 1. Discard changes<br> 2. Redirect to home page| pass|
| *Product detail page*| Click Delete link| 1. Prompt to confirm delete action<br> 2. Delete product<br> 3. Redirect to home page| pass|
| *Home page, announcement section*| Click Update link| Redirect to announcement page| pass|
| | 1. Update text<br> 2. Click Update button| 1. Update announcement<br> 2. Redirect to home page| *pass<br> *[bug #5](#bugs)*|

<br>

Back to [README.md](https://github.com/e-kai00/gungnir-shop/blob/main/README.md)



