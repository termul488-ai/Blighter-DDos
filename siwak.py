import re
import requests
from bs4 import BeautifulSoup
import time
import random
import socket
import socks
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_socks5_proxy(proxy, test_url="http://httpbin.org/ip", timeout=5):
    """Checks the functionality of the SOCKS5 proxy"""
    try:
        ip, port = proxy.split(':')
        port = int(port)
        
        # Set up a SOCKS5 proxy for socket
        socks.set_default_proxy(socks.SOCKS5, ip, port)
        socket.socket = socks.socksocket
        
        start_time = time.time()
        response = requests.get(test_url, timeout=timeout)
        response_time = round((time.time() - start_time) * 1000, 2)
        
        # Восстанавливаем стандартный socket
        socks.set_default_proxy()
        
        if response.status_code == 200:
            print(f" Working proxy: {proxy} (response time: {response_time}мс)")
            return proxy
        else:
            print(f" Not working proxy: {proxy} (status: {response.status_code})")
            return None
            
    except Exception as e:
        # Restoring the default socket in case of an error
        socks.set_default_proxy()
        print(f" Proxy error {proxy}: {str(e)[:50]}...")
        return None

def extract_socks5_from_text(text):
     """Extracts a SOCKS5 proxy from text."""
    socks5_patterns = [
        r'\b(?:\d{1,3}\.){3}\d{1,3}:\d{1,5}\b',
        r'socks5://(?:\d{1,3}\.){3}\d{1,3}:\d{1,5}',
        r'\b(?:\d{1,3}\.){3}\d{1,3}:\d{1,5}(?=:[A-Za-z\s]+)',
    ]
    
    proxies = set()
    
    for pattern in socks5_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            proxy = match.replace('socks5://', '')
            proxy = re.sub(r':[^:]+$', '', proxy) if proxy.count(':') > 1 else proxy
            proxies.add(proxy)
    
    return list(proxies)

def scrape_url(url, timeout=10):
   """Scrapes URLs and extracts SOCKS5 proxies"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        if 'text/html' in response.headers.get('content-type', ''):
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
        else:
            text = response.text
        
        proxies = extract_socks5_from_text(text)
        return proxies
        
    except Exception as e:
        print(f"Error while scraping {url}: {e}")
        return []

def read_urls_from_file(filename):
    """Reads URLs from a file"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            urls = [line.strip() for line in file if line.strip()]
        return urls
    except FileNotFoundError:
        print(f"File {filename} not found!")
        return []

def save_proxies_to_file(proxies, filename):
    """Saves the proxy to a file"""
    with open(filename, 'w', encoding='utf-8') as file:
        for proxy in sorted(set(proxies)):
            file.write(proxy + '\n')

