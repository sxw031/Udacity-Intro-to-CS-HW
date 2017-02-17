def get_page(url):
    """procedure that get requested url from thr internet"""

    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""

def union(a, b):
    """help function that union two arrays"""
    
    for e in b:
        if e not in a:
            a.append(e)

def get_next_target(page):
    """help function that return first link and end position of the link"""
    
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_links(page):
    """procedure that extract all links from requested page"""
    
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def crawl_web(seed): 
    """Initial function that starts the web crawling on the particular URL, returns index, graph of inlinks"""
    
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {}
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph

def add_to_index(index, keyword, url):
    """procedure that add [keyword:[url,...]] to the index."""

    # this index includes a url in the list of urls for a keyword multiple times, if the keyword appears on that page more than once.
    # if keyword in index:
    #     index[keyword].append(url)
    # else:
    #     index[keyword] = [url]

    # a given url is only inlclude once in the url list for a keyword, no matter how many times that keyword appears.
    for entry in index:
        if entry[0] == keyword:
            if url not in entry[1]:
                entry[1].append(url)
            return 
    index.append([keyword,[url]])

def add_page_to_index(index, url, content):
    """procedure that splits page into words as keyword and adds them to the index."""
    
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

def lookup(index, keyword):
    """help function that search the url from the given keyword from the index."""
    
    if keyword in index:
        return index[keyword]
    else:
        return None
 
def ordered_search(index, ranks, keyword):
    """function that returns the sorted list of all URLs from the keyword. """
    
    pages = lookup(index,keyword)
    return quick_sort(pages, ranks)
  
def quick_sort(pages, ranks):
    """help function that use quick_sort algorithm to order the ranking result from the index. """
    
    if not pages or len(pages) <= 1:
        return pages
    else:
        pivot = ranks[pages[0]]
        better = []
        worse = []
        for page in pages[1:]:
            if ranks[page] >= pivot:
                better.append(page)
            else:
                worse.append(page)
        return quick_sort(better, ranks) + [pages[0]] + quick_sort(worse, ranks)

# A -> B a reciprocal link if there is a link path from B to A of length equal to k.
# The length of a link path is the number of links which are taken to travel from one page to the other. 
# This solve the problem where page ranking system is not longer able to collude with each other to improve their page ranks.
# If k == 0, then a link from A to A is a reciprocal link for node A.
# if k == 1, B -> A would count as a reciprocal link if there is a link A -> B, which include one link and so is of length of 1
# if k == 2 and above, the same logic continues.

def is_reciprocal_link(graph, source, destination, k):
    """function take an input k, which is a non-negative integer, and identify the reciprocal links of length up to and including k."""
    
    if k == 0:
        if destination == source:
            return True
        return False
    if source in graph[destination]:
        return True
    for node in graph[destination]:
        if is_reciprocal_link(graph, source, node, k-1):
            return True
    return False

# Formula to count rank:
#
# rank(page, 0) = 1/npages
# rank(page, t) = (1-d)/npages
#                 + sum (d * rank(p, t - 1) / number of outlinks from p)
#                 over all pages p that link to this page
def compute_ranks(graph,k):
    """function that coputes page ranks."""
    
    d = 0.8 # damping factor
    numloops = 10

    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages

    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    # exclude reciprocal links of length up to and including k from helping the page rank.
                    if not is_reciprocal_link(graph, node, page, k):
                        newrank = newrank + d * (ranks[node] / len(graph[node]) )
                    newrank = newrank + d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks


# Here are some example showing what ordered_search should do:
# Observe that the result list is sorted so the highest-ranking site is at the
# beginning of the list.

# Note: the intent of this question is for students to write their own sorting
# code, not to use the built-in sort procedure.

# test url
cache = {
   'http://udacity.com/cs101x/urank/index.html': """<html>
<body>
<h1>Dave's Cooking Algorithms</h1>
<p>
Here are my favorite recipies:
<ul>
<li> <a href="http://udacity.com/cs101x/urank/hummus.html">Hummus Recipe</a>
<li> <a href="http://udacity.com/cs101x/urank/arsenic.html">World's Best Hummus</a>
<li> <a href="http://udacity.com/cs101x/urank/kathleen.html">Kathleen's Hummus Recipe</a>
</ul>

For more expert opinions, check out the
<a href="http://udacity.com/cs101x/urank/nickel.html">Nickel Chef</a>
and <a href="http://udacity.com/cs101x/urank/zinc.html">Zinc Chef</a>.
</body>
</html>






""",
   'http://udacity.com/cs101x/urank/zinc.html': """<html>
<body>
<h1>The Zinc Chef</h1>
<p>
I learned everything I know from
<a href="http://udacity.com/cs101x/urank/nickel.html">the Nickel Chef</a>.
</p>
<p>
For great hummus, try
<a href="http://udacity.com/cs101x/urank/arsenic.html">this recipe</a>.

</body>
</html>






""",
   'http://udacity.com/cs101x/urank/nickel.html': """<html>
<body>
<h1>The Nickel Chef</h1>
<p>
This is the
<a href="http://udacity.com/cs101x/urank/kathleen.html">
best Hummus recipe!
</a>

</body>
</html>






""",
   'http://udacity.com/cs101x/urank/kathleen.html': """<html>
<body>
<h1>
Kathleen's Hummus Recipe
</h1>
<p>

<ol>
<li> Open a can of garbonzo beans.
<li> Crush them in a blender.
<li> Add 3 tablesppons of tahini sauce.
<li> Squeeze in one lemon.
<li> Add salt, pepper, and buttercream frosting to taste.
</ol>

</body>
</html>

""",
   'http://udacity.com/cs101x/urank/arsenic.html': """<html>
<body>
<h1>
The Arsenic Chef's World Famous Hummus Recipe
</h1>
<p>

<ol>
<li> Kidnap the <a href="http://udacity.com/cs101x/urank/nickel.html">Nickel Chef</a>.
<li> Force her to make hummus for you.
</ol>

</body>
</html>

""",
   'http://udacity.com/cs101x/urank/hummus.html': """<html>
<body>
<h1>
Hummus Recipe
</h1>
<p>

<ol>
<li> Go to the store and buy a container of hummus.
<li> Open it.
</ol>

</body>
</html>




""",
}


index, graph = crawl_web('http://udacity.com/cs101x/urank/index.html')
ranks = compute_ranks(graph)

print ordered_search(index, ranks, 'Hummus')
#>>> ['http://udacity.com/cs101x/urank/kathleen.html',
#    'http://udacity.com/cs101x/urank/nickel.html',
#    'http://udacity.com/cs101x/urank/arsenic.html',
#    'http://udacity.com/cs101x/urank/hummus.html',
#    'http://udacity.com/cs101x/urank/index.html']

print ordered_search(index, ranks, 'the')
#>>> ['http://udacity.com/cs101x/urank/nickel.html',
#    'http://udacity.com/cs101x/urank/arsenic.html',
#    'http://udacity.com/cs101x/urank/hummus.html',
#    'http://udacity.com/cs101x/urank/index.html']


print ordered_search(index, ranks, 'babaganoush')
#>>> None

