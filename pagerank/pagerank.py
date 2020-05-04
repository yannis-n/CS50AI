import os
import random
import re
import sys
import numpy as np

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    links = dict()
    if not corpus[page]:
        for link in corpus:
            links[link] = 1/len(corpus)
        return links

    linked_probability = damping_factor / len(corpus[page])
    probability = (1-damping_factor)/len(corpus)

    for link in corpus:
        links[link] = probability
        if link in corpus[page]:
            links[link] += linked_probability
    return links



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    samples = dict().fromkeys(list(corpus), 0)

    sample = random.choice(list(corpus))
    samples[sample] += 1
    for i in range(1,n):
        probabilities = transition_model(corpus, sample, damping_factor)
        sample = np.random.choice(list(probabilities), 1, replace=True, p=list(probabilities.values()))[0]
        samples[sample] +=1
    samples = {k: v / n for k, v in samples.items()}
    return samples

def iterative_algorithm(corpus, damping_factor, RP):
    new_RP = dict().fromkeys(list(corpus), 0)
    for rp in RP:
        sum = 0
        for page in corpus:
            if rp in corpus[page]:
                sum += RP[page]/len(corpus[page])

        new_RP[rp] = (1 - damping_factor)/ len(corpus) + damping_factor * sum
    divergence = dict()
    for page in corpus:
        divergence[page] = RP[page] - new_RP[page]
    if all(value < 0.001 for value in divergence.values()):
        return RP
    else:
        RP = iterative_algorithm(corpus, damping_factor, new_RP)
        return RP



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    for page in corpus:
        if len(corpus[page]) == 0:
            corpus[page] = set(link for link in corpus)
    RP = dict().fromkeys(list(corpus), 1/len(corpus))

    RP = iterative_algorithm(corpus, damping_factor, RP)

    return RP


if __name__ == "__main__":
    main()
