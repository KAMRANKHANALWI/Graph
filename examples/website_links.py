"""
Website Links Example
====================
Simple example showing how website pages link to each other.
"""

from collections import deque


def create_website_structure():
    """
    Create a simple website with page links
    """
    # Website pages and their outgoing links
    pages = {
        "home": ["about", "products", "contact", "blog"],
        "about": ["home", "team", "history"],
        "products": ["home", "product1", "product2", "product3"],
        "contact": ["home"],
        "blog": ["home", "post1", "post2", "post3"],
        "team": ["about", "home"],
        "history": ["about", "home"],
        "product1": ["products", "home"],
        "product2": ["products", "home"],
        "product3": ["products", "home"],
        "post1": ["blog", "home"],
        "post2": ["blog", "home"],
        "post3": ["blog", "home"],
    }
    return pages


def show_website_map(pages):
    """
    Display the website structure clearly
    """
    print("🌐 WEBSITE STRUCTURE")
    print("=" * 25)

    # Organize by page type
    main_pages = ["home", "about", "products", "contact", "blog"]
    sub_pages = [page for page in pages.keys() if page not in main_pages]

    print("Main pages:")
    for page in main_pages:
        if page in pages:
            links = pages[page]
            print(f"  {page}: links to {links}")

    print(f"\nSub pages:")
    for page in sorted(sub_pages):
        links = pages[page]
        print(f"  {page}: links to {links}")

    total_pages = len(pages)
    total_links = sum(len(links) for links in pages.values())

    print(f"\nTotal pages: {total_pages}")
    print(f"Total links: {total_links}")


def find_navigation_path(pages, start_page, target_page):
    """
    Find how to navigate from one page to another
    """
    print(f"\n🧭 Navigation path: {start_page} → {target_page}")

    if start_page == target_page:
        print(f"  Already on {target_page}!")
        return [start_page]

    if start_page not in pages:
        print(f"  ❌ Page '{start_page}' doesn't exist!")
        return None

    # BFS to find shortest navigation path
    visited = set([start_page])
    queue = deque([(start_page, [start_page])])

    while queue:
        current_page, path = queue.popleft()

        # Check all links from current page
        for linked_page in pages.get(current_page, []):
            if linked_page == target_page:
                final_path = path + [linked_page]
                print(f"  ✅ Path found: {' → '.join(final_path)}")
                print(f"  Clicks needed: {len(final_path) - 1}")
                return final_path

            if linked_page not in visited:
                visited.add(linked_page)
                queue.append((linked_page, path + [linked_page]))

    print(f"  ❌ Cannot navigate to {target_page}")
    return None


def find_orphaned_pages(pages):
    """
    Find pages that no other page links to (orphaned pages)
    """
    print(f"\n🏝️ FINDING ORPHANED PAGES")
    print("=" * 28)

    # Find all pages that are linked to
    linked_to = set()
    for page, links in pages.items():
        linked_to.update(links)

    # Find pages that exist but aren't linked to
    all_pages = set(pages.keys())
    orphaned = all_pages - linked_to

    if orphaned:
        print(f"  ⚠️ Orphaned pages: {list(orphaned)}")
        print(f"  These pages can't be reached by following links!")
    else:
        print(f"  ✅ No orphaned pages - all pages are linked to")

    return list(orphaned)


def find_dead_end_pages(pages):
    """
    Find pages with no outgoing links (dead ends)
    """
    print(f"\n🔚 FINDING DEAD END PAGES")
    print("=" * 27)

    dead_ends = []
    for page, links in pages.items():
        if not links:
            dead_ends.append(page)

    if dead_ends:
        print(f"  🚫 Dead end pages: {dead_ends}")
        print(f"  Users get stuck here - should add more links!")
    else:
        print(f"  ✅ No dead ends - all pages have outgoing links")

    return dead_ends


def analyze_page_importance(pages):
    """
    Analyze which pages are most important based on incoming links
    """
    print(f"\n⭐ PAGE IMPORTANCE ANALYSIS")
    print("=" * 30)

    # Count incoming links for each page
    incoming_links = {page: 0 for page in pages}

    for page, links in pages.items():
        for linked_page in links:
            if linked_page in incoming_links:
                incoming_links[linked_page] += 1

    # Sort by importance (most incoming links)
    sorted_pages = sorted(incoming_links.items(), key=lambda x: x[1], reverse=True)

    print(f"Pages ranked by incoming links:")
    for i, (page, link_count) in enumerate(sorted_pages[:5], 1):
        print(f"  {i}. {page}: {link_count} incoming links")

    return sorted_pages


