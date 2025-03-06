import os

from flask import request, redirect, render_template, jsonify

from base import app
from base.com.dao.category_dao import CategoryDAO
from base.com.dao.subcategory_dao import SubCategoryDAO
from base.com.dto.product_dto import ProductDTO
from base.com.service.login_service import LoginService
from base.com.service.product_service import ProductService
from base.utils import my_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum,ResponseMessageEnum

logger = my_logger.get_logger()

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
ADD_PRODUCT_TEMPLATE = "product_templates/addProduct.html"


@app.route('/load_product')
@LoginService.login_required(role="ADMIN")
def load_product():
    try:
        category_dao = CategoryDAO()
        category_vo_lst = category_dao.view_category()
        sub_category_dao = SubCategoryDAO()
        sub_category_vo_lst = sub_category_dao.view_sub_category()
        logger.info('load product successfully')
        return render_template(ADD_PRODUCT_TEMPLATE,
                               category_vo_lst=category_vo_lst,
                               sub_category_vo_lst=sub_category_vo_lst)
    except Exception as e:
        logger.error(f"Error in load_product: {str(e)}")
        return render_template(ADD_PRODUCT_TEMPLATE,
                               error_message=ResponseMessageEnum.UNEXPECTED_ERROR_MESSAGE)


@app.route('/ajax_load_subcategory')
@LoginService.login_required(role="ADMIN")
def ajax_load_subcategory():
    try:
        product_category_id = request.args.get('product_category_id')
        product_service = ProductService()
        sub_cat = product_service.ajax_product_service(
            product_category_id)

        logger.info('ajax load subcategory successfully')
        return jsonify([i.as_dict() for i in sub_cat])
    except Exception as e:
        logger.error(f"Error in ajax_load_subcategory: {str(e)}")
        return jsonify({"error": ResponseMessageEnum.UNEXPECTED_ERROR_MESSAGE}), 500


@app.route("/insert_product", methods=["POST"])
@LoginService.login_required(role="ADMIN")
def insert_product():
    try:
        product_category_id = request.form.get("product_category_id")
        product_sub_category_id = request.form.get(
            "product_sub_category_id")
        product_name = request.form.get("productName")
        product_description = request.form.get("productDescription")
        product_price = request.form.get("productPrice")
        product_quantity = request.form.get("productQuantity")
        product_image = request.files.get("productImage")

        if not product_image:
            return render_template(
                ADD_PRODUCT_TEMPLATE,
                error_message="Please upload an image."
            )

        if not product_image.filename.lower().endswith(
                (".png", ".jpg", ".jpeg", ".gif")):
            return render_template(
                ADD_PRODUCT_TEMPLATE,
                error_message="Invalid file type. Allowed types: png, jpg, jpeg, gif."
            )

        image_name = product_image.filename
        image_directory = os.path.join("base", "static", "product_images")

        if not os.path.exists(image_directory):
            os.makedirs(image_directory)
        image_path = os.path.join(image_directory, image_name)
        product_image.save(image_path)

        product_dto = ProductDTO(
            product_name=product_name,
            product_description=product_description,
            product_price=product_price,
            product_quantity=product_quantity,
            product_image_name=image_name,
            product_image_path=image_path
        )
        product_dto.validate()

        product_service = ProductService()
        product_service.insert_product_service(product_category_id,
                                               product_sub_category_id,
                                               product_image, product_dto)

        logger.info('Product inserted successfully.')
        return redirect("/view_product")
    except Exception as e:
        logger.error(f"Error in insert_product: {str(e)}")
        print("Error occurred:", str(e))  # Debugging print statement
        return render_template(ADD_PRODUCT_TEMPLATE,
                               error_message=HttpStatusCodeEnum.OK)


@app.route('/view_product', methods=['GET', 'POST'])
@LoginService.login_required(role="ADMIN")
def view_products():
    try:
        product_service = ProductService()
        product_vo_lst = product_service.view_product_service()
        logger.info('view product successfully')
        return render_template('product_templates/viewProduct.html',
                               product_vo_lst=product_vo_lst)
    except Exception as e:
        logger.error(f"Error in view_products: {str(e)}")
        return render_template("product_templates/viewProduct.html",
                               error_message=ResponseMessageEnum.UNEXPECTED_ERROR_MESSAGE)


@app.route('/delete_product', methods=['POST'])
@LoginService.login_required(role="ADMIN")
def delete_product():
    try:
        product_id = request.form.get("product_id")
        product_service = ProductService()
        product_service.delete_product_service(product_id)
        logger.info('delete product successfully')
        return redirect('/view_product')
    except Exception as e:
        logger.error(f"Error in delete_product: {str(e)}")
        return render_template("product_templates/viewProduct.html",
                               error_message=ResponseMessageEnum.UNEXPECTED_ERROR_MESSAGE)


@app.route('/edit_product/<int:product_id>', methods=['GET'])
@LoginService.login_required(role="ADMIN")
def edit_product(product_id):
    try:
        product_service = ProductService()
        product_vo_lst, category_vo_lst, sub_category_vo_lst = product_service.edit_product_service(
            product_id)
        logger.info('edit product successfully')
        return render_template(
            'product_templates/updateProduct.html',
            product_vo_lst=product_vo_lst,
            category_vo_lst=category_vo_lst,
            sub_category_vo_lst=sub_category_vo_lst
        )
    except Exception as e:
        logger.error(f"Error in edit_product: {str(e)}")
        return render_template('product_templates/updateProduct.html',
                               error_message=ResponseMessageEnum.UNEXPECTED_ERROR_MESSAGE)


@app.route('/update_product/<int:product_id>', methods=['POST'])
@LoginService.login_required(role="ADMIN")
def update_product(product_id):
    try:
        product_category_id = request.form.get("productCategoryId")
        product_sub_category_id = request.form.get(
            "productSubCategoryId")
        product_name = request.form.get("productName")
        product_description = request.form.get("productDescription")
        product_price = request.form.get("productPrice")
        product_quantity = request.form.get("productQuantity")
        product_image = request.files.get("productImage")

        image_name = None
        image_path = None

        if product_image and product_image.filename:
            image_name = product_image.filename
            image_directory = os.path.join("base", "static",
                                           "product_images")

            if not os.path.exists(image_directory):
                os.makedirs(image_directory)

            image_path = os.path.join(image_directory, image_name)
            product_image.save(image_path)

        product_dto = ProductDTO(
            product_name=product_name,
            product_description=product_description,
            product_price=product_price,
            product_quantity=product_quantity,
            product_image_name=image_name,
            product_image_path=image_path
        )
        product_dto.update_validate()

        product_service = ProductService()
        product_service.update_product_service(product_id,
                                               product_category_id,
                                               product_sub_category_id,
                                               product_dto)

        logger.info('Product updated successfully')
        return redirect('/view_product')

    except ValueError as ve:
        return render_template(ADD_PRODUCT_TEMPLATE,
                               error_message=str(ve))
    except Exception as e:
        logger.error(f"Error in update_product: {str(e)}")
        return render_template(ADD_PRODUCT_TEMPLATE,
                               error_message=ResponseMessageEnum.UNEXPECTED_ERROR_MESSAGE)
