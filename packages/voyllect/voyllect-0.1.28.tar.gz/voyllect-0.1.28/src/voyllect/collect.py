#!/usr/bin/env python

import datetime
import json
import sys
import time

sys.path.append('..')

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver as sw_webdriver

from voyllect.driver import get_random_user_agent, quit_driver
from voyllect.utils import n_pages


def create_products_listing_pages_files(create_products_listing_pages_brands,
                                        driver_dict,
                                        brands_page_dict,
                                        products_listing_pages_folder_path,
                                        proxy_configuration):
    """Creates the products-listing pages files.

    Args:
        create_products_listing_pages_brands (function): function used to create the products-listing
                                                         pages brands.
        driver_dict (dict): dictionary with information of the driver.
        brands_page_dict (dict): dictionary with information from the products-listing brands page.
        products_listing_pages_folder_path (str): path of the directory in which the files 
                                                  will be created.
        
    """
        
    # Get a random user agent
    driver_dict['options'].add_argument(f'user-agent={get_random_user_agent()}')

    # Set the driver
    if driver_dict['headless']:
        driver_dict['options'].add_argument("--headless=new")

    if driver_dict['use_proxy']:
        # Set the options for seleniumwire
        seleniumwire_options = {'proxy': {'https': driver_dict['proxy_url'], 'verify_ssl': False}}

        driver = sw_webdriver.Chrome(
            driver_dict['driver_path'], 
            options=driver_dict['options'], 
            seleniumwire_options=seleniumwire_options)
    else:
        service = Service(executable_path=driver_dict['driver_path'])
        driver = webdriver.Chrome(service=service, options=driver_dict['options'])
    
    # Create the products-listing pages brands
    create_products_listing_pages_brands(
        driver=driver,
        brands_page_dict=brands_page_dict,
        products_listing_pages_folder_path=products_listing_pages_folder_path)
    
    # Quit the driver
    quit_driver(driver=driver, delete_cookies=driver_dict['delete_cookies'])


def generate_products_listing_pages_dicts(from_brands, 
                                          brands,
                                          from_categories, 
                                          categories,  
                                          from_search_keywords, 
                                          search_keywords):
    """Generates the list of products-listing pages dictionaries.
    
    Args:
        from_brands (bool): whether to include product-listing pages from brands.
        brands (list): list of brand products-listing pages.
        from_categories (bool): whether to include product-listing pages from categories.
        categories (list): list of category products-listing pages.
        from_search_keywords (bool): whether to include product-listing pages from searches.
        search_keywords (list): list of search products-listing pages.
        
    Returns:
        list[dict], List of products-listing pages dictionaries.
    """

    products_listing_page_dicts = []

    if from_brands:
        if brands:
            for brand in brands:
                products_listing_page_dicts.append({
                    'origin': 'brands',
                    'product_brand': brand[0],
                    'url': brand[-1],
                })
    
    if from_categories:
        if categories:
            for category in categories:
                products_listing_page_dicts.append({
                    'origin': 'categories',
                    'category': category[0],
                    'sub_category': category[1],
                    'sub_sub_category': category[2],
                    'url': category[-1],
                }) 
        
    if from_search_keywords:
        if search_keywords:
            for search_keyword in search_keywords:
                products_listing_page_dicts.append({
                    'origin': 'search_keywords',
                    'search_keyword': search_keyword[0],
                    'url': search_keyword[-1],
                }) 

    return products_listing_page_dicts


def get_products_listing_pages_dicts_to_collect(brands, 
                                                categories, 
                                                search_keywords, 
                                                args):
    """Gets the products-listing pages dictionaries to collect 
    from the parsed arguments.
    
    Args:
        brands (list): list of brand products-listing pages.
        categories (list): list of category products-listing pages.
        search_keywords (list): list of search products-listing pages.
        args (dict): parsed arguments.
        
    Returns:
        list[dict], List of products-listing pages dictionaries.
    """

    if args.products_listing_page_url:
        products_listing_pages_dicts = [{
            'origin': 'parser',
            'url': args.products_listing_page_url,
        }]
    else:
        products_listing_pages_dicts = \
            generate_products_listing_pages_dicts(from_brands=args.from_brands,
                                                  brands=brands,
                                                  from_categories=args.from_categories,
                                                  categories=categories,
                                                  from_search_keywords=args.from_search_keywords,
                                                  search_keywords=search_keywords)
    
    return products_listing_pages_dicts


def retrieve_data_from_products_listing_page_dict_to_url_dict(products_listing_page_dict, 
                                                              url_dict):
    """Retrieves data from products-listing page dictionary to URL dictionary.
    
    Args:
        products_listing_page_dict (dict): dictionary with information of 
                                           the products-listing page.
        url_dict (dict): dictionary with the URL information.
        
    Returns:
        dict, Dictionary with the URL information and the origin of 
              the products-listing page. 
    """

    url_dict['products_listing_page_origin'] = \
        products_listing_page_dict['origin']
    url_dict['products_listing_page_url'] = \
        products_listing_page_dict['url']
    if products_listing_page_dict.get('product_brand'):
        url_dict['products_listing_page_product_brand'] = \
            products_listing_page_dict['product_brand']
    if products_listing_page_dict.get('search_keyword'):
        url_dict['products_listing_page_search_keyword'] = \
            products_listing_page_dict['search_keyword']
    if products_listing_page_dict.get('category'):
        url_dict['products_listing_page_category'] = \
            products_listing_page_dict['category']
    if products_listing_page_dict.get('sub_category'):
        url_dict['products_listing_page_sub_category'] = \
            products_listing_page_dict['sub_category']
    if products_listing_page_dict.get('sub_sub_category'):
        url_dict['products_listing_page_sub_sub_category'] = \
            products_listing_page_dict['sub_sub_category']
        
    return url_dict


def retrieve_data_from_product_dict_to_review_dict(product_dict, 
                                                   review_dict):
    """Saves the product data in the review dictionary.

    Args:
        product_dict (dict): dictionary with product data.
        review_dict (dict): dictionary with reviews data.

    Returns:
        dict, Dictionary with reviews data.
    """

    # Product name & brand
    review_dict['product_name'] = product_dict['product_name']
    review_dict['product_sub_name'] = product_dict['product_sub_name']
    review_dict['product_brand'] = product_dict['product_brand']
    review_dict['product_brand_line'] = product_dict['product_brand_line']
    # URL
    review_dict['url'] = product_dict['url']
    # Categories
    review_dict['category'] = product_dict['category']
    review_dict['sub_category'] = product_dict['sub_category']
    review_dict['sub_sub_category'] = product_dict['sub_sub_category']
    review_dict['sub_sub_sub_category'] = product_dict['sub_sub_sub_category']
    # Codes
    review_dict['code_asin'] = product_dict['code_asin']
    review_dict['code_ean'] = product_dict['code_ean']
    review_dict['code_gtin'] = product_dict['code_gtin']
    review_dict['code_sku'] = product_dict['code_sku']
    review_dict['code_source'] = product_dict['code_source']

    return review_dict


