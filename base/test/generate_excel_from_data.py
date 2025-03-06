import io
import xlsxwriter
from PIL import Image


def create_excel(data_, file_name):
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()

    headers = ["Category_Name", "Price", "Quantity", "Image"]
    worksheet.write_row(0, 0, headers)

    worksheet.set_column(0, 0, 20)  # Category_Name
    worksheet.set_column(1, 1, 10)  # Price
    worksheet.set_column(2, 2, 10)  # Quantity
    worksheet.set_column(3, 3, 30)  # Image width increased

    # Write the data_ to the worksheet
    for row_num, item in enumerate(data_, 1):
        worksheet.write(row_num, 0, item['Category_Name'])
        worksheet.write(row_num, 1, item['Price'])
        worksheet.write(row_num, 2, item['Quantity'])

        # Insert the image in the worksheet
        image_data_ = item['Image']
        image_stream = io.BytesIO(image_data_)
        image = Image.open(image_stream)

        # Get image dimensions for setting row height
        image_width, image_height = image.size
        cell_width = 180  # Increased cell width in pixels
        cell_height = 120  # Increased cell height in pixels
        x_scale = cell_width / image_width
        y_scale = cell_height / image_height

        worksheet.set_row(row_num, cell_height / 0.75)

        # Convert image to a format that can be directly inserted
        output = io.BytesIO()
        image.save(output, format="PNG")
        output.seek(0)  # Rewind the buffer to the beginning

        # Insert image into the worksheet
        worksheet.insert_image(row_num, 3, "image.png",
                               {'image_data': output, 'x_scale': x_scale,
                                'y_scale': y_scale, 'positioning': 1,
                                'x_offset': 5, 'y_offset': 5})

    # Close the workbook to save the file
    workbook.close()


data_ = [
    {
        "Category_Name": "Electronics",
        "Price": 299.99,
        "Quantity": 10,
        "Image": open(
            "/images/product_images/14pro.jpg",
            "rb").read()
    },
    {
        "Category_Name": "Books",
        "Price": 19.99,
        "Quantity": 50,
        "Image": open(
            "/images/product_images/15pro.jpg",
            "rb").read()
    },
]

create_excel(data_, "image_excel.xlsx")
