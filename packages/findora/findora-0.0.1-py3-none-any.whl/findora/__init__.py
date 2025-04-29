import re
from prompts import prompts
from llmatch import llmatch
from langchain_llm7 import ChatLLM7


def findora(
        search_query,
        llm=None,
        n=10,
        enhance=True,
        verbose=False,
        max_retries=100,
        language="en-US",
        location="World",
):
    """
    Findora is a function that searches for relevant documents based on a query.

    Parameters
    ----------
    search_query : str
        The query string to search for.
    llm : object, optional
        The language model to use for searching. If not provided, a default one will be used.
    n : int, optional
        The number of results to return. Default is 10.
    enhance : bool, optional
        Whether to enhance the input query. Default is True.

    Returns
    -------
    list
        A list of relevant documents based on the search query.
    """
    if len(search_query) > 1024:
        raise ValueError("Search query is too long. Maximum length is 1000 characters.")

    if llm is None:
        llm = ChatLLM7(model="searchgpt")

    is_valid_query = llmatch(
        llm=llm,
        query=prompts["check_search_query"]["system"] + "\n" +
              prompts["check_search_query"]["user"].format(search_query=search_query),
        verbose=verbose,
        max_retries=max_retries,
        pattern=prompts["check_search_query"]["pattern"],
    )
    is_valid_query = is_valid_query["extracted_data"][0]
    if is_valid_query is not '1':
        raise ValueError(f"Invalid search query: {search_query}")

    if enhance:
        enhanced_query = llmatch(
            query=prompts["enhance_search_query"]["system"] + "\n" +
                  prompts["enhance_search_query"]["user"].format(search_query=search_query),
            verbose=verbose,
            max_retries=max_retries,
            pattern=prompts["enhance_search_query"]["pattern"],
        )
        search_query = enhanced_query["extracted_data"][0]

    count_results = 0
    results = []
    seen_urls = set()

    curr_results = llmatch(
            query=prompts["search"]["system"] + "\n" +
                  prompts["search"]["user"].format(search=search_query),
            llm=llm,
            verbose=verbose,
            max_retries=max_retries,
            pattern=prompts["search"]["pattern"],
    )
    curr_results = curr_results["extracted_data"][0]
    matches = re.findall(r"<search_result>\s*<title>(.*?)</title>\s*<url>(.*?)</url>\s*<desc>(.*?)</desc>\s*</search_result>", curr_results, re.DOTALL)

    for title, url, desc in matches:
        url = url.strip()
        if url not in seen_urls:
            seen_urls.add(url)
            results.append(
                    {
                        "title": title.strip(),
                        "url": url,
                        "desc": desc.strip(),
                    }
            )

    results = results[:n]

    return results
'''
results = findora(
    search_query="Найди картинки парижа",
    llm=ChatLLM7(model="searchgpt"),
    n=5,
    enhance=True,
    verbose=True,
)
print(results)
'''