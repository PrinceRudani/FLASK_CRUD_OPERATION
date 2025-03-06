import io
import xlsxwriter
from PIL import Image


def create_excel(data_, file_name):
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()

    center_format = workbook.add_format(
        {'align': 'center', 'valign': 'vcenter'})

    headers = ["Category_Name", "Price", "Quantity", "Image"]
    worksheet.write_row(0, 0, headers, center_format)

    worksheet.set_column(0, 0, 20)  # Category_Name width
    worksheet.set_column(1, 1, 10)  # Price width
    worksheet.set_column(2, 2, 10)  # Quantity width

    cell_width = 17  # Width of the cell in Excel units
    cell_height = 80  # Row height in pixels

    worksheet.set_column(3, 3, cell_width)  # Set column width for the image

    for row_num, item in enumerate(data_, 1):
        worksheet.write(row_num, 0, item['Category_Name'], center_format)
        # worksheet.write(row_num, 1, item['Price'], center_format)
        worksheet.write(row_num, 1, item['Category_Description'],
                        center_format)

        image_data_ = item['Image']
        image_stream = io.BytesIO(image_data_)
        image = Image.open(image_stream)

        # Resize the image to fit the cell size
        image = image.resize((cell_width * 7, cell_height))

        worksheet.set_row(row_num, cell_height)  # Set row height to match image height

        output = io.BytesIO()
        image.save(output, format="PNG")
        output.seek(0)

        # Calculate the x_offset to center the image within the cell
        x_offset = (cell_width * 7 - image.size[0])//3   # Center the image
        # horizontally

        # Insert the image with proper x_offset to center it
        worksheet.insert_image(row_num, 3, "image.png",
                               {'image_data': output, 'positioning': 1,
                                'x_offset': x_offset, 'y_offset': 0,
                                'x_scale': 1, 'y_scale': 1})

    workbook.close()


# data_ = [
#     {
#         "Category_Name": "Electronics",
#         "Price": 299.99,
#         "Quantity": 10,
#         "Image": open(
#             "/home/prince/sahana_projects/FlaskMVCProject/base/static/product_images/14pro.jpg",
#             "rb").read()
#     },
#     {
#         "Category_Name": "Books",
#         "Price": 19.99,
#         "Quantity": 50,
#         "Image": open(
#             "/home/prince/sahana_projects/FlaskMVCProject/base/static/product_images/15pro.jpg",
#             "rb").read()
#     },
#     {
#         "Category_Name": "Books",
#         "Price": 19.99,
#         "Quantity": 50,
#         "Image": open(
#             "/home/prince/sahana_projects/FlaskMVCProject/base/static/product_images/jacket.jpg",
#             "rb").read()
#     },
# ]

# create_excel(data_, "image_excel.xlsx")
