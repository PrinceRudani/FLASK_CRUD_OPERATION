import os

from base.com.dao.product_dao import ProductDAO
from base.com.vo.product_vo import ProductVO
from base.com.vo.subcategory_vo import SubcategoryVO
from base.utils.generate_excel_file import excel_data_from_product_table
from base.utils.time_stamp import get_current_timestamp

image_directory = '/home/prince/sahana_projects/FlaskMVCProject/base/static/product_images'


class ProductService:
    @staticmethod
    def ajax_product_service(product_category_id):
        try:
            subcategory_vo = SubcategoryVO()
            subcategory_vo.subcategory_category_id = product_category_id
            product_dao = ProductDAO()
            sub_category_vo_lst = product_dao.ajax_product(subcategory_vo)
            return sub_category_vo_lst
        except Exception as e:
            raise Exception(f"Failed to fetch subcategories: {str(e)}")

    @staticmethod
    def insert_product_service(product_category_id,
                               product_sub_category_id, product_image,
                               product_dto):
        try:
            if not product_image or not hasattr(product_image, "filename"):
                raise ValueError("Invalid product image provided.")

            image_name = product_image.filename
            if not image_name.lower().endswith(
                    (".png", ".jpg", ".jpeg", ".gif")):
                raise ValueError(
                    "Invalid file type. Allowed types: png, jpg, jpeg, gif.")

            if not os.path.exists(image_directory):
                os.makedirs(image_directory)
            image_path = os.path.join(image_directory, image_name)
            product_image.save(image_path)

            product_vo = ProductVO()
            product_vo.product_category_id = product_category_id
            product_vo.product_sub_category_id = product_sub_category_id
            product_vo.product_name = product_dto.product_name
            product_vo.product_price = product_dto.product_price
            product_vo.product_description = product_dto.product_description
            product_vo.product_image_name = image_name
            product_vo.product_image_path = os.path.join(
                "home", "prince", "sahana_projects", "FlaskMVCProject",
                "base,static", "product_images", image_name)
            product_vo.product_quantity = product_dto.product_quantity

            timestamp = get_current_timestamp()
            product_vo.create_at = timestamp
            product_vo.modify_at = timestamp

            product_dao = ProductDAO()
            product_dao.insert_product(product_vo)
            excel_data_from_product_table()
        except Exception as e:
            raise Exception(f"Failed to insert product: {str(e)}")

    @staticmethod
    def view_product_service():
        try:
            product_dao = ProductDAO()
            product_vo_lst = product_dao.view_product()
            print(product_vo_lst)
            excel_data_from_product_table()
            return product_vo_lst

        except Exception as e:
            raise Exception(f"Failed to fetch products: {str(e)}")

    @staticmethod
    def delete_product_service(product_id):
        try:
            modify_at = get_current_timestamp()
            product_vo = ProductVO()
            product_vo.modify_at = modify_at
            product_dao = ProductDAO()
            product_dao.delete_product(product_id)
            excel_data_from_product_table()
        except Exception as e:
            raise Exception(f"Failed to delete product: {str(e)}")

    @staticmethod
    def edit_product_service(product_id):
        try:
            product_dao = ProductDAO()
            product_vo_lst, category_vo_lst, sub_category_vo_lst = product_dao.edit_product(
                product_id)
            return product_vo_lst, category_vo_lst, sub_category_vo_lst
        except Exception as e:
            raise Exception(f"Failed to edit product: {str(e)}")

    @staticmethod
    def update_product_service(product_id, product_category_id,
                               product_sub_category_id, product_dto):
        try:
            product_vo = ProductVO()
            product_vo.product_id = product_id
            product_vo.product_category_id = product_category_id
            product_vo.product_sub_category_id = product_sub_category_id
            product_vo.product_name = product_dto.product_name
            product_vo.product_price = product_dto.product_price
            product_vo.product_description = product_dto.product_description
            product_vo.product_quantity = product_dto.product_quantity

            if product_dto.product_image_name:
                if not product_dto.product_image_name.lower().endswith(
                        (".png", ".jpg", ".jpeg", ".gif")):
                    raise ValueError(
                        "Invalid file type. Allowed types: png, jpg, jpeg, gif.")

                if not os.path.exists(image_directory):
                    os.makedirs(image_directory)

                image_path = os.path.join(image_directory,
                                          product_dto.product_image_name)
                product_vo.product_image_name = product_dto.product_image_name
                product_vo.product_image_path = os.path.join("static",
                                                             "product_images",
                                                             product_dto.product_image_name)

            product_vo.modify_at = get_current_timestamp()

            product_dao = ProductDAO()
            product_dao.update_product(product_vo)
            excel_data_from_product_table()
        except Exception as e:
            raise Exception(f"Failed to update product: {str(e)}")