def check_proxies_parallel(proxies, max_workers=20, output_file='socks5work.txt'):
    """Checks proxies in multi-threaded mode and saves results as they are found"""
    working_proxies = []
    
    print(f"Let's start checking {len(proxies)} proxy...")
    
    # Create or clear a file for writing
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Workers SOCKS5 proxy\n")
        f.write(f"# Updated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    def proxy_callback(proxy):
        """Callback function for saving the found proxy"""
        if proxy:
            working_proxies.append(proxy)
            # working_proxies.append(proxy) 
            # Immediately save to file
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(proxy + '\n')
            print(f"Working proxy saved: {proxy}")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_proxy = {
            executor.submit(check_socks5_proxy, proxy): proxy 
            for proxy in proxies
        }
        
        for future in as_completed(future_to_proxy):
            result = future.result()
            if result:
                proxy_callback(result)
    
    return working_proxies

def collect_proxies_only():
    """Only proxy collection without verification"""
    input_file = 'socks5list.txt'
    output_file = 'socks5.txt'
    
    print("Reading URLs from a file...")
    urls = read_urls_from_file(input_file)
    
    if not urls:
        print("Not found URLs for processing.")
        return
    
    print(f"Found {len(urls)} URLs for processing.")
    
    all_proxies = []
    
    # Proxy collection
    for i, url in enumerate(urls, 1):
        print(f"Proxy collection {i}/{len(urls)}: {url}")
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        proxies = scrape_url(url)
        
        if proxies:
            print(f"Found {len(proxies)} прокси")
            all_proxies.extend(proxies)
        else:
            print("Proxy not found.")
        
        time.sleep(random.uniform(1, 3))
    
    if not all_proxies:
        print("No SOCKS5 proxies found.
        return
    
    # Removing duplicates unique_proxies = list(set(all_proxies)) 
print(f"\nFound {len(unique_proxies)} unique proxies")
    
    # We save all found proxies
    save_proxies_to_file(unique_proxies, output_file)
    print(f"✓ All found proxies are saved in {output_file}")
    
    # Showing a partial list print("\nFirst 10 found proxies:")
    for i, proxy in enumerate(unique_proxies[:10], 1):
        print(f"  {i:2d}. {proxy}")
    if len(unique_proxies) > 10:
        print(f"  ... and another {len(unique_proxies) - 10} proxies")

def collect_and_check_proxies():
    """Collecting and checking proxies"""
    input_file = 'socks5list.txt'
    output_file = 'socks5work.txt'
    
    print("Reading URLs from a file...")
    urls = read_urls_from_file(input_file)
    
    if not urls:
        print("No URLs found to process.")
        return
    
    print(f"Found {len(urls)} URLs to process.")
    
    all_proxies = []
    
    # Step 1: Collecting Proxies for i, url in enumerate(urls, 1): print(f"Collecting Proxies" {i}/{len(urls)}: {url}")
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        proxies = scrape_url(url)
        
        if proxies:
            print(f"Found {len(proxies)} proxies")
            all_proxies.extend(proxies)
        else:
            print("No proxies found")
        
        time.sleep(random.uniform(1, 3))
    
    if not all_proxies:
        print("No SOCKS5 proxies found")
        return
    
    # Removing duplicates
    unique_proxies = list(set(all_proxies))
    print(f"\nRemoving duplicates unique_proxies = list(set(all_proxies")) 
    print(f"\nFound {len(unique_proxies)} unique proxies")
    
    # Step 2: Testing functionality with automatic saving
    print("Starting to test proxy functionality...") 
    print(f"The results will be saved in real time in {output_file}")
    
    working_proxies = check_proxies_parallel(unique_proxies, output_file=output_file)
    
    # Final statistics
    if working_proxies:
        print(f"\n Check complete! Found {len(working_proxies)} working SOCKS5 proxy")
        print(f"All results are saved in {output_file}")
        
        print("\nFinalyl list of working proxies:")
        for i, proxy in enumerate(working_proxies, 1):
            print(f"  {i:2d}. {proxy}")
    else:
        print("✗ No working SOCKS5 proxies found")
        # Create an empty file with a comment
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# No workers found SOCKS5 прокси\n")
            f.write(f"# Verification completed: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

def show_menu():
    """Shows selection menu"""
    print("\n" + "="*50)
    print(" SOCKS5 PROXY COLLECTOR")
    print("="*50)
    print("1. Just build proxy (no verification))")
    print("2. Collect and check the proxy for availability")
    print("3. Выход")
    print("="*50)
    
    while True:
        choice = input("\nSelect an action (1-3): ").strip()
        if choice in ['1', '2', '3']:
            return choice
        else:
            print("Incorrect choice! Please enter 1, 2 or 3.")

def main():
    """Main function with selection menu"""
    while True:
        choice = show_menu()
        
        if choice == '1':
            print("\nStarting proxy collection...")
            collect_proxies_only()
            
        elif choice == '2':
            print("\nStarting proxy collection and verification...")
            collect_and_check_proxies()
            
        elif choice == '3':
            print("Exit the program.")
            break
        
        # We ask if the user wants to continue
        continue_choice = input("\nDo you want to perform another operation? (y/n): ").strip().lower()
        if continue_choice not in ['y', 'yes', 'd', 'no']:
            print("Exit the program.")
            break

if __name__ == "__main__":
    main()