def collect_urls(save_products_listing_page_data_functions_dict,
                 driver_dict, 
                 source_dict,
                 products_listing_pages_dicts, 
                 new_urls_folder_path):
    """Collects the new URLs.

    Args:
        save_products_listing_page_data_functions_dict (dict): dictionary with the function 
                                                               to save products-listing page data.
        driver_dict (dict): dictionary with information of the driver.
        source_dict (dict): dictionary with information from the source.
        products_listing_pages_dicts (list[dict]): list of products-listing pages dictionaries.
        new_urls_folder_path (str): path of the directory in which the URLs will be saved.
    """

    save_products_listing_brands_page_data = \
        save_products_listing_page_data_functions_dict['brands']
    save_products_listing_categories_page_data = \
        save_products_listing_page_data_functions_dict['categories']
    save_products_listing_search_keywords_page_data = \
        save_products_listing_page_data_functions_dict['search_keywords']

    for products_listing_page_dict in products_listing_pages_dicts:
        # Get a random user agent
        driver_dict['options'].add_argument(f'user-agent={get_random_user_agent()}')
        
        # Set the driver
        if driver_dict['use_driver']:
            if driver_dict['headless']:
                driver_dict['options'].add_argument("--headless=new")
            # Set the driver
            if driver_dict['use_proxy']:
                # Set the options for seleniumwire
                seleniumwire_options = {'proxy': {'https': driver_dict['proxy_url'], 'verify_ssl': False}}
                driver = sw_webdriver.Chrome(
                    driver_dict['driver_path'], 
                    options=driver_dict['options'], 
                    seleniumwire_options=seleniumwire_options)
            else:
                service = Service(executable_path=driver_dict['driver_path'])
                driver = webdriver.Chrome(service=service, options=driver_dict['options'])
        else:
            driver = False

        # Collect and save new URLs data
        if products_listing_page_dict['origin'] == 'brands':
            print("[LOG] Collect products-listing brands page data.")
            save_products_listing_brands_page_data(driver=driver,
                                                   source_dict=source_dict,
                                                   products_listing_page_dict=products_listing_page_dict,
                                                   new_urls_folder_path=new_urls_folder_path)

        elif products_listing_page_dict['origin'] == 'categories':
            print("[LOG] Collect products-listing categories page data.")
            save_products_listing_categories_page_data(driver=driver,
                                                       source_dict=source_dict,
                                                       products_listing_page_dict=products_listing_page_dict,
                                                       new_urls_folder_path=new_urls_folder_path)
            
        elif products_listing_page_dict['origin'] == 'search_keywords':
            print("[LOG] Collect products-listing search keywords page data.")
            save_products_listing_search_keywords_page_data(driver=driver,
                                                            source_dict=source_dict,
                                                            products_listing_page_dict=products_listing_page_dict,
                                                            new_urls_folder_path=new_urls_folder_path)
            
        # Quit the driver
        if driver:
            quit_driver(driver=driver, delete_cookies=driver_dict['delete_cookies'])


def collect_page(save_product_page_data,
                 driver_dict, 
                 source_dict,
                 product_page_dict,
                 n_max_reviews, 
                 min_date_year,
                 products_folder_path, 
                 reviews_folder_path,
                 reviews_dict_api_key):
    """Collect product data and reviews data from product page.

    Args:
        save_product_page_data (function): function to save product page data.
        driver_dict (dict): dictionary with information of the driver.
        source_dict (dict): dictionary with information from the source.
        product_page_dict (str): product page dict.
        n_max_reviews (int): max number of reviews to collect.
        min_date_year (int): oldest review year to collect.
        products_folder_path (str): path to the 'products' folder.
        reviews_folder_path (str): path to the 'reviews' folder.  
        reviews_dict_api_key (str): The API key allowing access to the reviews data.
    """

    # Set the driver
    if driver_dict['headless']:
        driver_dict['options'].add_argument("--headless=new")

    # Get a random user agent
    driver_dict['options'].add_argument(f'user-agent={get_random_user_agent()}')

    if driver_dict['use_proxy']:
        # Set the options for seleniumwire
        seleniumwire_options = {'proxy': {'https': driver_dict['proxy_url'], 'verify_ssl': False}}
        driver = sw_webdriver.Chrome(
            driver_dict['driver_path'], 
            options=driver_dict['options'], 
            seleniumwire_options=seleniumwire_options)
    else:
        service = Service(executable_path=driver_dict['driver_path'])
        driver = webdriver.Chrome(service=service, options=driver_dict['options'])

    # Collect the product and reviews data
    save_product_page_data(driver=driver, 
                           source_dict=source_dict, 
                           product_page_dict=product_page_dict, 
                           n_max_reviews=n_max_reviews,
                           min_date_year=min_date_year,
                           products_folder_path=products_folder_path, 
                           reviews_folder_path=reviews_folder_path,
                           reviews_dict_api_key=reviews_dict_api_key,
                           proxy_url=driver_dict['proxy_url'])
    
    # Quit the driver
    quit_driver(driver=driver, delete_cookies=driver_dict['delete_cookies'])


def collect_product_page(save_product_page_data,
                         driver_dict, 
                         source_dict,
                         product_page_dict,
                         products_folder_path):
    """Collect product data from product page.

    Args:
        save_product_page_data (function): function to save product page data.
        driver_dict (dict): dictionary with information of the driver.
        source_dict (dict): dictionary with information from the source.
        product_page_dict (str): product page dict.
        products_folder_path (str): path to the 'products' folder.
        
    Returns:
        dict, Dictionary with product data.
    """

    # Set the driver
    if driver_dict['use_driver']:
        if driver_dict['headless']:
            driver_dict['options'].add_argument("--headless=new")
        if driver_dict['use_proxy']:
            # Set the options for seleniumwire
            seleniumwire_options = {'proxy': {'https': driver_dict['proxy_url'], 'verify_ssl': False}}
            driver = sw_webdriver.Chrome(
                driver_dict['driver_path'], 
                options=driver_dict['options'], 
                seleniumwire_options=seleniumwire_options)
        else:
            service = Service(executable_path=driver_dict['driver_path'])
            driver = webdriver.Chrome(service=service, options=driver_dict['options'])
    else:
        driver = False

    # Collect the product and reviews data
    product_dict = \
        save_product_page_data(driver=driver, 
                               source_dict=source_dict, 
                               product_page_dict=product_page_dict, 
                               products_folder_path=products_folder_path)
    
    # Quit the driver
    if driver:
        quit_driver(driver=driver, delete_cookies=driver_dict['delete_cookies'])

    return product_dict


