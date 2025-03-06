from base import db
from base.com.vo.category_vo import CategoryVO
from base.utils.time_stamp import get_current_timestamp


class CategoryDAO:
    @staticmethod
    def insert_category(category_vo):
        """Insert a new category into database."""
        db.session.add(category_vo)
        db.session.commit()
        print("category_vo",CategoryVO)
        return category_vo

    @staticmethod
    def view_category():
        """Retrieve all non-deleted categories."""
        category_vo_lst = CategoryVO.query.filter(
            CategoryVO.is_delete == False).all()
        print(category_vo_lst)
        return category_vo_lst

    @staticmethod
    def delete_category(category_id):
        """Soft delete a category by setting is_delete flag."""
        category = db.session.query(CategoryVO).get(category_id)
        category.modify_at = get_current_timestamp()
        category.is_delete = True
        db.session.commit()

    @staticmethod
    def edit_category(category_id):
        """Retrieve a category by ID for editing."""
        return db.session.query(CategoryVO).filter_by(
            category_id=category_id).first()

    @staticmethod
    def update_category(category_id, category_name,
                        category_description):
        """
        Updates a category in the database.
        """
        category = db.session.query(CategoryVO).get(category_id)
        category.category_name = category_name
        category.category_description = category_description
        category.modify_at = get_current_timestamp()

        db.session.commit()
        return category
