"""
Web Crawler using Graphs
=========================================
Learn how web crawlers work using graph algorithms (BFS/DFS).
"""

from collections import deque


class SimpleWebCrawler:
    """
    A simple web crawler that treats websites as a graph
    """

    def __init__(self):
        self.website_links = {}  # website -> list of linked websites
        self.visited_sites = set()
        self.crawl_results = []

    def add_website(self, site, links):
        """
        Add a website and its outgoing links
        """
        self.website_links[site] = links
        print(f"📄 Added website: {site} with {len(links)} links")

    def crawl_bfs(self, start_site, max_pages=10):
        """
        Crawl websites using BFS (breadth-first)
        Explores level by level like real crawlers
        """
        print(f"🌐 Starting BFS crawl from: {start_site}")
        print("=" * 40)

        if start_site not in self.website_links:
            print(f"❌ Starting site {start_site} not found!")
            return []

        visited = set()
        queue = deque([start_site])
        visited.add(start_site)
        crawled_sites = []

        while queue and len(crawled_sites) < max_pages:
            current_site = queue.popleft()
            crawled_sites.append(current_site)

            print(f"  🔍 Crawling: {current_site}")

            # Get all links from current site
            links = self.website_links.get(current_site, [])
            print(f"    Found {len(links)} links: {links}")

            # Add unvisited links to queue
            for link in links:
                if link not in visited and link in self.website_links:
                    visited.add(link)
                    queue.append(link)
                    print(f"      ➕ Added to queue: {link}")

        print(f"\n✅ BFS Crawl complete! Visited {len(crawled_sites)} pages")
        return crawled_sites

    def crawl_dfs(self, start_site, max_pages=10):
        """
        Crawl websites using DFS (depth-first)
        Goes deep into one path before backtracking
        """
        print(f"🕳️ Starting DFS crawl from: {start_site}")
        print("=" * 40)

        if start_site not in self.website_links:
            print(f"❌ Starting site {start_site} not found!")
            return []

        visited = set()
        crawled_sites = []

        def dfs_helper(site):
            if len(crawled_sites) >= max_pages:
                return

            visited.add(site)
            crawled_sites.append(site)
            print(f"  🔍 Crawling: {site}")

            # Get all links from current site
            links = self.website_links.get(site, [])
            print(f"    Found {len(links)} links: {links}")

            # Visit each unvisited link
            for link in links:
                if link not in visited and link in self.website_links:
                    print(f"      ➡️ Going deeper to: {link}")
                    dfs_helper(link)

        dfs_helper(start_site)
        print(f"\n✅ DFS Crawl complete! Visited {len(crawled_sites)} pages")
        return crawled_sites

    def find_path_between_sites(self, start_site, target_site):
        """
        Find if you can get from one website to another by following links
        """
        print(f"🎯 Finding path: {start_site} → {target_site}")

        if start_site not in self.website_links:
            return None

        visited = set([start_site])
        queue = deque([(start_site, [start_site])])

        while queue:
            current_site, path = queue.popleft()

            if current_site == target_site:
                print(f"  ✅ Path found: {' → '.join(path)}")
                return path

            for link in self.website_links.get(current_site, []):
                if link not in visited and link in self.website_links:
                    visited.add(link)
                    queue.append((link, path + [link]))

        print(f"  ❌ No path from {start_site} to {target_site}")
        return None

    def analyze_website_network(self):
        """
        Analyze the website network structure
        """
        print("📊 WEBSITE NETWORK ANALYSIS")
        print("=" * 30)

        total_sites = len(self.website_links)
        total_links = sum(len(links) for links in self.website_links.values())

        print(f"🌐 Total websites: {total_sites}")
        print(f"🔗 Total links: {total_links}")

        if total_sites > 0:
            avg_links = total_links / total_sites
            print(f"📊 Average links per site: {avg_links:.1f}")

        # Find most connected sites
        site_connections = [
            (site, len(links)) for site, links in self.website_links.items()
        ]
        site_connections.sort(key=lambda x: x[1], reverse=True)

        print(f"\n🌟 Most connected sites:")
        for i, (site, links) in enumerate(site_connections[:3], 1):
            print(f"   {i}. {site} ({links} outgoing links)")

        # Find sites with no outgoing links (dead ends)
        dead_ends = [site for site, links in self.website_links.items() if not links]
        if dead_ends:
            print(f"\n🔚 Dead end sites (no outgoing links): {dead_ends}")


def create_example_website_network():
    """
    Create a simple website network for testing
    """
    print("🏗️ CREATING EXAMPLE WEBSITE NETWORK")
    print("=" * 38)

    crawler = SimpleWebCrawler()

    # Add websites and their links (simplified)
    websites = {
        "google.com": ["youtube.com", "gmail.com", "maps.google.com"],
        "youtube.com": ["google.com", "music.youtube.com"],
        "gmail.com": ["google.com", "calendar.google.com"],
        "facebook.com": ["instagram.com", "whatsapp.com"],
        "instagram.com": ["facebook.com"],
        "whatsapp.com": ["facebook.com"],
        "twitter.com": ["tweetdeck.com"],
        "tweetdeck.com": ["twitter.com"],
        "maps.google.com": ["google.com"],
        "music.youtube.com": ["youtube.com"],
        "calendar.google.com": ["gmail.com"],
        "reddit.com": ["news.reddit.com"],
        "news.reddit.com": ["reddit.com"],
    }

    # Add all websites to crawler
    for site, links in websites.items():
        crawler.add_website(site, links)

    return crawler


