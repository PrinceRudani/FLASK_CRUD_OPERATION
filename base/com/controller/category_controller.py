from flask import render_template, request, redirect, session
from marshmallow import ValidationError

from base import app
from base.com.dto.category_dto import CategoryDTO
from base.com.service.category_service import CategoryService
from base.com.service.login_service import LoginService, static_variables
from base.utils import my_logger
from base.com.service.custome_service import AppServices
from base.custom_enum.http_enum import ResponseMessageEnum, HttpStatusCodeEnum

VIEW_CATEGORY_URL = '/view_category'

logger = my_logger.get_logger()

@app.route('/load_category')
@LoginService.login_required(role=static_variables.ADMIN_ROLE)
def load_category():
    """Render category add form."""
    try:
        user_name = session.get('user_name', 'Guest')
        logger.info('Load category successfully')
        return render_template("category_templates/addCategory.html",
                               user_name=user_name)
    except Exception as e:
        logger.error(f'Error loading category: {str(e)}')
        response = AppServices.app_response(
            HttpStatusCodeEnum.INTERNAL_SERVER_ERROR,
            ResponseMessageEnum.INTERNAL_SERVER_ERROR)
        return AppServices.handle_exception(response,is_raise=True)


@app.route('/insert_category', methods=['POST', 'GET'])
@LoginService.login_required(role=static_variables.ADMIN_ROLE)
def insert_category():
    """Add new category to system."""
    try:
        category_dto = CategoryDTO()
        data = {
            'category_name': request.form.get('categoryName').strip() or None,
            'category_description': request.form.get(
                'categoryDescription').strip() or None
        }
        if not data['category_name'] or not data['category_description']:
            return render_template('category_templates/addCategory.html',
                                   errors="Please fill in both fields.")

        category_dto_lst = category_dto.load(data)
        category_service = CategoryService()
        category_service.add_category_service(category_dto_lst)
        logger.info(
            f'Category inserted successfully: Name -> {category_dto_lst["category_name"]},'
            f' Description -> {category_dto_lst["category_description"]}')
        return redirect(VIEW_CATEGORY_URL)

    except ValidationError as ve:
        logger.error(f'Validation error while inserting category: {str(ve)}')
        return render_template('category_templates/addCategory.html',
                               errors=str(ve))
    except Exception as e:
        logger.error(f'Error inserting category: {str(e)}')
        response = AppServices.app_response(
            HttpStatusCodeEnum.INTERNAL_SERVER_ERROR,
            ResponseMessageEnum.INTERNAL_SERVER_ERROR)
        return AppServices.handle_exception(response, is_raise=True)


@app.route('/view_category', methods=['POST', 'GET'])
@LoginService.login_required(role=static_variables.ADMIN_ROLE)
def view_category():
    """Display all categories."""
    try:
        category_service = CategoryService()
        category_dto_lst = category_service.view_category_service()
        logger.info(f'View category: {category_dto_lst}')
        return render_template('category_templates/viewCategory.html',
                               category_dto_lst=category_dto_lst)
    except Exception as e:
        logger.error(f"Error viewing categories: {str(e)}")
        response = AppServices.app_response(
            HttpStatusCodeEnum.INTERNAL_SERVER_ERROR,
            ResponseMessageEnum.INTERNAL_SERVER_ERROR)
        return AppServices.handle_exception(response, is_raise=True)


@app.route('/delete_category', methods=['POST'])
@LoginService.login_required(role=static_variables.ADMIN_ROLE)
def delete_category():
    """Soft delete a category."""
    try:
        category_id = request.form.get('category_id')
        category_service = CategoryService()
        category_service.delete_category_service(category_id)
        return redirect(VIEW_CATEGORY_URL)
    except Exception as e:
        logger.error(f"Error deleting category: {str(e)}")
        return redirect(VIEW_CATEGORY_URL)


@app.route('/edit_category', methods=['GET'])
@LoginService.login_required(role=static_variables.ADMIN_ROLE)
def edit_category():
    """Load category edit form."""
    try:
        category_id = request.args.get('category_id')
        category_service = CategoryService()
        category = category_service.edit_category_service(category_id)
        return render_template('category_templates/updateCategory.html',
                               category=category)
    except Exception as e:
        logger.error(f"Error editing category: {str(e)}")
        return redirect(VIEW_CATEGORY_URL)


@app.route('/update_category', methods=['POST'])
@LoginService.login_required(role=static_variables.ADMIN_ROLE)
def update_category():
    """Update existing category."""
    category_id = None
    try:
        category_id = int(request.form.get('category_id'))
        category_dto = CategoryDTO()
        data = {
            'category_name': request.form.get('categoryName'),
            'category_description': request.form.get('categoryDescription')
        }

        if not data['category_name'] or not data['category_description']:
            return redirect(f'/edit_category?category_id={category_id}')

        category_dto_lst = category_dto.load(data)
        category_service = CategoryService()
        category_service.update_category_service(category_id, category_dto_lst)
        return redirect(VIEW_CATEGORY_URL)

    except Exception as e:
        logger.error(f'Error updating category: {str(e)}')
        return redirect(f'/edit_category?category_id={category_id or "error"}')
