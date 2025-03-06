class ProductDTO:

    def __init__(self, product_name:str=None, product_description:str=None,
                 product_price:float=None,
                 product_image_name:str=None, product_image_path:str=None,
                 product_quantity:int=None):
        self.product_name = product_name
        self.product_description = product_description
        self.product_price = product_price
        self.product_image_name = product_image_name
        self.product_image_path = product_image_path
        self.product_quantity = product_quantity

    def validate(self):
        if not all([self.product_name, self.product_description,
                    self.product_price,
                    self.product_image_name, self.product_image_path,
                    self.product_quantity]):
            raise ValueError("All product fields must be filled and valid.")
        return self

    def update_validate(self):
        if not all([self.product_name, self.product_description, self.product_price, self.product_quantity]):
            raise ValueError("Product name, description, price, and quantity must be filled.")
        return self


    def __repr__(self):
        return (f"ProductDTO(product_name={self.product_name!r}, "
                f"product_description={self.product_description!r}, "
                f"product_price={self.product_price!r}, "
                f"product_image_name={self.product_image_name!r}, "
                f"product_image_path={self.product_image_path!r}, "
                f"product_quantity={self.product_quantity!r})")



