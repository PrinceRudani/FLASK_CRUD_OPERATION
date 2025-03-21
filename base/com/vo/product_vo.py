from base import db


class ProductVO(db.Model):
    __tablename__ = 'product_table'
    product_id = db.Column('product_id', db.Integer, autoincrement=True,
                           primary_key=True)
    product_category_id = db.Column('product_category_id', db.Integer,
                                    db.ForeignKey(
                                        'category_table.category_id',
                                        ondelete="CASCADE"),
                                    nullable=False)
    product_sub_category_id = db.Column('product_sub_category_id', db.Integer,
                                        db.ForeignKey(
                                            'sub_category_table.sub_category_id',
                                            ondelete="CASCADE"),
                                        nullable=False)
    product_name = db.Column('product_name', db.String(100), nullable=False)
    product_price = db.Column('product_price', db.Float, nullable=False)
    product_description = db.Column('product_description', db.String(1000),
                                    nullable=False)
    product_image_name = db.Column('product_image_name', db.String(255),
                                   nullable=False)
    product_image_path = db.Column('product_image_path', db.String(500),
                                   nullable=False)
    product_quantity = db.Column('product_quantity', db.Integer,
                                 nullable=False)
    is_delete = db.Column('is_delete', db.Boolean, nullable=False,
                          default=False)
    create_at = db.Column('create_at', db.Integer, nullable=False)
    modify_at = db.Column('modify_at', db.Integer, nullable=True)

    def as_dict(self):
        return {
            'product_id': self.product_id,
            'product_category_id': self.product_category_id,
            'product_sub_category_id': self.product_sub_category_id,
            'product_name': self.product_name,
            'product_price': self.product_price,
            'product_description': self.product_description,
            'product_image_name': self.product_image_name,
            'product_image_path': self.product_image_path,
            'product_quantity': self.product_quantity,
            'is_delete': self.is_delete,
            'create_at': self.create_at,
            'modify_at': self.modify_at,
        }


db.create_all()
