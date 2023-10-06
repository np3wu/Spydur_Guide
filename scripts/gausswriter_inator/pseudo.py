# -*- coding: utf-8 -*-
"""
pseudo.py is specifically made for scraping the website: 
https://www.tc.uni-koeln.de/PP/clickpse.en.html
However, There are some good functions for handling selenium Webdriver
that can be used in later projects
"""
# Credits
__author__ = 'Nam H. Pham'
__copyright__ = 'Copyright 2023'
__credits__ = None
__email__ = "nam.pham@richmond.edu"

# System imports
import sys
import os
import re
from urllib.parse import urljoin

#Multithreading
import concurrent.futures

# BeautifulSoup imports
import requests
from bs4 import BeautifulSoup

#Selenium Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# N-ary tree structures
from sloppytree import SloppyTree
from anytree import NodeMixin, RenderTree

# Data imports and exports
import json
import pickle
import csv
from anytree.exporter import JsonExporter
from anytree.importer import JsonImporter


######################################################################
# SCRAPING FUNCTIONS
######################################################################

def ECP_format_select(driver):
    """
    This function handles the dropdown menu for ECP format.
    Currently only chooses from Gaussian format. Needs to 
    be updated for other format
    """

    # Find the dropdown element by its name
    dropdown_element = driver.find_element(By.NAME, "ECPFormat")

    # Create a Select object from the dropdown element
    dropdown = Select(dropdown_element)

    # Check if the dropdown is enabled before interacting with it
    if dropdown_element.is_enabled():
        # Select an option from the dropdown by value
        desired_option_value = "gaussian"  # Change to the desired option value
        dropdown.select_by_value(desired_option_value)

        # Wait for the page to update after selecting the option
        wait = WebDriverWait(driver, 10)
        wait.until(EC.text_to_be_present_in_element_value((By.NAME, "ECPFormat"), desired_option_value))
        
def get_and_sort_urls(soup):
    """
    The main way to deal with links in the pop up window.
    Retrieves the url and the text of link
    """
    popup_url = "https://www.tc.uni-koeln.de"
    a_elements = soup.find("p", style="margin-left:24pt").find_all("a")
    
    url_dict = {}
    for a in a_elements:
        link = urljoin(popup_url, a["href"])
        name = a.get_text(strip=True)
        url_dict[name] = link
    
    print("links are scraped")
    return url_dict

def get_info(url):
    """
    Getting the desired information. The data should be
    stored for later use in a separate file
    """

    print(f"Start scraping {url}")
    soup = get_soup(url)
    # Get the basis set info
    info = (soup.find("pre")).get_text()
    lines = info.strip().splitlines()[1:]
    used_lines = '\n'.join(lines)
    
    return used_lines
    
