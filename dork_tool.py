#!/usr/bin/env python3
"""
Dorking Tool by Jackalope - GOOGLE CSE VERSION
Real Google Dorking with Google Custom Search Engine API
"""

import argparse
import requests
import sys
import time
import random
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor
import json
from datetime import datetime
import urllib3
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BANNER = r"""
██████╗  ██████╗ ██████╗ ██╗  ██╗    ████████╗ ██████╗  ██████╗ ██╗     
██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
██║  ██║██║   ██║██████╔╝█████╔╝        ██║   ██║   ██║██║   ██║██║     
██║  ██║██║   ██║██╔══██╗██╔═██╗        ██║   ██║   ██║██║   ██║██║     
██████╔╝╚██████╔╝██║  ██║██║  ██╗       ██║   ╚██████╔╝╚██████╔╝███████╗
╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝

"""

GOOGLE_CSE_CX = os.getenv("GOOGLE_CSE_CX")
GOOGLE_CSE_BASE_URL = "https://www.googleapis.com/customsearch/v1"
GOOGLE_PSE_API_KEY = os.getenv("GOOGLE_PSE_API_KEY")
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:117.0) Gecko/20100101 Firefox/117.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15'
]

class CSEDorkTool:
    def __init__(self):
        self.session = requests.Session()
        self.google_api_key = GOOGLE_PSE_API_KEY
        self.cse_cx = GOOGLE_CSE_CX

        # Set header
        self.session.headers.update({
            'Accept': 'application/json,text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
        })

        self.session.verify = False

        # Retry strategy
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504], allowed_methods=["GET", "POST", "OPTIONS"])
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount('https://', adapter)
        self.session.mount('http://', adapter)

        self.results = []
        self.found_urls = set()

    def _get(self, url, extra_headers=None, timeout=15):
        """Helper to perform GET with rotated UA and merged headers"""
        headers = {}
        headers['User-Agent'] = random.choice(USER_AGENTS)
        if extra_headers:
            headers.update(extra_headers)

        try:
            resp = self.session.get(url, headers=headers, timeout=timeout, allow_redirects=True)
            return resp
        except Exception as e:
            raise

    def print_banner(self):
        print("\033[1;36m")
        print(BANNER)
        print("\033[1;35mGoogle CSE Dorking Tool - Web Surface Scanner")
        print("Created for Jackalope - Penetration Tester")
        print("=" * 60)
        print("\033[0m")

    def google_cse_search(self, query, num_results=10):
        """Search using Google Custom Search Engine API"""
        print(f"[*] Searching Google CSE for: {query}")
        urls = []

        if not self.google_api_key:
            print("[-] Google API Key is required for CSE search")
            print("[!] Please provide your Google API key using --google-api-key")
            return urls

        try:
            # CSE API parameters
            params = {
                'key': self.google_api_key,
                'cx': self.cse_cx,
                'q': query,
                'num': min(num_results, 10),
            }

            total_collected = 0
            start_index = 1

            while total_collected < num_results:
                params['start'] = start_index

                resp = self.session.get(GOOGLE_CSE_BASE_URL, params=params, timeout=15)

                if resp.status_code == 200:
                    data = resp.json()

                    if 'items' in data:
                        for item in data['items']:
                            urls.append(item['link'])
                            total_collected += 1

                            if total_collected >= num_results:
                                break

                    # Check if there are more results
                    if 'queries' in data and 'nextPage' in data['queries']:
                        start_index += 1
                        time.sleep(1)
                    else:
                        break
                else:
                    print(f"[-] CSE API returned HTTP {resp.status_code}: {resp.text}")
                    break

        except Exception as e:
            print(f"[-] Google CSE search failed: {e}")

        print(f"[+] Google CSE found {len(urls)} URLs")
        return urls

    def dorking_search(self, query, num_results=10, engines=None):
        if engines is None:
            engines = ['google_cse']

        print(f"[*] Performing dorking across {len(engines)} search engines")
        all_urls = []
        for engine in engines:
            if engine == 'google_cse':
                urls = self.google_cse_search(query, num_results)
            else:
                urls = []

            all_urls.extend(urls)
            time.sleep(1 + random.random() * 1.5) # Small randomized delay

        unique_urls = list(dict.fromkeys(all_urls))
        return unique_urls[:num_results]

    def build_dork_query(self, domain, url_pattern):
        query_parts = []

        if domain:
            if domain.startswith('*.'):
                query_parts.append(f"site {domain[2:]}")
            else:
                query_parts.append(f"site {domain}")

        if url_pattern:
            query_parts.append(f'inurl "{url_pattern}"')

        return " ".join(query_parts)

    def check_status(self, url):
        try:
            resp = self._get(url, timeout=15)
            return {
                'url': url,
                'status_code': resp.status_code if resp is not None else 0,
                'content_length': len(resp.content) if resp is not None else 0,
                'headers': dict(resp.headers) if resp is not None else {},
                'final_url': resp.url if resp is not None else url,
                'title': self.extract_title(resp.text) if resp is not None else None,
                'error': None
            }

        except Exception as e:
            return {
                'url': url,
                'status_code': 0,
                'content_length': 0,
                'title': None,
                'error': e
            }

    def extract_title(self, html):
        try:
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find('title')
            return title.text.strip() if title else "No Title"

        except:
            return "Except No Title"

    def filter_by_status(self, results, status_codes):
        if not status_codes:
            return results

        return [r for r in results if r['status_code'] in status_codes]

    def save_results(self, filename, results):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("DORKING RESULTS - Google CSE Tool\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Google CSE Tool found {len(results)} URLs")
                f.write("=" * 80 + "\n\n")

                for result in results:
                    f.write(f"URL: {result['url']}\n")
                    f.write(f"Status Code: {result['status_code']}\n")
                    f.write(f"Title: {result.get('title', 'N/A')}\n")
                    f.write(f"Content Length: {result['content_length']} bytes\n")
                    f.write(f"Final URL: {result.get('final_url', result['url'])}\n")

                    if result.get('error'):
                        f.write(f"Error: {result['error']}\n")

                    f.write("-" * 50 + "\n")

            print(f"[+] Results saved to: {filename}")

        except Exception as e:
            print(f"[-] Error saving results: {e}")

    def export_json(self, filename, results):
        try:
            output_data = {
                'metadata': {
                    'generated': datetime.now().isoformat(),
                    'tool': 'Google CSE Dorking Tool',
                    'google_cse_cx': GOOGLE_CSE_CX,
                    'total_results': len(results)
                },
                'results': results
            }

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=4, default=str, ensure_ascii=False)

            print(f"[+] JSON export saved to: {filename}")

        except Exception as e:
            print(f"[-] Error exporting JSON: {e}")

    def run_scan(self, domain, url_pattern, status_codes, num_results, output_file=None, export_json=False, threads=10):
        self.print_banner()
        print("[*] Starting Google CSE Dorking Scan")
        print(f"[*] Target Domain: {domain if domain else 'All domains'}")
        print(f"[*] URL Pattern: {url_pattern}")
        print(f"[*] Status Codes: {status_codes}")
        print(f"[*] Number of Results: {num_results}")
        print(f"[*] Threads: {threads}")

        if self.google_api_key:
            print(f"[*] Google API Key: {self.google_api_key[:10]}... (provided)")
        else:
            print("[-] Google API Key: NOT PROVIDED (CSE search will be disabled)")
        print("-" * 60)

        dork_query = self.build_dork_query(domain, url_pattern)
        print(f"[*] Dork Query: {dork_query}")

        # Determine which search engines to use
        engines = []
        if self.google_api_key:
            engines = ['google_cse']

        urls = self.dorking_search(dork_query, num_results, engines=engines)

        if not urls:
            print("[-] No URLs found with the specified criteria")
            print("[!] Try different search terms, adjust filters, or check your network / blocks")
            return

        print(f"[+] Found {len(urls)} potential targets from search engines")
        print("[*] Checking HTTP status codes...")

        with ThreadPoolExecutor(max_workers=threads) as executor:
            results = list(executor.map(self.check_status, urls))

        filtered_results = self.filter_by_status(results, status_codes)
        print(f"[+] Found {len(filtered_results)} URLs matching status criteria")

        if filtered_results:
            print("\n" + "=" * 100)
            print("\033[1;32mDORKING RESULTS:\033[0m")
            print("=" * 100)

            for i, result in enumerate(filtered_results, 1):
                status_code = result['status_code']
                if status_code == 200:
                    status_color = "\033[1;32m"
                elif status_code in [301, 302]:
                    status_color = "\033[1;33m"
                elif status_code == 404:
                    status_color = "\033[1;31m"
                else:
                    status_color = "\033[1;36m"

                print(f"{status_color}[{status_code}]\033[0m \033[1;34m{result['url']}\033[0m")
                print(f"     Title: {result.get('title', 'N/A')}")
                print(f"     Size: {result['content_length']} bytes")

                if result.get('error'):
                    print(f"     \033[1;31mError: {result['error']}\033[0m")

                print()
        else:
            print("[-] No results found matching the specified status codes")
            print("[*] Available status codes in results:")

            status_counts = {}
            for result in results:
                code = result['status_code']
                status_counts[code] = status_counts.get(code, 0) + 1

            for code, count in sorted(status_counts.items()):
                print(f"  - {code}: {count} URLs")

        if output_file and filtered_results:
            self.save_results(output_file, filtered_results)

        if export_json and filtered_results:
            json_file = output_file.replace('.txt', '.json') if output_file else 'dork_results.json'
            self.export_json(json_file, filtered_results)

        print(f"\n[+] Scan Summary:")
        print(f"    Total URLs Found: {len(urls)}")
        print(f"    URLs Matching Criteria: {len(filtered_results)}")
        print(f"    Scan completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def parse_status_codes(status_args):
    status_codes = []
    for arg in status_args:
        if ',' in arg:
            codes = arg.split(',')
            for code in codes:
                try:
                    status_codes.append(int(code.strip()))

                except ValueError:
                    print(f"[-] Invalid status code: {code}")
        else:
            try:
                status_codes.append(int(arg))

            except ValueError:
                print(f"[-] Invalid status code: {arg}")

    return status_codes if status_codes else [200]

def main():
    parser = argparse.ArgumentParser(
        description='Google CSE Dorking Tool - Web Surface Scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s -u "?id" -n 20 --google-api-key "YOUR_API_KEY"
  %(prog)s -d "example.com" -u "?page" -s 200 301 302 --google-api-key "YOUR_API_KEY"
  %(prog)s -d "*.co.id" -u "?view" -n 15 -o results.txt --json --google-api-key "YOUR_API_KEY"
  %(prog)s -u "index.php?q=" -n 30 -s 200 --threads 20 --google-api-key "YOUR_API_KEY"

Note: Google API Key is required for CSE functionality. Get one from:
      https://developers.google.com/custom-search/v1/introduction
        '''
    )

    parser.add_argument('-d', '--domain', help='Specific domain to target (e.g., example.co.id or *.co.id)')
    parser.add_argument('-u', '--url-pattern', required=True, help='URL pattern to search for (e.g., "?page=", "?id=", "index.php?q=")')
    parser.add_argument('-s', '--status-codes', nargs='+', default=['200'], help='HTTP status codes to filter (e.g., 200 301 302 or "200,301,302")')
    parser.add_argument('-n', '--number', type=int, default=10, help='Number of results to collect (default: 10)')
    parser.add_argument('-o', '--output', help='Output file to save results')
    parser.add_argument('--json', action='store_true', help='Export results as JSON')
    parser.add_argument('--threads', type=int, default=10, help='Number of threads (default: 10)')
    parser.add_argument('--google-api-key', help='Google API Key for Custom Search Engine (required for CSE)')

    args = parser.parse_args()
    status_codes = parse_status_codes(args.status_codes)

    tool = CSEDorkTool()

    try:
        tool.run_scan(
            domain=args.domain,
            url_pattern=args.url_pattern,
            status_codes=status_codes,
            num_results=args.number,
            output_file=args.output,
            export_json=args.json,
            threads=args.threads
        )
    except KeyboardInterrupt:
        print("\n[-] Scan interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"[-] Error during scan: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()