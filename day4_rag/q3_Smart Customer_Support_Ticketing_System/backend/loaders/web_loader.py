from langchain_community.document_loaders import WebBaseLoader

def load_webpage_ulr(urls):
    """
    Loads a webpage from a given URL using LangChain's WebBaseLoader.

    Args:
        url (str): The URL of the web page you want to scrape.

    Returns:
        List of Document objects (each has text content and metadata)
    """
    loader = WebBaseLoader(web_paths=[urls])
    docs = loader.load()
    return docs

