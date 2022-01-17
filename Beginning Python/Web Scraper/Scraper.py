from os import makedirs
from string import punctuation
from re import sub
from requests import get
from bs4 import BeautifulSoup


def main():
    # Gets type of article to search for
    article_type = input('Input type of article to search for (Try: "News", "Nature Briefing", "Article"): ')
    article_type = article_type.strip().title()

    # Gets number of pages to search
    while True:
        pages = input("Input number of pages to search: ")
        try:
            int(pages)
        except ValueError:
            print("Invalid input. ", end="")
        else:
            break

    print("Searching...\n")

    # Makes a new directory for new article types
    try:
        makedirs(article_type)
    except FileExistsError:
        pass

    # Found var to check if any articles are found
    found = False

    # Sequentially searches each webpage
    for p in range(1, int(pages) + 1):
        # Accesses the webpage at a specific page
        response = get(f"https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page={p}")

        if response.status_code != 200:
            raise ConnectionError

        # Finds all html sections for matching article types
        soup = BeautifulSoup(response.content, 'html.parser')
        anchors = soup.find_all('span', attrs={"class": "c-meta__type"}, text=article_type)

        for article in anchors:
            # Accesses each article's url and formats its title and body
            path = article.findParent('article').find('a', {'data-track-action': 'view article'})['href']
            url = f"https://www.nature.com{path}"
            response = get(url)

            if response.status_code != 200:
                raise ConnectionError

            soup = BeautifulSoup(response.content, 'html.parser')

            # Catches restricted articles
            if article_type == "Article":
                if '"open":true' not in soup.find("script", {"data-test": "dataLayer"}).text:
                    continue
                body = soup.find("div", {"class": "c-article-body"}).text
            else:
                body = soup.find("div", {"class": "c-article-body u-clearfix"}).text

            found = True

            # Removes excess new lines from body text
            body = sub(r'\n\s*\n', '\n\n', body)
            # Citation and title
            try:
                author = soup.find("meta", {"name": "dc.creator"})["content"]
            except TypeError:
                author = ""

            publisher = soup.find("meta", {"name": "prism.publicationName"})["content"]

            pub_date = soup.find("meta", {"name": "dc.date"})["content"]

            title = soup.find("title").text
            f_title = title.translate(title.maketrans(" ", "_", punctuation))

            citation = f"{author + '. ' if author else ''}{title}. {publisher}. {pub_date}. {url}.\n"

            # Stores the body in a file titled with the article's formatted title
            with open(f".\\{article_type}\\{f_title}.txt", mode="wb") as file:
                file.write(citation.encode())
                file.write(body.encode())

    if found:
        print("Articles saved.")
    else:
        print("No articles found.")


if __name__ == '__main__':
    main()
