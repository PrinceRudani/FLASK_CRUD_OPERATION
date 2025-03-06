import threading
import xlsxwriter

from base.com.dao.category_dao import CategoryDAO
from base.com.vo.category_vo import CategoryVO
from base.utils.generate_excel_file import excel_data_from_category_table
from base.utils.my_logger import get_logger
from base.utils.time_stamp import get_current_timestamp

logger = get_logger()
category_excel = 'base/static/category_excel_sheet/image_excel.xlsx'


class CategoryService:
    @staticmethod
    def add_category_service(category_dto_lst):
        try:
            create_at = get_current_timestamp()
            modify_at = get_current_timestamp()
            category_vo = CategoryVO()

            category_vo.category_name = category_dto_lst['category_name']
            category_vo.category_description = category_dto_lst['category_description']
            category_vo.create_at = create_at
            category_vo.modify_at = modify_at

            category_dao = CategoryDAO()
            category_dao.insert_category(category_vo)

            excel_data_from_category_table() # insert excel data

            logger.info('Insert category successfully')

        except Exception as e:
            logger.error(f"Error in add_category_service: {e}")
            raise RuntimeError(f"Error in add_category_service: {str(e)}")

    @staticmethod
    def view_category_service():
        try:
            category_dao = CategoryDAO()
            category_vo_lst = category_dao.view_category()
            logger.info(
                'view category successfully {} '.format(category_vo_lst))
            return category_vo_lst
        except Exception as e:
            raise RuntimeError(f"Error in view_category_service: {str(e)}")

    @staticmethod
    def delete_category_service(category_id):
        try:
            modify_at = get_current_timestamp()
            category_vo = CategoryVO()
            category_vo.modify_at = modify_at

            category_dao = CategoryDAO()
            category_dao.delete_category(category_id)

            excel_data_from_category_table() # delete excel data

            logger.info(
                'delete category successfully : {}'.format(category_id))
        except Exception as e:
            raise RuntimeError(f"Error in delete_category_service: {str(e)}")

    @staticmethod
    def edit_category_service(category_id):
        try:
            category_dao = CategoryDAO()
            category_vo = category_dao.edit_category(category_id)
            logger.info('edit category successfully : {}'.format(category_id))
            return category_vo
        except Exception as e:
            raise RuntimeError(f"Error in edit_category_service: {str(e)}")

    @staticmethod
    def update_category_service(category_id, category_dto_lst):
        try:
            create_at = get_current_timestamp()
            modify_at = get_current_timestamp()


            category_vo = CategoryVO()
            category_vo.category_id = category_id
            category_vo.category_name = category_dto_lst['category_name']
            category_vo.category_description = category_dto_lst['category_description']
            category_vo.create_at = create_at
            category_vo.modify_at = modify_at

            category_dao = CategoryDAO()
            updated_category = category_dao.update_category(
                category_id,
                category_vo.category_name,
                category_vo.category_description
            )

            excel_data_from_category_table() # update excel data

            logger.info(
                f'Update category successfully: ID -> {category_vo.category_id}, '
                f'Name -> {category_vo.category_name}, Description -> {category_vo.category_description}'
            )
            return updated_category
        except Exception as e:
            logger.error(f"Error in update_category_service: {str(e)}")
            raise RuntimeError(f"Error in update_category_service: {str(e)}")