def collect_reviews_page(save_reviews_page_data,
                         driver_dict, 
                         source_dict,
                         product_dict,
                         reviews_page_dict,
                         n_max_reviews, 
                         min_date_year,
                         reviews_folder_path):
    """Collect product data and reviews data from product page.

    Args:
        save_product_page_data (function): function to save product page data.
        driver_dict (dict): dictionary with information of the driver.
        source_dict (dict): dictionary with information from the source.
        product_dict (str): product page dictionary.
        reviews_page_dict (str): reviews page dictionary.
        n_max_reviews (int): max number of reviews to collect.
        min_date_year (int): oldest review year to collect.
        reviews_folder_path (str): path to the 'reviews' folder.

    Returns:
        tuple[list[dict], int],
            list[dict]: List of reviews dictionaries.
            int: Number of reviews in the reviews dictionaries.
    """

    # Set the driver
    if driver_dict['use_driver']:
        if driver_dict['headless']:
            driver_dict['options'].add_argument("--headless=new")
        if driver_dict['use_proxy']:
            # Set the options for seleniumwire
            seleniumwire_options = {'proxy': {'https': driver_dict['proxy_url'], 'verify_ssl': False}}
            driver = sw_webdriver.Chrome(
                driver_dict['driver_path'], 
                options=driver_dict['options'], 
                seleniumwire_options=seleniumwire_options)
        else:
            service = Service(executable_path=driver_dict['driver_path'])
            driver = webdriver.Chrome(service=service, options=driver_dict['options'])
    else:
        driver = False

    # Collect the reviews data
    reviews_dicts = \
        save_reviews_page_data(
            driver=driver, 
            source_dict=source_dict,
            product_dict=product_dict, 
            reviews_page_dict=reviews_page_dict,
            n_max_reviews=n_max_reviews, 
            min_date_year=min_date_year,
            reviews_folder_path=reviews_folder_path)
    
    # Quit the driver
    if driver:
        quit_driver(driver=driver, delete_cookies=driver_dict['delete_cookies'])
    
    return reviews_dicts, len(reviews_dicts)


