import meilisearch

client = meilisearch.Client(
    "http://127.0.0.1:7700"
)

# PRODUCTS INDEX
products_index = client.index(
    "products"
)

# CATEGORY INDEX
categories_index = client.index(
    "categories"
)

# PRIMARY KEYS
try:

    products_index.update_filterable_attributes([
        "category",
        "brand",
        "offer_price",
        "status"
    ])

except:
    pass

print(
    "Meilisearch Connected"
)