def check_broken_links(pages):
    """
    Find broken links (links to pages that don't exist)
    """
    print(f"\n🔗 CHECKING FOR BROKEN LINKS")
    print("=" * 30)

    all_pages = set(pages.keys())
    broken_links = []

    for page, links in pages.items():
        for linked_page in links:
            if linked_page not in all_pages:
                broken_links.append((page, linked_page))

    if broken_links:
        print(f"  ❌ Broken links found:")
        for from_page, to_page in broken_links:
            print(f"    {from_page} → {to_page} (page doesn't exist)")
    else:
        print(f"  ✅ No broken links found")

    return broken_links


def suggest_navigation_improvements(pages):
    """
    Suggest improvements to website navigation
    """
    print(f"\n💡 NAVIGATION IMPROVEMENT SUGGESTIONS")
    print("=" * 40)

    # Check if home page is reachable from all pages
    unreachable_from_home = []
    for page in pages:
        if page != "home":
            path = find_navigation_path(pages, "home", page)
            if not path:
                unreachable_from_home.append(page)

    if unreachable_from_home:
        print(f"  📍 Pages unreachable from home: {unreachable_from_home}")
        print(f"     Suggestion: Add navigation links to these pages")

    # Check for long navigation paths
    print(f"\n  📏 Checking navigation efficiency:")
    long_paths = []

    important_pages = ["about", "products", "contact", "blog"]
    for target in important_pages:
        if target in pages:
            path = find_navigation_path(pages, "home", target)
            if path and len(path) > 2:
                long_paths.append((target, len(path) - 1))

    if long_paths:
        print(f"     Pages requiring multiple clicks from home:")
        for page, clicks in long_paths:
            print(f"       {page}: {clicks} clicks")
        print(f"     Suggestion: Add direct links from home to important pages")
    else:
        print(f"     ✅ All important pages accessible in 1 click from home")


def simulate_user_journey(pages, start_page="home", max_clicks=5):
    """
    Simulate a random user browsing the website
    """
    print(f"\n👤 SIMULATING USER JOURNEY")
    print("=" * 28)

    import random

    current_page = start_page
    journey = [current_page]

    print(f"Starting at: {current_page}")

    for click in range(max_clicks):
        available_links = pages.get(current_page, [])

        if not available_links:
            print(f"  Click {click + 1}: Stuck at {current_page} (no links)")
            break

        # Randomly choose next page
        next_page = random.choice(available_links)
        journey.append(next_page)
        current_page = next_page

        print(f"  Click {click + 1}: Went to {next_page}")

    print(f"\nComplete journey: {' → '.join(journey)}")
    print(f"Pages visited: {len(set(journey))} unique pages")

    return journey


def create_sitemap(pages):
    """
    Create a visual sitemap using graph structure
    """
    print(f"\n🗺️ WEBSITE SITEMAP")
    print("=" * 20)

    # Start from home and show the hierarchy
    def show_level(page, visited, indent=0):
        if page in visited:
            return

        visited.add(page)
        spacing = "  " * indent
        links = pages.get(page, [])

        if links:
            print(f"{spacing}{page} → {links}")
        else:
            print(f"{spacing}{page} (no outgoing links)")

        # Show sub-pages
        for linked_page in links:
            if linked_page not in visited and linked_page != "home":
                show_level(linked_page, visited, indent + 1)

    visited = set()
    show_level("home", visited)


def main():
    """
    Main demonstration of website link analysis
    """
    print("🌐 WEBSITE LINKS ANALYSIS")
    print("=" * 30)

    # Create and show website structure
    pages = create_website_structure()
    show_website_map(pages)

    # Create sitemap
    create_sitemap(pages)

    # Test navigation paths
    print(f"\n" + "=" * 50)
    test_navigations = [
        ("home", "product2"),
        ("post1", "about"),
        ("team", "products"),
        ("contact", "blog"),
    ]

    for start, end in test_navigations:
        find_navigation_path(pages, start, end)

    # Analyze website health
    print(f"\n" + "=" * 50)
    find_orphaned_pages(pages)
    find_dead_end_pages(pages)
    check_broken_links(pages)

    # Analyze page importance
    print(f"\n" + "=" * 50)
    analyze_page_importance(pages)

    # Suggest improvements
    print(f"\n" + "=" * 50)
    suggest_navigation_improvements(pages)

    # Simulate user journey
    print(f"\n" + "=" * 50)
    simulate_user_journey(pages)


if __name__ == "__main__":
    main()

    print("\n✅ You analyzed website structure with graphs!")
    print("🎯 This shows how graphs help optimize website navigation!")