def collect_pages(save_product_page_data, 
                  driver_dict, 
                  source_dict, 
                  urls_to_collect_dicts_object_name, 
                  urls_to_collect_status, 
                  n_max_reviews, 
                  min_date_year, 
                  products_folder_path, 
                  reviews_folder_path,
                  reviews_dict_api_key):
    """Collects the data from URLs to collect.

    Args:
        save_product_page_data (function): function used for saving product page data.
        driver_dict (dict): dictionary with information of the driver.
        source_dict (dict): dictionary with information from the source.
        urls_to_collect_dicts_object_name (str): URLs to collect object name.
        urls_to_collect_status (str): status of the URLs to collect.
        n_max_reviews (int): max number of reviews to collect.
        min_date_year (int): oldest review year to collect.
        products_folder_path (str): Path to the 'products' folder.
        reviews_folder_path (str): Path to the 'reviews' folder.
        reviews_dict_api_key (str): The API key allowing access to the reviews data.
    """

    # Load the most recent URLs to collect object name
    urls_to_collect_dicts = json.load(
        open(urls_to_collect_dicts_object_name, 'r', encoding='utf-8'))

    for url_to_collect_dict in urls_to_collect_dicts:
        if url_to_collect_dict['collected'] == urls_to_collect_status:

            # Get a random user agent
            driver_dict['options'].add_argument(f'user-agent={get_random_user_agent()}')

            # Set the driver
            if driver_dict['headless']:
                driver_dict['options'].add_argument("--headless=new")

            if driver_dict['use_proxy']:
            # Set the options for seleniumwire
                seleniumwire_options = {'proxy': {'https': driver_dict['proxy_url'], 'verify_ssl': False}}
                driver = sw_webdriver.Chrome(
                    driver_dict['driver_path'], 
                    options=driver_dict['options'], 
                    seleniumwire_options=seleniumwire_options)
            else:
                service = Service(executable_path=driver_dict['driver_path'])
                driver = webdriver.Chrome(service=service, options=driver_dict['options'])
                
            print(f"[LOG] Time: {time.strftime('%H:%M:%S')}")

            try:
                # Collect and save the product and reviews data
                # --------------------------------------------------------
                product_dict, n_saved_reviews = save_product_page_data(
                    driver=driver,
                    source_dict=source_dict,
                    product_page_dict=url_to_collect_dict,
                    products_folder_path=products_folder_path,
                    reviews_folder_path=reviews_folder_path,
                    n_max_reviews=n_max_reviews,
                    min_date_year=min_date_year,
                    reviews_dict_api_key=reviews_dict_api_key,
                    proxy_url=driver_dict['proxy_url']
                )

                # Change the status of the URL to collect
                # --------------------------------------------------------
                # Step 1
                # ** What: product data has been collected
                # ** How: 'product_dict' is not empty
                if product_dict:

                    # Step 2
                    # ** What: product data contains the mandatory fields
                    # ** How: the fields 'product_name' and 'product_brand' aren't None
                    if product_dict['product_name'] is not None and \
                       product_dict['product_brand'] is not None:

                        # Step 3
                        # ** What: product data has the field 'n_reviews'
                        # The number of reviews for the product is displayed on the product page
                        # and has been saved
                        # ** How: the field 'n_reviews' is in the 'product_dict' and the value
                        # is not None
                        if product_dict.get('n_reviews') and \
                           product_dict['n_reviews'] is not None:
                                
                                # Step 5
                                # ** What: the number of reviews for the product is displayed on the product page
                                # and has been saved in the field 'n_reviews' in the correct integer type
                                # ** How: the field 'n_reviews' in 'product_dict' is an integer
                                if isinstance(product_dict['n_reviews'], int):
                                
                                    # Step 6
                                    # ** What: the number of reviews on the product page has been saved
                                    # in the correct integer type and the product has reviews to collect
                                    # ** How: the field 'n_reviews' is strictly higher than 0
                                    if product_dict['n_reviews'] > 0:

                                        # Step 10
                                        # ** What: some reviews have been saved
                                        # ** How: `n_saved_reviews` is strictly higher than 0
                                        if n_saved_reviews > 0:

                                            # Step 11
                                            # ** What: the number of saved reviews is higher or equal to the number of displayed 
                                            # reviews on the product page
                                            # All the reviews available on the product page have been collected
                                            # ** How: `n_saved_reviews` is higher or equal than the field 'n_reviews' in the 'product_dict'
                                            # ** URL status: the current URL is saved as 'yes'
                                            if n_saved_reviews >= product_dict['n_reviews']:
                                                url_to_collect_dict['collected'] = 'yes'
                                                print("[LOG] [Step 11] All the reviews have been collected for the product.\n"
                                                      "[LOG] [Step 11] The current URL is saved as 'yes'.")

                                            # Step 11 (if not)
                                            # ** What: the number of saved reviews is lower than the number of displayed 
                                            # reviews on the product page
                                            # Not all the reviews available on the product page have been collected
                                            # ** How: `n_saved_reviews` is strictly lower than the field 'n_reviews' in the 'product_dict'
                                            # ** URL status: the current URL is saved as 'once'
                                            else:
                                                url_to_collect_dict['collected'] = 'once'
                                                print("[LOG] [Step 11 (if not)] Not all the reviews have been collected for the product.\n"
                                                      "[LOG] [Step 11 (if not)] Or the product has ratings without text.\n"
                                                      "[LOG] [Step 11 (if not)] The current URL is saved as 'once'.")                                      

                                        # Step 10 (if not)
                                        # ** What: no reviews have been saved
                                        # The product page displayed the product has reviews and the field
                                        # 'n_reviews' in the 'product_dict' has been correctly saved as a strictly
                                        # positive integer
                                        # There has been an issue with the reviews data collection
                                        # ** URL status: the current URL is saved as 'issue'
                                        else:
                                            url_to_collect_dict['collected'] = 'issue'
                                            print("[LOG] [Step 10 (if not)] There has been an issue with the current URL.\n"
                                                  "[LOG] [Step 10 (if not)] The current URL is saved as 'issue'.")

                                    # Step 6 (elif)
                                    # ** What: the number of reviews on the product page has been saved
                                    # in the correct integer type but the product hasn't any reviews to collect
                                    # ** How: the field 'n_reviews' is equal to 0 
                                    elif product_dict['n_reviews'] == 0:

                                        # Step 7
                                        # ** What: some reviews have been saved 
                                        # The number of saved reviews can't be compared with the number of reviews 
                                        # for the product because the information is displayed on the product page 
                                        # but has been saved as a null integer
                                        # There has been a problem with the product data collection
                                        # ** URL status: the current URL is saved as 'issue'
                                        if n_saved_reviews > 0:
                                            url_to_collect_dict['collected'] = 'issue'
                                            print("[LOG] [Step 7] There has been an issue with the current URL.\n"
                                                  "[LOG] [Step 7] The current URL is saved as 'issue'.")
                                            
                                        # Step 7 (if not)
                                        # ** What: no reviews have been saved
                                        # There aren't any saved reviews but the number of displayed reviews isn't correctly saved
                                        # There has been a problem with the product data collection
                                        # There has been a problem with the reviews data collecttion because 
                                        # the product is supposed to have reviews                                        
                                        # The current URL is saved as 'issue'
                                        else:
                                            url_to_collect_dict['collected'] = 'issue'
                                            print("[LOG] [Step 7 (if not)] There has been an issue with the current URL.\n"
                                                  "[LOG] [Step 7 (if not)] The current URL is saved as 'issue'.")
                                                                                
                                    # Step 6 (else)
                                    # ** What: The number of reviews on the product page has been saved
                                    # in the correct integer type but the product hasn't any reviews to collect
                                    # ** How: the field 'n_reviews' is lower than 0 
                                    else:

                                        # Step 8
                                        # ** What: some reviews have been saved 
                                        # The number of saved reviews can't be compared with the number of reviews 
                                        # for the product because the information is displayed on the product page 
                                        # but hasn't been saved correctly as a positive or null integer
                                        # It is impossible to know if all the reviews have been saved
                                        # ** How: `n_saved_reviews` is higher than 0
                                        # ** URL status: The current URL is saved as 'once'
                                        if n_saved_reviews > 0:
                                            url_to_collect_dict['collected'] = 'once'
                                            print("[LOG] [Step 8] Not all the reviews have been collected for the product.\n"
                                                  "[LOG] [Step 8] The current URL is saved as 'once'.") 

                                        # Step 9 (if not)
                                        # What: no reviews have been saved
                                        # There aren't any saved reviews but the number of displayed reviews is 
                                        # accessible on the product page and has been saved in the correct integer format
                                        # There has been a problem with the product data collection because 
                                        # the number of reviews is not in the correct positive or null integer format
                                        # There has been a problem with the reviews data collecttion because 
                                        # the product is supposed to have reviews
                                        # ** How: `n_saved_reviews` is equal to 0
                                        # ** URL status: The current URL is saved as 'issue'
                                        else:
                                            url_to_collect_dict['collected'] = 'issue'
                                            print("[LOG] [Step 9 (if not)] There has been an issue with the current URL.\n"
                                                  "[LOG] [Step 9 (if not)] The current URL is saved as 'issue'.")

                                # Step 5 (if not)
                                # ** What: the number of reviews for the product is displayed on the product page
                                # and has been saved in the field 'n_reviews' but the type isn't correct
                                # There has been a problem with the product data collection or the conversion of the
                                # field 'n_reviews' to integer                                
                                # How: the field 'n_reviews' in 'product_dict' isn't an integer         
                                else:

                                    # Step 12
                                    # ** What: some reviews have been saved 
                                    # The number of saved reviews can't be compare with the number of reviews for 
                                    # the product because the information is displayed on the product page 
                                    # but hasn't been saved correctly in the type integer
                                    # It is impossible to know if all the reviews have been saved
                                    # ** How: `n_saved_reviews` is higher than 0
                                    # ** URL status: The current URL is saved as 'once'
                                    if n_saved_reviews > 0:
                                        url_to_collect_dict['collected'] = 'once'
                                        print("[LOG] [Step 12] Not all the reviews have been collected for the product.\n"
                                              "[LOG] [Step 12] The current URL is saved as 'once'.")

                                    # Step 12 (if not)
                                    # What: no reviews have been saved
                                    # There aren't any saved reviews but the number of displayed reviews is accessible 
                                    # on the product page
                                    # There has been a problem with the product data collection because the number 
                                    # of reviews hasn't been in the correct integer type
                                    # And product is supposed to have reviews, so the number of saved reviews should be
                                    # higher than 0
                                    # ** How: `n_saved_reviews` is equal to 0
                                    # ** URL status: The current URL is saved as 'issue'
                                    else:
                                        url_to_collect_dict['collected'] = 'issue'
                                        print("[LOG] [Step 12 (if not)] There has been an issue with the current URL.\n"
                                              "[LOG] [Step 12 (if not)] The current URL is saved as 'issue'.")     
                                                                                                    
                        # Step 3 (if not)
                        # ** What: product data doesn't contain the field 'n_reviews' or hasn't been able
                        # to point to the information in the product page
                        # The number of reviews for the product isn't displayed on the product page or hasn't been
                        # successfully saved
                        # ** How: the field 'n_reviews' isn't in the 'product_dict'
                        else:
                            
                            # Step 4
                            # ** What: some reviews have been saved 
                            # The number of saved reviews can't be compared with the number of 
                            # reviews for the product because the information isn't displayed 
                            # on the product page
                            # It is impossible to know if all the reviews have been saved
                            # ** How: `n_saved_reviews` is higher than 0
                            # ** URL status: The current URL is saved as 'once'
                            if n_saved_reviews > 0:
                                url_to_collect_dict['collected'] = 'once'
                                print("[LOG] [Step 4] Not all the reviews have been collected for the product.\n"
                                      "[LOG] [Step 4] The current URL is saved as 'once'.")
                                
                            # Step 4 (if not)
                            # What: no reviews have been saved
                            # There aren't any saved reviews and the number of displayed reviews isn't 
                            # accessible on the product page
                            # The product hasn't any reviews
                            # ** How: `n_saved_reviews` is equal to 0
                            # ** URL status: The current URL is saved as 'yes'
                            else:
                                url_to_collect_dict['collected'] = 'yes'
                                print("[LOG] [Step 4 (if not)] All the reviews have been collected for the product.\n"
                                      "[LOG] [Step 4 (if not)] The current URL is saved as 'yes'.")
                                
                    # Step 2 (if not)
                    # ** What: product data doesn't contain the mandatory fields
                    # The fields 'product_name' and 'product_brand' are both None
                    # There has been a problem with the product data collection
                    # ** How: one of the fields 'product_name' or 'product_brand' is None
                    # ** URL status: the current URL is saved as 'issue'
                    else:
                        url_to_collect_dict['collected'] = 'issue'
                        print("[LOG] [Step 2 (if not)] There has been an issue with the current URL.\n"
                              "[LOG] [Step 2 (if not)] The current URL is saved as 'issue'.")
                        
                # Step 1 (if not)
                # ** What: product data hasn't been collected
                # There has been a problem with the product data collection
                # ** How: 'product_dict' is empty
                # ** URL status: the current URL is saved as a 'issue'
                else:
                    url_to_collect_dict['collected'] = 'issue'
                    print("[LOG] [Step 1 (if not)] There has been an issue with the current URL.\n"
                          "[LOG] [Step 1 (if not)] The current URL is saved as 'issue'.")
                    
            # Errors
            # --------------------------------------------------------
            # The collect for the current URL has raised an error so the current URL is saved as a 'issue'
            except:
                url_to_collect_dict['collected'] = 'issue'
                print("[LOG] [Errors] There has been an issue with the current URL.\n"
                      "[LOG] [Errors] The current URL is saved as 'issue'.")

            finally:
                with open(urls_to_collect_dicts_object_name, 
                          'w', encoding='utf-8') as file_to_dump:
                    json.dump(urls_to_collect_dicts, file_to_dump, indent=4, ensure_ascii=False)
    
            # Quit the driver
            quit_driver(driver=driver, delete_cookies=driver_dict['delete_cookies'])


