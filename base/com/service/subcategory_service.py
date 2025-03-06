from base.com.dao.subcategory_dao import SubCategoryDAO
from base.com.vo.subcategory_vo import SubcategoryVO
from base.utils.generate_excel_file import excel_data_from_subcategory_table
from base.utils.my_logger import get_logger
from base.utils.time_stamp import get_current_timestamp

logger = get_logger()


class SubcategoryService:
    @staticmethod
    def insert_subcategory_service(subcategory_category_id,
                                   subcategory_dto_lst):
        create_at = get_current_timestamp()
        modify_at = get_current_timestamp()

        sub_category_vo = SubcategoryVO()
        sub_category_vo.subcategory_category_id = subcategory_category_id
        sub_category_vo.sub_category_name = subcategory_dto_lst.sub_category_name
        sub_category_vo.sub_category_description = subcategory_dto_lst.sub_category_description
        sub_category_vo.create_at = create_at
        sub_category_vo.modify_at = modify_at

        sub_category_dao = SubCategoryDAO()
        sub_category_dao.insert_sub_category(sub_category_vo)

        excel_data_from_subcategory_table()
        #
        logger.info(
            f"Subcategory inserted: category_id={subcategory_category_id}, name={subcategory_dto_lst.sub_category_name}")

    @staticmethod
    def view_subcategory_service():
        sub_category_dao = SubCategoryDAO()
        sub_category_vo_lst = sub_category_dao.view_sub_category()
        logger.info("Retrieved subcategory list")
        return sub_category_vo_lst

    @staticmethod
    def delete_subcategory_service(sub_category_id):
        modify_at = get_current_timestamp()
        sub_category_vo = SubcategoryVO()
        sub_category_vo.modify_at = modify_at
        sub_category_dao = SubCategoryDAO()
        sub_category_dao.delete_sub_category(sub_category_id)

        excel_data_from_subcategory_table()

        logger.info(f"Subcategory deleted: id={sub_category_id}")

    @staticmethod
    def edit_subcategory_service(sub_category_id):
        sub_category_dao = SubCategoryDAO()

        sub_category, category_vo_lst = sub_category_dao.edit_sub_category(
            sub_category_id)
        logger.info(f"Retrieved subcategory for editing: id={sub_category_id}")
        return sub_category, category_vo_lst

    @staticmethod
    def update_subcategory_service(sub_category_id,
                                   subcategory_category_id,
                                   subcategory_dto_lst):
        modify_at = get_current_timestamp()

        sub_category_vo = SubcategoryVO()
        sub_category_vo.sub_category_id = sub_category_id
        sub_category_vo.subcategory_category_id = subcategory_category_id
        sub_category_vo.sub_category_name = subcategory_dto_lst.sub_category_name
        sub_category_vo.sub_category_description = subcategory_dto_lst.sub_category_description

        sub_category_vo.modify_at = modify_at

        sub_category_dao = SubCategoryDAO()
        sub_category_dao.update_sub_category(sub_category_vo)
        excel_data_from_subcategory_table()
        logger.info(
            f"Subcategory updated: id={sub_category_id}, name={subcategory_dto_lst.sub_category_name}")