def get_soup(url) -> bytes: 
    """
    Resonably straight forward. Retrieves web info using
    BeautifulSoup
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def get_soup_from_popup_window(driver,main_window_handle):
    """
    Handels pop up windows and retrieve soup. Needs the main
    window handle to function. Remember to put at the end:
        # Close the new window
        driver.close()

        # Switch back to the main window
        driver.switch_to.window(main_window_handle)
    """
    # Wait for the new window to open
    wait = WebDriverWait(driver, 10)
    wait.until(EC.number_of_windows_to_be(2))

    # Switch to the new window
    new_window_handle = [handle for handle in driver.window_handles if handle != main_window_handle][0]
    driver.switch_to.window(new_window_handle)

    # Get the updated page source after executing the JavaScript function
    updated_page_source = driver.page_source

    # Parse the updated HTML content using BeautifulSoup
    updated_soup = BeautifulSoup(updated_page_source, "html.parser")
    return updated_soup

######################################################################
# ANYTREE
######################################################################
class DataNode(NodeMixin):
    def __init__(self, name, value=None, parent=None):
        super().__init__()
        self.name = name
        self.value = value
        self.parent = parent

    def __repr__(self):
        return f"{self.name}: {self.value}"

######################################################################
# DATA COLLECTION FUNCTIONS
######################################################################
def export_data_json(filename, root):
    """
    This function imports data (root) into a json file
    """
    try:
        # Create an instance of JsonExporter
        exporter = JsonExporter(indent=2, sort_keys=True)

        # Export the tree to a JSON-compatible dictionary
        data = exporter.export(root)

        json_data = json.dumps(data, indent=4)

        # Write the JSON string to a file
        with open(filename, "w") as file:
            file.write(json_data)
            
    except Exception as e:
        print(f"Cannot export data from {file}: {e}")

def import_data_json(filename):
    """
    This function imports data from a jason file as imported_data.
    It also renders a tree of the nested data
    """
    try:
        importer = JsonImporter()

        # Read the JSON file
        with open(filename, "r") as file:
            json_data = json.loads(file.read())
            
        # Import the JSON data
        imported_data = importer.import_(json_data)
        print(RenderTree(imported_data))
        
    except Exception as e:
        print(f"Cannot import data from {file}: {e}")
        

def save_data_to_csv(node, file_path):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Node', 'Value'])

        for pre, _, n in RenderTree(node):
            writer.writerow([pre + n.name, n.value])

####################################################################

def get_element_page(soup):
    """
    The main function of the script. Needs to be separated
    further cause its messy
    """
    # Find the map element by its class name and area elements within the map
    periodensystemmap = soup.find("map", {"name": "PeriodensystemMap"})
    areas = periodensystemmap.find_all("area")

    page_source = driver.page_source

    root = DataNode("Root")
    
    main_window_handle = driver.current_window_handle

    for area in areas:
        # Assign a key value to the element
        symbol = area['alt']
        # Create a node for symbol
        symbol_node = DataNode(symbol, parent=root)        
        if 'href' in area.attrs and area['href'].startswith('javascript:'):
            # Simulate a click on the element using JavaScript
            element_id = area['id']
            
            driver.execute_script("arguments[0].click();", driver.find_element(By.ID, element_id))

            # Get the soup from the popup window
            updated_soup = get_soup_from_popup_window(driver,main_window_handle)

            # # Test if page is accessible
            # element = updated_soup.find("h3")
            # print(element)
            
            # Get the link to all the ECP core types 
            pseudopotential_links_dict = get_and_sort_urls(updated_soup)
            
            # FIX REQUIRED: need to change this to iterate over the key and value
            # so that pseudo_name = key and get_info(pseudo_link) = value
            for pseudo_name, pseudo_link in pseudopotential_links_dict.items():
                pseudo_line = get_info(pseudo_link)
                
                # Create a node for pseudo_name
                pseudo_node = DataNode(pseudo_name, value=pseudo_line, parent=symbol_node)
                print(pseudo_node.value)
                
                # Get the basis set links
                pseudo_soup = get_soup(pseudo_link)
                basis_set_links_dict = get_and_sort_urls(pseudo_soup)
                
                for basis_name, basis_link in basis_set_links_dict.items():
                    basis_line = get_info(basis_link)
                    # Create a node for basis_name
                    basis_node = DataNode(basis_name, value=basis_line, parent=pseudo_node)                    
                    print(basis_node.value)
            # Close the new window
            driver.close()

            # Switch back to the main window
            driver.switch_to.window(main_window_handle)

    # Close the Selenium WebDriver
    driver.quit()
    
    # Print the hierarchy using RenderTree
    for pre, _, node in RenderTree(root):
        print(f"{pre}{node.name}: {node.value}")
    return root

if __name__ == "__main__":
    # URL of the website
    url = "https://www.tc.uni-koeln.de/PP/clickpse.en.html"

    soup = get_soup(url)

    # Using selenium to interact with the website
    driver = webdriver.Chrome()
    driver.get(url)
        
    ECP_format_select(driver)
    root = get_element_page(soup)
    
    export_data_json("tree_data_json" , root)

