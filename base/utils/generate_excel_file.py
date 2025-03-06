import threading

import xlsxwriter

from base.com.dao.category_dao import CategoryDAO
from base.com.dao.product_dao import ProductDAO
from base.com.dao.subcategory_dao import SubCategoryDAO
from base.utils.my_logger import get_logger

category_excel_path = 'base/static/excel_sheet/category_excel_sheet.xlsx'
subcategory_excel_path = 'base/static/excel_sheet/subctegory_excel_sheet.xlsx'
product_excel_path = 'base/static/excel_sheet/product_excel_sheet.xlsx'


# create excel sheet for category
def create_excel_for_category(data_, file_name):
    category_workbook = xlsxwriter.Workbook(file_name)
    worksheet = category_workbook.add_worksheet()

    center_format = category_workbook.add_format(
        {'align': 'center', 'valign': 'vcenter'})

    headers = ["Category_Name", "Category_Description"]
    worksheet.write_row(0, 0, headers, center_format)

    worksheet.set_column(0, 0, 30)
    worksheet.set_column(1, 1, 80)

    for row_num, item in enumerate(data_, 1):
        worksheet.write(row_num, 0, item['Category_Name'], center_format)
        worksheet.write(row_num, 1, item['Category_Description'],
                        center_format)
    category_workbook.close()


def excel_data_from_category_table():
    data_ = []
    category_dao = CategoryDAO()
    category_data = category_dao.view_category()
    for category in category_data:
        data_.append({
            "Category_Name": category.category_name,
            "Category_Description": category.category_description,
        })
    threading.Thread(target=create_excel_for_category,
                     args=(data_, category_excel_path)).start()


# create excel sheet for subcategory
def create_excel_for_subcategory(data_, file_name):
    try:
        subcategory_workbook = xlsxwriter.Workbook(file_name)
        worksheet = subcategory_workbook.add_worksheet()

        center_format = subcategory_workbook.add_format(
            {'align': 'center', 'valign': 'vcenter'})

        headers = ["Category_Name", "SubCategory_Name",
                   "SubCategory_Description"]
        worksheet.write_row(0, 0, headers, center_format)

        worksheet.set_column(0, 0, 30)
        worksheet.set_column(1, 1, 30)
        worksheet.set_column(2, 2, 80)

        for row_num, item in enumerate(data_, 1):
            worksheet.write(row_num, 0, item['Category_Name'], center_format)
            worksheet.write(row_num, 1, item['SubCategory_Name'],
                            center_format)
            worksheet.write(row_num, 2, item['SubCategory_Description'],
                            center_format)

        subcategory_workbook.close()
        logger = get_logger()
        logger.info(f"Excel file created successfully at {file_name}")
    except Exception as e:
        logger = get_logger()
        logger.error(f"Error in create_excel_for_subcategory: {e}")


def excel_data_from_subcategory_table():
    try:
        data_ = []
        subcategory_dao = SubCategoryDAO()
        subcategory_data = subcategory_dao.view_sub_category()

        for category_vo, subcategory_vo in subcategory_data:
            data_.append({
                "Category_Name": category_vo.category_name,
                "SubCategory_Name": subcategory_vo.sub_category_name,
                "SubCategory_Description": subcategory_vo.sub_category_description,
            })
            print("data so far:", data_)

        if data_:
            logger = get_logger()
            logger.info("Starting thread to generate Excel.")
            thread = threading.Thread(target=create_excel_for_subcategory,
                                      args=(data_, subcategory_excel_path))
            thread.start()
        else:
            logger = get_logger()
            logger.warning("No data to generate Excel file.")

    except Exception as e:
        logger = get_logger()
        logger.error(f"Error in excel_data_from_subcategory_table: {e}")


def create_excel_for_product(data_, file_name):
    try:
        product_workbook = xlsxwriter.Workbook(file_name)
        worksheet = product_workbook.add_worksheet()

        center_format = product_workbook.add_format(
            {'align': 'center', 'valign': 'vcenter'})

        headers = ["Category_Name", "SubCategory_Name", "Product_name",
                   "Product_price", "Product_quantity", "Product_image"]

        worksheet.write_row(0, 0, headers, center_format)

        worksheet.set_column(0, 0, 30)
        worksheet.set_column(1, 1, 30)
        worksheet.set_column(2, 2, 80)
        worksheet.set_column(3, 3, 10)
        worksheet.set_column(4, 4, 10)
        worksheet.set_column(5, 5, 100)

        for row_num, item in enumerate(data_, 1):
            worksheet.write(row_num, 0, item['Category_Name'], center_format)
            worksheet.write(row_num, 1, item['SubCategory_Name'],
                            center_format)
            worksheet.write(row_num, 2, item['Product_name'], center_format)
            worksheet.write(row_num, 3, item['Product_price'], center_format)
            worksheet.write(row_num, 4, item['Product_quantity'],
                            center_format)
            worksheet.write(row_num, 5, item['Product_image'], center_format)
            print("data so far:", data_)

        product_workbook.close()
        logger = get_logger()
        logger.info(f"Excel file created successfully at {file_name}")
    except Exception as e:
        logger = get_logger()
        logger.error(f"Error in create_excel_for_subcategory: {e}")


def excel_data_from_product_table():
    try:
        data_ = []
        product_dao = ProductDAO()
        product_data = product_dao.view_product()

        for category_vo, subcategory_vo, product_vo in product_data:
            print(f"Category VO: {category_vo}")
            print(f"Subcategory VO: {subcategory_vo}")
            print(f"Product VO: {product_vo}")

            data_.append({
                "Category_Name": category_vo.category_name,
                "SubCategory_Name": subcategory_vo.sub_category_name,
                "Product_name": product_vo.product_name,
                "Product_price": product_vo.product_price,
                "Product_quantity": product_vo.product_quantity,
                "Product_image": product_vo.product_image,
            })

        # If data is available, start generating the Excel file
        if data_:
            logger = get_logger()
            logger.info("Starting thread to generate Excel.")
            # Ensure the correct target function and path for the Excel file
            thread = threading.Thread(target=create_excel_for_product,
                                      args=(data_,
                                            product_excel_path))  # Adjust the file path as needed
            thread.start()
            thread.join()  # Wait for the thread to complete
            logger.info("Excel file generation completed.")
        else:
            logger = get_logger()
            logger.warning("No data to generate Excel file.")

    except Exception as e:
        logger = get_logger()
        logger.error(f"Error in excel_data_from_product_table: {e}")
