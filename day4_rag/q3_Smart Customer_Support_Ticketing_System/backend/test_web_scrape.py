from loaders.web_loader import load_webpage_ulr
from db.document_db import insert_documents

def main():
     url = "https://support.apple.com/en-in/iphone"  # Apple iPhone Support FAQ page
     category = "faq"

     docs = load_webpage_ulr(url)

     # print("docs: ", docs)
     print("length of docs: ", len(docs))

     insert_documents(docs, category)

if  __name__=="__main__":
    main()



# from loaders.web_loader import load_webpage_ulr
# from db.document_db import insert_documents

# category_url_map = {
# #     "FAQ": "https://support.apple.com/en-in/iphone",
#     "Returns": "https://www.apple.com/in/shop/help/returns_refund",
#     "Shipping": "https://www.apple.com/in/shop/help/shipping_delivery",
#     "Warranty": "https://support.apple.com/en-in/iphone/repair/service",
#     "Payments": "https://support.apple.com/en-in/billing",
# }

# def main():
#     for category, url in category_url_map.items():
#         print(f"\n🔍 Processing category: {category}")
#         docs = load_webpage_ulr(url)
#         print(f"→ Loaded {len(docs)} docs for '{category}'")
#         insert_documents(docs, category)

# if __name__ == "__main__":
#     main()
