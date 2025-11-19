from schemas import Product


def product_image_key(product: Product) -> str:
    return f"{product.tenant_id}/{product.product_id}.png"
