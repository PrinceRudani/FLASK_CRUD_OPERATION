import io
import threading

import xlsxwriter
from PIL import Image

from base.com.dao.category_dao import CategoryDAO
from base.com.dao.product_dao import ProductDAO
from base.com.dao.subcategory_dao import SubCategoryDAO
from base.utils.my_logger import get_logger

category_excel_path = 'base/static/excel_sheet/category_excel_sheet.xlsx'
subcategory_excel_path = 'base/static/excel_sheet/subcategory_excel_sheet.xlsx'
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

        worksheet.set_column(0, 0, 25)
        worksheet.set_column(1, 1, 25)
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
            # print("data so far:", data_)

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
        product_worksheet = product_workbook.add_worksheet()

        # Create formats for centering text in cells
        center_format = product_workbook.add_format(
            {'align': 'center', 'valign': 'vcenter'})
        wrap_center_format = product_workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True})

        # Column headers for the Excel file
        headers = ["Category_Name", "SubCategory_Name", "Product_name",
                   "product_description", "Product_price", "Product_quantity",
                   "Product_image"]

        product_worksheet.write_row(0, 0, headers, center_format)

        # Set the width of the columns
        product_worksheet.set_column(0, 0, 25)  # Category
        product_worksheet.set_column(1, 1, 25)  # Subcategory
        product_worksheet.set_column(2, 2, 25)  # Product name
        product_worksheet.set_column(3, 3, 70)  # Description
        product_worksheet.set_column(4, 4, 20)  # Price
        product_worksheet.set_column(5, 5, 18)  # Quantity
        product_worksheet.set_column(6, 6, 35)  # Image column

        # Constants for image sizing
        IMAGE_WIDTH_PIXELS = 280  # Target width in pixels
        CELL_HEIGHT_PIXELS = 180  # Target height in pixels

        # Write the product data into the worksheet
        for row_num, item in enumerate(data_, 1):
            product_worksheet.write(row_num, 0, item['Category_Name'],
                                    center_format)
            product_worksheet.write(row_num, 1, item['SubCategory_Name'],
                                    center_format)
            product_worksheet.write(row_num, 2, item['Product_name'],
                                    center_format)
            product_worksheet.write(row_num, 3, item['product_description'],
                                    wrap_center_format)
            product_worksheet.write(row_num, 4, item['Product_price'],
                                    center_format)
            product_worksheet.write(row_num, 5, item['Product_quantity'],
                                    center_format)

            # Set row height
            product_worksheet.set_row(row_num, CELL_HEIGHT_PIXELS)

            # Process the image
            with open(item['Product_image'], "rb") as image_file:
                image_data = image_file.read()

            image_stream = io.BytesIO(image_data)
            image = Image.open(image_stream)

            # Resize image maintaining aspect ratio
            width, height = image.size
            ratio = min(IMAGE_WIDTH_PIXELS / width,
                        CELL_HEIGHT_PIXELS / height)
            new_size = (int(width * ratio), int(height * ratio))
            resized_image = image.resize(new_size, Image.Resampling.LANCZOS)

            # Prepare image for Excel
            output = io.BytesIO()
            resized_image.save(output, format="PNG")
            output.seek(0)

            # Calculate offsets for centering
            x_offset = (IMAGE_WIDTH_PIXELS - new_size[0]) // 2
            y_offset = (CELL_HEIGHT_PIXELS - new_size[1]) // 2

            # Insert the image
            product_worksheet.insert_image(
                row_num, 6, "image.png",
                {
                    'image_data': output,
                    'x_offset': x_offset,
                    'y_offset': y_offset,
                    'object_position': 1  # Move and size with cells
                }
            )

        product_workbook.close()
        logger = get_logger()
        logger.info(f"Excel file created successfully at {file_name}")

    except Exception as e:
        logger = get_logger()
        logger.error(f"Error creating Excel file: {str(e)}")
        raise


def excel_data_from_product_table():
    try:
        # Initialize an empty list to store the data
        data_ = []

        # Create an instance of ProductDAO to fetch product data
        product_dao = ProductDAO()

        # Fetch product data (this returns a list of tuples)
        product_data = product_dao.view_product()

        # Process each record (category, subcategory, and product)
        for product_vo, subcategory_vo, category_vo in product_data:
            category_name = category_vo.category_name if category_vo else 'Unknown'
            subcategory_name = subcategory_vo.sub_category_name if subcategory_vo else 'Unknown'

            data_.append({
                "Category_Name": category_name,
                "SubCategory_Name": subcategory_name,
                "Product_name": getattr(product_vo, 'product_name', 'Unknown'),
                "product_description": getattr(product_vo,
                                               'product_description',
                                               'Unknown'),
                "Product_price": getattr(product_vo, 'product_price', '0'),
                "Product_quantity": getattr(product_vo, 'product_quantity',
                                            '0'),
                "Product_image": getattr(product_vo, 'product_image_path',
                                         'No Image'),

            })
            # Print current product data for debugging
            print("\nProduct Data Entry:")
            print("-" * 50)
            print(f"Category: {category_name}")
            print(f"Subcategory: {subcategory_name}")
            print(
                f"Product: {getattr(product_vo, 'product_description', 'Unknown')}")
            print("-" * 50)

        # If data is available, start generating the Excel file
        if data_:
            logger = get_logger()
            logger.info("Starting thread to generate Excel.")
            # Adjust the file path as needed
            thread = threading.Thread(target=create_excel_for_product,
                                      args=(data_, product_excel_path))
            thread.start()
            thread.join()  # Wait for the thread to complete
            logger.info("Excel file generation completed.")
        else:
            logger = get_logger()
            logger.warning("No data to generate Excel file.")

    except Exception as e:
        # Log any exceptions that occur in the process
        logger = get_logger()
        logger.error(f"Error in excel_data_from_product_table: {e}")