def demonstrate_web_crawling():
    """
    Show how web crawling works with both BFS and DFS
    """
    crawler = create_example_website_network()

    print("\n" + "=" * 50)

    # Analyze the network first
    crawler.analyze_website_network()

    print("\n" + "=" * 50)

    # Compare BFS vs DFS crawling
    start_site = "google.com"
    max_pages = 8

    print("🆚 COMPARING CRAWL STRATEGIES")
    print("=" * 30)

    # BFS crawl
    print(f"\n1️⃣ BFS Crawl (explores level by level):")
    bfs_results = crawler.crawl_bfs(start_site, max_pages)
    print(f"   BFS visited: {bfs_results}")

    print(f"\n2️⃣ DFS Crawl (goes deep first):")
    dfs_results = crawler.crawl_dfs(start_site, max_pages)
    print(f"   DFS visited: {dfs_results}")

    print(f"\n📊 Comparison:")
    print(f"   BFS explores broadly first")
    print(f"   DFS explores one path deeply first")
    print(f"   Both visit the same sites, just in different order!")


def show_link_analysis():
    """
    Show how to analyze connections between websites
    """
    print("\n🔗 LINK ANALYSIS EXAMPLES")
    print("=" * 30)

    crawler = create_example_website_network()

    # Test different paths
    test_paths = [
        ("google.com", "music.youtube.com"),
        ("facebook.com", "instagram.com"),
        ("google.com", "reddit.com"),
        ("twitter.com", "facebook.com"),
    ]

    for start, end in test_paths:
        crawler.find_path_between_sites(start, end)


def real_world_applications():
    """
    Explain real-world applications of web crawling
    """
    print("\n🌍 REAL-WORLD WEB CRAWLING")
    print("=" * 30)

    print(
        """
🚀 HOW WEB CRAWLERS ARE USED:

1. 🔍 SEARCH ENGINES
   • Google, Bing crawl billions of pages
   • Index content for search results  
   • Follow links to discover new pages
   • Use BFS to explore systematically

2. 📊 DATA COLLECTION
   • Price comparison websites
   • Social media analysis
   • News aggregation
   • Market research

3. 🛡️ SECURITY SCANNING
   • Find vulnerabilities in websites
   • Check for broken links
   • Monitor website changes
   • Detect malicious content

4. 📈 SEO ANALYSIS
   • Analyze website structure
   • Find internal linking issues
   • Check page accessibility
   • Monitor competitor sites

5. 📚 ARCHIVING
   • Wayback Machine saves web history
   • Digital preservation
   • Academic research
   • Legal compliance

🤖 CRAWLER STRATEGIES:

• BFS (Breadth-First): 
  ✅ Good for finding all pages
  ✅ Discovers important pages first
  ❌ Uses more memory

• DFS (Depth-First):
  ✅ Uses less memory
  ✅ Good for deep site exploration
  ❌ Might miss important pages

• Focused Crawling:
  ✅ Targets specific topics
  ✅ More efficient
  ✅ Better quality results
"""
    )


def simple_crawler_rules():
    """
    Basic rules and ethics of web crawling
    """
    print("\n📋 WEB CRAWLING BEST PRACTICES")
    print("=" * 35)

    print(
        """
✅ GOOD PRACTICES:

1. 🤖 RESPECT ROBOTS.TXT
   • Check /robots.txt file
   • Follow crawling rules
   • Respect disallowed areas

2. ⏱️ BE POLITE WITH REQUESTS
   • Add delays between requests
   • Don't overload servers
   • Respect rate limits

3. 🆔 IDENTIFY YOURSELF
   • Use proper User-Agent
   • Provide contact information
   • Be transparent about purpose

4. 📝 FOLLOW TERMS OF SERVICE
   • Read website policies
   • Don't violate copyright
   • Respect data usage rules

❌ THINGS TO AVOID:

• Don't crawl too fast
• Don't ignore robots.txt
• Don't scrape personal data
• Don't overload small sites
• Don't violate copyright

🛡️ TECHNICAL CONSIDERATIONS:

• Handle JavaScript-rendered pages
• Manage cookies and sessions
• Deal with CAPTCHAs
• Handle redirects properly
• Implement error handling
"""
    )


if __name__ == "__main__":
    # Main demonstration
    demonstrate_web_crawling()

    # Link analysis
    show_link_analysis()

    # Real-world applications
    real_world_applications()

    # Best practices
    simple_crawler_rules()

    print("\n✅ You now understand web crawling with graphs!")
    print("🎯 Key insight: Web crawling is just graph traversal on the internet!")