def define_key_prospected_state(url_to_collect_dict):
    """Defines the prospected key state.

    Args:
        url_to_collect_dict (dict): products and reviews URLs 
                                    to collect dictionary.

    Returns:
        str, Prospected state.
    """

    # According to product URL
    if url_to_collect_dict['product_url']['collected'] == 'issue':
        return 'issue'
    elif url_to_collect_dict['product_url']['collected'] == 'no':
        return 'no'
    elif url_to_collect_dict['product_url']['collected'] == 'yes':
        # According to reviews URLs
        n_yes = 0
        n_no = 0
        n_issue = 0
        for reviews_url in url_to_collect_dict['reviews_urls']:
            if reviews_url['collected'] == 'yes':
                n_yes = n_yes + 1
            elif reviews_url['collected'] == 'no':
                n_no = n_no + 1
            elif reviews_url['collected'] == 'issue':
                n_issue = n_issue + 1

        if n_issue == 0 and n_yes > 0:
            if n_yes == len(url_to_collect_dict['reviews_urls']):
                return 'yes'
            elif n_yes < len(url_to_collect_dict['reviews_urls']):
                return 'once'
        elif n_issue > 0:
            return 'issue'
        else:
            return 'issue'


def collect_products_and_reviews_pages(save_product_page_data,
                                       save_reviews_page_data,
                                       driver_dict, 
                                       source_dict, 
                                       urls_to_collect_dicts_object_name, 
                                       prospected_urls_to_collect_status,
                                       reviews_urls_to_collect_status,
                                       n_reviews_per_page,
                                       n_max_reviews, 
                                       min_date_year, 
                                       products_folder_path, 
                                       reviews_folder_path,
                                       proxy_configuration):
    """Collects the data from URLs to collect.

    Args:
        save_product_page_data (function): function used for saving product page data.
        save_reviews_page_data (function): function used for saving reviews page data.
        driver_dict (dict): dictionary with information of the driver.
        source_dict (dict): dictionary with information from the source.
        urls_to_collect_dicts_object_name (str): URLs to collect dictionaries object name.
        prospected_urls_to_collect_status (str): status of the URLs to collect prospected key.
        reviews_urls_to_collect_status (str): status of the URLs to collect collected key.
        n_reviews_per_page (int): number of reviews per page.
        n_max_reviews (int): max number of reviews to collect.
        min_date_year (int): oldest review year to collect.
        products_folder_path (str): Path to the 'products' folder.
        reviews_folder_path (str): Path to the 'reviews' folder.
        
    """

    try:
        # Load the most recent URLs to collect object name
        urls_to_collect_dicts = json.load(
            open(urls_to_collect_dicts_object_name, 'r', encoding='utf-8'))

        for url_to_collect_dict in urls_to_collect_dicts:
            if url_to_collect_dict['prospected'] == \
                prospected_urls_to_collect_status:

                print(f"[LOG] [collect_pages.py] Time: {time.strftime('%H:%M:%S')}")

                # >>> Product part <<<
                print("[LOG] [collect_pages.py] >>> Product part <<<")
                # Collect and save the product data
                # --------------------------------------------------------
                product_dict = \
                    collect_product_page(save_product_page_data=save_product_page_data,
                                         driver_dict=driver_dict, 
                                         source_dict=source_dict,
                                         product_page_dict=url_to_collect_dict['product_url'],
                                         products_folder_path=products_folder_path,
                                         proxy_configuration=proxy_configuration)

                # Change the status of the product URL to collect
                # --------------------------------------------------------
                # Step 1
                # ** What: product data has been collected
                # ** How: 'product_dict' is not empty
                if product_dict:

                    # Step 2
                    # ** What: product data contains the mandatory fields
                    # ** How: the fields 'product_name' and 'product_brand' aren't None
                    if product_dict['product_name'] is not None and \
                        product_dict['product_brand'] is not None:

                        # Step 3
                        # ** What: product data has the field 'n_reviews'
                        # The number of reviews for the product is displayed on the product page
                        # and has been saved
                        # ** How: the field 'n_reviews' is in the 'product_dict' and the value
                        # is not None
                        if product_dict.get('n_reviews') and \
                            product_dict['n_reviews'] is not None:
                                
                                # Step 4
                                # ** What: the number of reviews for the product is displayed on the product page
                                # and has been saved in the field 'n_reviews' in the correct integer type
                                # ** How: the field 'n_reviews' in 'product_dict' is an integer
                                if isinstance(product_dict['n_reviews'], int):
                                
                                    # Step 5
                                    # ** What: the number of reviews on the product page has been saved
                                    # in the correct integer type and the product has reviews to collect
                                    # ** How: the field 'n_reviews' is strictly higher than 0
                                    # ** URL status: the current URL is saved as 'yes'
                                    if product_dict['n_reviews'] > 0:
                                        url_to_collect_dict['product_url']['collected'] = 'yes'
                                        print(\
                                            "[LOG] [collect_pages.py] [Step 5] All the reviews have been collected for the product.\n"
                                            "[LOG] [collect_pages.py] [Step 5] The current product URL is saved as 'yes'.")
                                                                                
                                    # Step 5 (if not)
                                    # ** What: the number of collected reviews is equal to 0 so there aren't
                                    # any reviews to collect.
                                    # ** How: the field 'n_reviews' is 0
                                    # ** URL status: the current URL is saved as 'issue'
                                    else:
                                        url_to_collect_dict['product_url']['collected'] = 'issue'
                                        print(\
                                            "[LOG] [collect_pages.py] [Step 5 (if not)] The dictionary 'product_dict' has the attribute 'n_reviews' to int(0).\n"
                                            "[LOG] [collect_pages.py] [Step 5 (if not)] There has been an issue with the current URL.\n"
                                            "[LOG] [collect_pages.py] [Step 5 (if not)] The current product URL is saved as 'issue'.")

                                # Step 4 (if not)   
                                # ** What: the number of reviews for the product is displayed on the product page
                                # and has been saved in the field 'n_reviews' but the type isn't correct
                                # There has been a problem with the product data collection or the conversion of the
                                # field 'n_reviews' to integer                                
                                # How: the field 'n_reviews' in 'product_dict' isn't an integer       
                                # ** URL status: the current URL is saved as 'issue'  
                                else:
                                    url_to_collect_dict['product_url']['collected'] = 'issue'
                                    print(\
                                        "[LOG] [collect_pages.py] [Step 4 (if not)] The dictionary 'product_dict' hasn't the attribute 'n_reviews' as int.\n"
                                        "[LOG] [collect_pages.py] [Step 4 (if not)] There has been an issue with the current URL.\n"
                                        "[LOG] [collect_pages.py] [Step 4 (if not)] The current URL is saved as 'issue'.")     
                                                            
                        # Step 3 (if not)
                        # ** What: product data doesn't contain the field 'n_reviews' or hasn't been able
                        # to point to the information in the product page
                        # The number of reviews for the product isn't displayed on the product page or hasn't been
                        # successfully saved
                        # ** How: the field 'n_reviews' isn't in the 'product_dict'
                        # ** URL status: the current URL is saved as 'issue'
                        else:
                            url_to_collect_dict['product_url']['collected'] = 'issue'
                            print(\
                                "[LOG] [collect_pages.py] [Step 3 (if not)] The dictionary 'product_dict' hasn't the attribute 'n_reviews'.\n"
                                "[LOG] [collect_pages.py] [Step 3 (if not)] There has been an issue with the current URL.\n"
                                "[LOG] [collect_pages.py] [Step 3 (if not)] The current URL is saved as 'issue'.")
                                
                    # Step 2 (if not)
                    # ** What: product data doesn't contain the mandatory fields
                    # The fields 'product_name' and 'product_brand' are both None
                    # There has been a problem with the product data collection
                    # ** How: one of the fields 'product_name' or 'product_brand' is None
                    # ** URL status: the current URL is saved as 'issue'
                    else:
                        url_to_collect_dict['product_url']['collected'] = 'issue'
                        print(\
                            "[LOG] [collect_pages.py] [Step 2 (if not)] The dictionary 'product_dict' hasn't the attributes 'product_name' or 'product_brand'.\n"
                            "[LOG] [collect_pages.py] [Step 2 (if not)] There has been an issue with the current URL.\n"
                            "[LOG] [collect_pages.py] [Step 2 (if not)] The current URL is saved as 'issue'.")
                        
                # Step 1 (if not)
                # ** What: product data hasn't been collected
                # There has been a problem with the product data collection
                # ** How: 'product_dict' is empty
                # ** URL status: the current URL is saved as a 'issue'
                else:
                    url_to_collect_dict['product_url']['collected'] = 'issue'
                    print(\
                        "[LOG] [collect_pages.py] [Step 1 (if not)] The dictionary 'product_dict' is empty.\n"
                        "[LOG] [collect_pages.py] [Step 1 (if not)] There has been an issue with the current URL.\n"
                        "[LOG] [collect_pages.py] [Step 1 (if not)] The current URL is saved as 'issue'.")
                    
                # Save the status of the product URL to collect
                # --------------------------------------------------------
                print("[LOG] [collect_pages.py] Saving product URL key in 'urls_to_collect_dicts_object_name' file...")    
                with open(urls_to_collect_dicts_object_name, 
                          'w', encoding='utf-8') as file_to_dump:
                    json.dump(urls_to_collect_dicts, file_to_dump, indent=4, ensure_ascii=False)
                print("[LOG] [collect_pages.py] 'urls_to_collect_dicts_object_name' has been saved.")

                # >>> Reviews part <<<
                if n_reviews_per_page:
                    # Set max number of pages to collect
                    n_max_pages_to_collect = n_pages(n_reviews=n_max_reviews, 
                                                     n_reviews_per_page=n_reviews_per_page)
                    
                    print("[LOG] [collect_pages.py] >>> Reviews part <<<")
                    n_current_reviews_page = 1

                    if url_to_collect_dict['product_url']['collected'] == 'yes':
                        for reviews_url_id in range(0, len(url_to_collect_dict['reviews_urls'])):
                            if url_to_collect_dict['reviews_urls'][reviews_url_id]['collected'] == \
                                reviews_urls_to_collect_status:

                                print(f"[LOG] [collect_pages.py] Time: {time.strftime('%H:%M:%S')}")
                                
                                # Collect and save the reviews data
                                # --------------------------------------------------------
                                _, n_saved_reviews = \
                                    collect_reviews_page(save_reviews_page_data=save_reviews_page_data,
                                                         driver_dict=driver_dict, 
                                                         source_dict=source_dict,
                                                         product_dict=product_dict,
                                                         reviews_page_dict=url_to_collect_dict['reviews_urls'][reviews_url_id],
                                                         n_max_reviews=n_max_reviews, 
                                                         min_date_year=min_date_year,
                                                         reviews_folder_path=reviews_folder_path,
                                                         proxy_configuration=proxy_configuration)

                                # Change the status of the reviews URL to collect
                                # --------------------------------------------------------
                                # Step 8
                                # ** What: all the reviews have been collected
                                # ** How: the number of collected reviews is equal to the number of reviews
                                # per page
                                # ** URL status: The current reviews URL is saved as 'yes'
                                if n_saved_reviews == n_reviews_per_page:
                                    url_to_collect_dict['reviews_urls'][reviews_url_id]['collected'] = 'yes'
                                    print(
                                        "[LOG] [collect_pages.py] [Step 8] All reviews have been collected on the current reviews URL.\n"
                                        "[LOG] [collect_pages.py] [Step 8] The current reviews URL is saved as 'yes'.")

                                # Step 8 (elif)
                                # ** What: reviews have been collected on the reviews URL
                                # ** How: the number of collected reviews is higher than 0 and lower to the 
                                # number of reviews per page. It happens on the last reviews URL
                                # ** URL status: The current reviews URL is saved as 'yes'
                                elif n_saved_reviews > 0 and n_saved_reviews < n_reviews_per_page:
                                    url_to_collect_dict['reviews_urls'][reviews_url_id]['collected'] = 'yes'
                                    print(
                                        "[LOG] [collect_pages.py] [Step 8 (elif)] Reviews have been collected on the current reviews URL.\n"
                                        "[LOG] [collect_pages.py] [Step 8 (elif)] The current reviews URL is saved as 'yes'.")

                                # Step 8 (else)
                                # ** What: no reviews have been collected on the reviews URL
                                # ** How: the number of collected reviews is equal to 0
                                # ** URL status: The current reviews URL is saved as 'no'
                                else:
                                    url_to_collect_dict['reviews_urls'][reviews_url_id]['collected'] = 'no'
                                    print(
                                        "[LOG] [collect_pages.py] [Step 8 (else)] No reviews have been collected for the reviews page URL.\n"
                                        "[LOG] [collect_pages.py] [Step 8 (else)] The current reviews URL is saved as 'no'.")
                                
                                # Save the status of the reviews URL to collect
                                # --------------------------------------------------------
                                print("[LOG] [collect_pages.py] Saving reviews URL key in the 'urls_to_collect_dicts_object_name' file...")
                                with open(urls_to_collect_dicts_object_name, 
                                        'w', encoding='utf-8') as file_to_dump:
                                    json.dump(urls_to_collect_dicts, file_to_dump, indent=4, ensure_ascii=False)
                                print("[LOG] [collect_pages.py] 'urls_to_collect_dicts_object_name' has been saved.")
                            
                            if n_max_reviews:
                                if n_current_reviews_page >= n_max_pages_to_collect:
                                    print(
                                        "[LOG] [collect_pages.py] Reached the max number of pages to collect.\n"
                                        "[LOG] [collect_pages.py] Go to the prospected key management status.")
                                    break

                            # Go to the next reviews URL
                            n_current_reviews_page = n_current_reviews_page + 1

                    # >>> Key prospected part <<<
                    # Change the status of the prospected key for the product
                    # --------------------------------------------------------
                    print("[LOG] [collect_pages.py] >>> Prospected key part <<<")
                    url_to_collect_dict['prospected'] = \
                        define_key_prospected_state(url_to_collect_dict=url_to_collect_dict)
                    
                    # Step 9
                    # ** What: All the reviews URLs have been collected
                    # ** URL status: the prospected key is saved as 'yes'
                    if url_to_collect_dict['prospected'] == 'yes':
                        print(
                            "[LOG] [collect_pages.py] [Step 9] All reviews URLs have been collected for the current product URL.\n"
                            "[LOG] [collect_pages.py] [Step 9] The prospected key is set to 'yes'.")

                    # Step 9 (elif)
                    # ** What: Not all the reviews URLs have been collected
                    # ** URL status: the prospected key is saved as 'once'
                    elif url_to_collect_dict['prospected'] == 'once':
                        print(
                            "[LOG] [collect_pages.py] [Step 9 (elif)] Not all reviews URLs have been collected for the current product URL.\n"
                            "[LOG] [collect_pages.py] [Step 9 (elif)] The prospected key is set to 'once'.")

                    # Step 9 (elif)
                    # ** What: There has been an issue during the collect
                    # ** URL status: the prospected key is saved as 'issue'
                    elif url_to_collect_dict['prospected'] == 'issue':
                        print(
                            "[LOG] [collect_pages.py] [Step 9 (elif)] There has been an issue.\n"
                            "[LOG] [collect_pages.py] [Step 9 (elif)] The prospected key is set as 'issue.")
                        
                    # Step 9 (else)
                    # ** What: There has been an issue during the collect
                    # ** URL status: the prospected key is saved as 'issue'
                    else:
                        print(
                            "[LOG] [collect_pages.py] [Step 9 (else)] There has been an issue.\n"
                            "[LOG] [collect_pages.py] [Step 9 (else)] The prospected key is set as 'issue.")

                    # Save the status of the prospected key
                    # --------------------------------------------------------    
                    print("[LOG] [collect_pages.py] Saving prospected key in the 'urls_to_collect_dicts_object_name' file...")
                    with open(urls_to_collect_dicts_object_name, 
                                'w', encoding='utf-8') as file_to_dump:
                        json.dump(urls_to_collect_dicts, file_to_dump, indent=4, ensure_ascii=False)
                    print("[LOG] [collect_pages.py] 'urls_to_collect_dicts_object_name' has been saved.")
                           
                else:
                    raise ValueError(
                        "[LOG] [collect_pages.py] The value `n_reviews_per_page` is not defined.")

    except ValueError as e:
        print(
            "[LOG] [collect_pages.py] [ValueError] The script has been stopped.\n"
            "[LOG] [collect_pages.py] [ValueError] Set the value `n_reviews_per_page` as an integer.\n"
            f"[LOG] [collect_pages.py] [ValueError]:\n{e}")

    except KeyboardInterrupt as e:
        print(
            "[LOG] [collect_pages.py] [KeyboardInterrupt] The collect has been interrupted by the user.\n"
            f"[LOG] [collect_pages.py] [KeyboardInterrupt]:\n{e}")

    except Exception as e:
        print(
            "[LOG] [collect_pages.py] [Exception] There has been an error during the collect.\n"
            f"[LOG] [collect_pages.py] [Exception]:\n{e}")


