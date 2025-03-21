from flask import render_template, request, redirect

from base import app
from base.com.dao.category_dao import CategoryDAO
from base.com.dto.subcategory_dto import SubcategoryDTO
from base.com.service.login_service import LoginService
from base.com.service.subcategory_service import SubcategoryService
from base.utils.my_logger import get_logger

ADD_SUBCATEGORY_TEMPLATE = 'subcategory_templates/addSubCategory.html'
VIEW_SUBCATEGORY_PATH = '/view_sub_category'


@app.route('/load_sub_category', methods=['GET', 'POST'])
@LoginService.login_required(role="ADMIN")
def load_sub_category():
    """Load the form for adding a new subcategory.
    
    Returns:
        rendered template: The add subcategory form template with category data
        redirect: Redirects to home page on error
    """
    try:
        category_dao = CategoryDAO()
        sub_category_vo = category_dao.view_category()
        logger = get_logger()
        logger.info('load sub category successfully')
        return render_template(ADD_SUBCATEGORY_TEMPLATE,
                               sub_category_vo=sub_category_vo)
    except Exception as e:
        logger = get_logger()
        logger.error(f"Error in load_sub_category: {str(e)}")
        return redirect('/')


@app.route('/insert_sub_category', methods=['POST', 'GET'])
@LoginService.login_required(role="ADMIN")
def insert_sub_category():
    """Insert a new subcategory. """

    try:
        subcategory_dto = SubcategoryDTO()
        subcategory_category_id = request.form.get('subCategoryCategoryId')
        subcategory_dto.sub_category_name = request.form.get('subCategoryName')
        subcategory_dto.sub_category_description = request.form.get(
            'subCategoryDescription')
        if not subcategory_category_id:
            return render_template(
                ADD_SUBCATEGORY_TEMPLATE,
                error_message="Please select a category.")
        if not subcategory_dto.sub_category_name:
            return render_template(
                ADD_SUBCATEGORY_TEMPLATE,
                error_message="Please enter a subcategory name.")
        if not subcategory_dto.sub_category_description:
            return render_template(
                ADD_SUBCATEGORY_TEMPLATE,
                error_message="Please enter a subcategory description.")

        subcategory_dto_lst = subcategory_dto.validate()
        subcategory_service = SubcategoryService()
        subcategory_service.insert_subcategory_service(subcategory_category_id,
                                                       subcategory_dto_lst)
        logger = get_logger()
        logger.info(
            'insert sub category :category id -> {}, subcategory name -> {}, '
            'sub category description -> {}'.format(subcategory_category_id,
                                                    subcategory_dto_lst.sub_category_name,
                                                    subcategory_dto_lst.sub_category_description))
        return redirect(VIEW_SUBCATEGORY_PATH)

    except Exception as e:
        logger = get_logger()
        logger.error(f"Error in insert_sub_category: {str(e)}")
        return redirect('/load_sub_category')


@app.route('/view_sub_category', methods=['GET', 'POST'])
@LoginService.login_required(role="ADMIN")
def view_sub_category():
    """View all subcategories.
    
    Returns:
        rendered template: The view subcategories template with list of subcategories
    """
    subcategory_service = SubcategoryService()
    sub_category_vo_lst = subcategory_service.view_subcategory_service()
    logger = get_logger()
    logger.info(
        'view sub category successfully {} '.format(sub_category_vo_lst))
    return render_template('subcategory_templates/viewSubCategory.html',
                           sub_category_vo_lst=sub_category_vo_lst)


@app.route('/delete_sub_category', methods=['POST'])
@LoginService.login_required(role="ADMIN")
def delete_sub_category():
    """Delete a subcategory.
    
    Deletes subcategory with ID from form data.
    
    Returns:
        redirect: Redirects back to view subcategories
    """
    sub_category_id = request.form.get('sub_category_id')
    subcategory_service = SubcategoryService()
    subcategory_service.delete_subcategory_service(sub_category_id)
    logger = get_logger()
    logger.info(
        'delete sub category successfully : {}'.format(sub_category_id))
    return redirect(VIEW_SUBCATEGORY_PATH)


@app.route('/edit_sub_category/<int:sub_category_id>', methods=['GET'])
@LoginService.login_required(role="ADMIN")
def edit_sub_category(sub_category_id):
    """Load edit form for a subcategory.
    
    Args:
        sub_category_id: ID of subcategory to edit
        
    Returns:
        rendered template: The edit subcategory form with subcategory and category data
        redirect: Redirects to view subcategories on error
    """
    try:
        subcategory_service = SubcategoryService()
        sub_category, category_vo_lst = subcategory_service.edit_subcategory_service(
            sub_category_id)
        logger = get_logger()
        logger.info(
            'edit sub category successfully : subcategory id -> {}'.format(
                sub_category_id))
        return render_template(
            'subcategory_templates/updateSubCategory.html',
            sub_category=sub_category, category_vo_lst=category_vo_lst)
    except Exception as e:
        logger = get_logger()
        logger.error(f"Error in edit_sub_category: {str(e)}")
        return redirect(VIEW_SUBCATEGORY_PATH)


@app.route('/update_sub_category/<int:sub_category_id>', methods=['POST'])
@LoginService.login_required(role="ADMIN")
def update_sub_category(sub_category_id):
    """Update a subcategory.
    
    Args:
        sub_category_id: ID of subcategory to update
        
    Takes form data for updated subcategory details.
    Validates required fields and updates subcategory through service layer.
    
    Returns:
        redirect: Redirects to view subcategories on success
        rendered template: Returns to form with error message on validation failure
        redirect: Redirects back to edit form on error
    """
    subcategory_category_id = request.form.get('subCategoryCategoryId')
    subcategory_dto = SubcategoryDTO()
    subcategory_dto.sub_category_name = (request.form.get
                                         ('subCategoryName'))
    subcategory_dto.sub_category_description = (request.form.get
                                                ('subCategoryDescription'))
    if not subcategory_category_id:
        return render_template(
            ADD_SUBCATEGORY_TEMPLATE,
            error_message="Please select a category.")
    if not subcategory_dto.sub_category_name:
        return render_template(
            ADD_SUBCATEGORY_TEMPLATE,
            error_message="Please enter a subcategory name.")
    if not subcategory_dto.sub_category_description:
        return render_template(
            ADD_SUBCATEGORY_TEMPLATE,
            error_message="Please enter a subcategory description.")
    try:
        subcategory_dto_lst = subcategory_dto.validate()
        subcategory_service = SubcategoryService()
        subcategory_service.update_subcategory_service(sub_category_id,
                                                       subcategory_category_id,
                                                       subcategory_dto_lst)
        logger = get_logger()
        logger.info(
            'update sub category successfully : subcategory id -> {}'.format(
                sub_category_id))
        return redirect(VIEW_SUBCATEGORY_PATH)
    except Exception as e:
        logger = get_logger()
        logger.error(f"Error in update_sub_category: {str(e)}")
        return redirect(f'/edit_sub_category/{sub_category_id}?')
