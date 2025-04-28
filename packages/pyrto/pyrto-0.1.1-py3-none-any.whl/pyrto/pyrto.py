import requests
from bs4 import BeautifulSoup
import re
from PIL import Image
from io import BytesIO
import logging
import json

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fetch_vehicle_details(license_plate):
    url = f"https://www.carinfo.app/rc-details/{license_plate}"
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers, allow_redirects=True)
    
    if response.status_code != 200:
        logger.error(f"Failed to retrieve data for {license_plate}. HTTP Status code: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Initialize results dictionary
    results = {
        'License Plate': license_plate,
        'Owner Name': 'Not found',
        'Make & Model': 'Not found',
        'RTO Number': 'Not found',
        'Registered RTO Address': 'Not found',
        'State': 'Not found',
        'RTO Phone Number': 'Not found',
        'Website': 'Not found'
    }
    
    # Try to extract vehicle make & model from the new layout
    model_elem = soup.select_one('.input_vehical_layout_vehicalModel__1ABTF')
    if model_elem:
        results['Make & Model'] = model_elem.text.strip()
    
    # Try to extract owner name (may be hidden behind asterisks)
    owner_elem = soup.select_one('.input_vehical_layout_ownerName__NHkpi')
    if owner_elem:
        results['Owner Name'] = owner_elem.text.strip()
    
    # Extract RTO details from the expandable container
    rto_details = soup.select('.expand_component_detailItem__V43eh')
    for detail in rto_details:
        label_elem = detail.select_one('.expand_component_itemText__cbigB')
        value_elem = detail.select_one('.expand_component_itemSubTitle__ElsYf')
        
        if label_elem and value_elem:
            label = label_elem.text.strip()
            value = value_elem.text.strip()
            
            if "Number" in label and "RTO" not in label:
                results['RTO Number'] = value
            elif "Registered RTO" in label:
                results['Registered RTO Address'] = value
            elif "State" in label:
                results['State'] = value
            elif "RTO Phone number" in label:
                results['RTO Phone Number'] = value
            elif "Website" in label:
                results['Website'] = value

    # Log extracted details
    logger.info("Vehicle Details:")
    for key, value in results.items():
        logger.info(f"{key}: {value}")
    
    return results

def fetch_vehicle_image(license_plate):
    url = f"https://www.carinfo.app/rc-details/{license_plate}"
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers, allow_redirects=True)
    
    if response.status_code != 200:
        logger.error(f"Failed to retrieve data for {license_plate}. HTTP Status code: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # First try to find the image in the new layout
    img_elem = soup.select_one('.input_vehical_layout_rightSection__TJriH img')
    if img_elem and img_elem.get('src'):
        img_url = img_elem.get('src')
        if img_url.startswith('/'):
            # Convert relative URL to absolute
            img_url = f"https://www.carinfo.app{img_url}"
        elif img_url.startswith('/_next/image'):
            # Extract the original image URL from the _next/image URL
            img_match = re.search(r'url=([^&]+)', img_url)
            if img_match:
                img_url = requests.utils.unquote(img_match.group(1))
                if img_url.startswith('https'):
                    logger.info(f"Extracted image URL: {img_url}")
                else:
                    img_url = f"https://www.carinfo.app{img_url}"
        
        try:
            img_response = requests.get(img_url, headers=headers, allow_redirects=True)
            if img_response.status_code == 200:
                logger.info(f"Image successfully retrieved for {license_plate}")
                return Image.open(BytesIO(img_response.content))
            else:
                logger.error(f"Failed to retrieve image from {img_url}. HTTP Status code: {img_response.status_code}")
        except Exception as e:
            logger.error(f"Error processing image URL {img_url}: {e}")
    
    # Fallback to the old method
    img_pattern = r'https://imgd\.aeplcdn\.com[\S]+'
    img_urls = re.findall(img_pattern, response.text)
    
    if img_urls:
        img_url = img_urls[0]
        try:
            img_response = requests.get(img_url, headers=headers, allow_redirects=True)
            if img_response.status_code == 200:
                logger.info(f"Image successfully retrieved for {license_plate}")
                return Image.open(BytesIO(img_response.content))
            else:
                logger.error(f"Failed to retrieve image from {img_url}. HTTP Status code: {img_response.status_code}")
        except Exception as e:
            logger.error(f"Error processing image URL {img_url}: {e}")
    
    logger.warning("No image found with the specified URL patterns.")
    return None