def evaluate_collect_progression(urls_to_collect_object_name):
    """Evaluate the collect progression by displaying each key's number of occurences.
    
    Args:
        urls_to_collect_folder_path: urls_to_collect folder path.
        url_to_collect_file_name: url to collect file name to evaluate.    
    """

    current_day = datetime.datetime.today().strftime('%Y-%m-%d')
    print("[LOG] Start to evaluate collect progression.")
    print(f"[LOG] URLs to collect object name: {urls_to_collect_object_name}.")
    print(f"[LOG] Time: {current_day}")

    # Load the most recent URLs
    most_recent_urls_to_collect_dicts_object_name = urls_to_collect_object_name
    urls_to_collect_dicts = json.load(
        open(most_recent_urls_to_collect_dicts_object_name, 'r', encoding='utf-8'))

    n_urls_to_collect = len(urls_to_collect_dicts)

    # Get the number of URLs 'yes', 'once', 'issue' and 'no'
    n_status_yes = 0
    n_status_no = 0
    n_status_once = 0
    n_status_issue = 0
    for urls_to_collect_dict in urls_to_collect_dicts:
        url_status = urls_to_collect_dict['collected']
        if url_status == 'yes':
            n_status_yes += 1
        elif url_status == 'no':
            n_status_no += 1
        elif url_status == 'once':
            n_status_once += 1
        elif url_status == 'issue':
            n_status_issue += 1

    # Define the width for alignment
    field_width_n_status = 5
    field_width_p_status = 3
    field_width_p_unit = 2

    print(f"[LOG] There are {n_urls_to_collect} URLs to collect.")
    print(f"[LOG] {str(n_status_yes).ljust(field_width_n_status)} "
          f"({str(round(100 * n_status_yes / n_urls_to_collect, 1)).ljust(field_width_p_status)}"
          f"{''.ljust(field_width_p_unit)} %) "
           "URLs with the status YES.")
    print(f"[LOG] {str(n_status_no).ljust(field_width_n_status)} "
          f"({str(round(100 * n_status_no / n_urls_to_collect, 1)).ljust(field_width_p_status)}"
          f"{''.ljust(field_width_p_unit)} %) "
           "URLs with the status NO.")
    print(f"[LOG] {str(n_status_once).ljust(field_width_n_status)} "
          f"({str(round(100 * n_status_once / n_urls_to_collect, 1)).ljust(field_width_p_status)}"
          f"{''.ljust(field_width_p_unit)} %) "
           "URLs with the status ONCE.")
    print(f"[LOG] {str(n_status_issue).ljust(field_width_n_status)} "
          f"({str(round(100 * n_status_issue / n_urls_to_collect, 1)).ljust(field_width_p_status)}"
          f"{''.ljust(field_width_p_unit)} %) "
           "URLs with the status ISSUE.")
    print("[LOG] Evaluated collect progression.")


