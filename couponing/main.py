from typing import List, Dict, Optional, Union


def parent_category(child: Optional[str], categories: Dict[str, Optional[str]]) -> Optional[str]:
    """
    Returns the parent coupon category for a given category. if `child` is
    None or the parent name cannot be found, then None is returned.

    Args:
        child: The category name whose parent needs to be found.
        categories: A dictionary of `{child}:{parent}` representing the parent-child category relationship

    Returns:
        The parent category name of `None` if `child` is `None` or is not in the keys of `categories`
    """
    return categories.get(child, None) if child else None


def find_coupon(category_name: Optional[str], coupons: List[Dict[str, str]],
                categories: Dict[str, Optional[str]], reverse=False) -> str:
    """
    Given a category name, returns a list of the most recent coupons it can find

    Args:
        category_name: The category name
        coupons: A list of available coupons.
        categories: A dictionary of `{child}:{parent}` representing the parent-child category relationship
        reverse: Returns the list of coupons in reverse-lexical order if `True`

    Returns:
        The list of the most recent coupons it can find or an empty list if no list was found
    """
    if category_name is None:
        return []
    coupons_found = [(x["Coupon Name"], x["Date Modified"]) for x in coupons if x["Category Name"] == category_name]
    if not coupons_found:
        return find_coupon(parent_category(category_name, categories), coupons, categories, reverse=reverse)
    coupons_found.sort(reverse=True, key=lambda x: x[1])
    lowest_date = coupons_found[0][1]
    ret = [r[0] for r in coupons_found if r[1] == lowest_date]
    ret.sort(reverse=reverse)
    print(ret[0])
    return ret[0]


def apply_coupon(prod_name: str, coupons: List[Dict[str, str]],
                 categories: List[Union[Dict[str, str], Dict[str, Optional[str]]]]):
    """

    Args:
        prod_name:
        coupons:
        categories:

    Returns:

    """
    products = [
        {"Product Name": "Cozy Comforter", "Price": "100.00", "Category Name": "Comforter Sets"},
        {"Product Name": "All-in-one Bedding Set", "Price": "50.00", "Category Name": "Bedding"},
        {"Product Name": "Infinite Soap Dispenser", "Price": "500.00", "Category Name": "Bathroom Accessories"},
        {"Product Name": "Rainbow Toy Box", "Price": "257.00", "Category Name": "Baby And Kids"}
    ]
    product_category = [x for x in products if x["Product Name"] == prod_name]
    if not product_category:
        return None
    category_name, price = product_category[0]["Category Name"], float(product_category[0]["Price"])
    coupon = find_coupon(category_name, coupons, categories)
    if not coupon:
        return 0
    discount = float([x for x in coupons if x["Coupon Name"] == coupon][0]["Discount"][:-1])

    return price * (1 - discount / 100.0)


if __name__ == "__main__":
    coupons: List[Dict[str, str]] = [
        {"Category Name": "Comforter Sets", "Coupon Name": "Comforters sale", "Date Modified": "2020-01-01",
         "Discount": "10%"},
        {"Category Name": "Comforter Sets", "Coupon Name": "Cozy Comforter Coupon", "Date Modified": "2020-01-01",
         "Discount": "15%"},
        {"Category Name": "Bedding", "Coupon Name": "Best Bedding Bargains", "Date Modified": "2019-01-01",
         "Discount": "35%"},
        {"Category Name": "Bedding", "Coupon Name": "Savings on Bedding", "Date Modified": "2019-01-01",
         "Discount": "25%"},
        {"Category Name": "Bed & Bath", "Coupon Name": "Low price for Bed & Bath", "Date Modified": "2018-01-01",
         "Discount": "50%"},
        {"Category Name": "Bed & Bath", "Coupon Name": "Bed & Bath extravaganza", "Date Modified": "2019-01-01",
         "Discount": "75%"}
    ]

    categories: List[Union[Dict[str, str], Dict[str, Optional[str]]]] = [
        {"Category Name": "Comforter Sets", "Category Parent Name": "Bedding"},
        {"Category Name": "Bedding", "Category Parent Name": "Bed & Bath"},
        {"Category Name": "Bed & Bath", "Category Parent Name": None},
        {"Category Name": "Soap Dispensers", "Category Parent Name": "Bathroom Accessories"},
        {"Category Name": "Bathroom Accessories", "Category Parent Name": "Bed & Bath"},
        {"Category Name": "Toy Organizers", "Category Parent Name": "Baby And Kids"},
        {"Category Name": "Baby And Kids", "Category Parent Name": None},
    ]

    x = apply_coupon("Cozy Comforter", coupons, categories)
    print(x)
    x = apply_coupon("All-in-one Bedding Set", coupons, categories)
    print(x)

    # search_categories = ["Bed & Bath", "Bedding", "Bathroom Accessories", "Comforter Sets", "Toy Organizers"]
    # categories_child_parent = {x['Category Name']: x['Category Parent Name'] for x in categories}
    # for category in search_categories:
    #     print(f'"{category}"', "=>", find_coupon(category, coupons=coupons, categories=categories_child_parent))