def evaluate_products_and_reviews_collect_progression(urls_to_collect_object_name):
    """Evaluates the collect progression by displaying each key's number of occurences.
    
    Args:
        urls_to_collect_object_name (str): URLs to collect object name.
    """

    print(f"[LOG] Time: {time.strftime('%H:%M:%S')}")
    print("[LOG] Start to evaluate collect progression.")
    print(f"[LOG] URLs to collect object name: {urls_to_collect_object_name}.")

    # Load the most recent URLs to collect
    most_recent_urls_to_collect_dicts_object_name = urls_to_collect_object_name
    urls_to_collect_dicts = json.load(
        open(most_recent_urls_to_collect_dicts_object_name, 'r', encoding='utf-8'))

    n_urls_to_collect = len(urls_to_collect_dicts)
    n_reviews_page = 0
    
    # Get the number of URLs 'yes', 'once', 'issue' and 'no'
    # Prospected key
    n_prospected_yes = 0
    n_prospected_no = 0
    n_prospected_once = 0
    n_prospected_issue = 0
    # Collected key
    n_reviews_page_collected_yes = 0
    n_reviews_page_collected_no = 0
    n_reviews_page_collected_once = 0
    n_reviews_page_collected_issue = 0

    # {
    #     "prospected": "yes",
    #     "product_url": {
    #         "url": "https://www.beaute-test.com/cc-cream-chanel.php",
    #         "collected": "yes"
    #     },
    #     "reviews_urls": [
    #         {
    #             "url": "https://www.beaute-test.com/cc-cream-chanel.php?listeavis=1",
    #             "collected": "yes"
    #         },
    #         {
    #             "url": "https://www.beaute-test.com/cc-cream-chanel.php?listeavis=2",
    #             "collected": "yes"
    #         }
    #     ]
    # },

    for urls_to_collect_dict in urls_to_collect_dicts:
        # Prospected key
        if urls_to_collect_dict['prospected'] == 'yes':
            n_prospected_yes += 1
        elif urls_to_collect_dict['prospected'] == 'no':
            n_prospected_no += 1
        elif urls_to_collect_dict['prospected'] == 'once':
            n_prospected_once += 1
        elif urls_to_collect_dict['prospected'] == 'issue':
            n_prospected_issue += 1
        # Collected key
        for review_url in urls_to_collect_dict['reviews_urls']:
            n_reviews_page = n_reviews_page + 1
            if review_url['collected'] == 'yes':
                n_reviews_page_collected_yes += 1
            elif review_url['collected'] == 'no':
                n_reviews_page_collected_no += 1
            elif review_url['collected'] == 'once':
                n_reviews_page_collected_once += 1
            elif review_url['collected'] == 'issue':
                n_reviews_page_collected_issue += 1

    # Define the width for alignment
    field_width_n_status = 5
    field_width_p_status = 3
    field_width_p_unit = 2

    print(f"[LOG] There are {n_urls_to_collect} URLs to collect.")
    print(f"[LOG] {str(n_prospected_yes).ljust(field_width_n_status)} "
          f"({str(round(100 * n_prospected_yes / n_urls_to_collect, 1)).ljust(field_width_p_status)}"
          f"{''.ljust(field_width_p_unit)} %) "
           "URLs to collect with the prospected status YES.")
    print(f"[LOG] {str(n_prospected_no).ljust(field_width_n_status)} "
          f"({str(round(100 * n_prospected_no / n_urls_to_collect, 1)).ljust(field_width_p_status)}"
          f"{''.ljust(field_width_p_unit)} %) "
           "URLs to collect with the prospected status NO.")
    print(f"[LOG] {str(n_prospected_once).ljust(field_width_n_status)} "
          f"({str(round(100 * n_prospected_once / n_urls_to_collect, 1)).ljust(field_width_p_status)}"
          f"{''.ljust(field_width_p_unit)} %) "
           "URLs to collect with the prospected status ONCE.")
    print(f"[LOG] {str(n_prospected_issue).ljust(field_width_n_status)} "
          f"({str(round(100 * n_prospected_issue / n_urls_to_collect, 1)).ljust(field_width_p_status)}"
          f"{''.ljust(field_width_p_unit)} %) "
           "URLs to collect with the prospected status ISSUE.")
    
    print(f"[LOG] There are {n_reviews_page} reviews URLs to collect.")
    print(f"[LOG] {str(n_reviews_page_collected_yes).ljust(field_width_n_status)} "
          f"({str(round(100 * n_reviews_page_collected_yes / n_reviews_page, 1)).ljust(field_width_p_status)}"
          f"{''.ljust(field_width_p_unit)} %) "
           "reviews URLs to collect with the collected status YES.")
    print(f"[LOG] {str(n_reviews_page_collected_no).ljust(field_width_n_status)} "
          f"({str(round(100 * n_reviews_page_collected_no / n_reviews_page, 1)).ljust(field_width_p_status)}"
          f"{''.ljust(field_width_p_unit)} %) "
           "reviews URLs to collect with the collected status NO.")
    print(f"[LOG] {str(n_reviews_page_collected_once).ljust(field_width_n_status)} "
          f"({str(round(100 * n_reviews_page_collected_once / n_reviews_page, 1)).ljust(field_width_p_status)}"
          f"{''.ljust(field_width_p_unit)} %) "
           "reviews URLs to collect with the collected status ONCE.")
    print(f"[LOG] {str(n_reviews_page_collected_issue).ljust(field_width_n_status)} "
          f"({str(round(100 * n_reviews_page_collected_issue / n_reviews_page, 1)).ljust(field_width_p_status)}"
          f"{''.ljust(field_width_p_unit)} %) "
           "reviews URLs to collect with the collected status ISSUE.")

    print("[LOG] Evaluated collect progression.")
        