import flet as ft
import LimaController as lc  # ADDED IMPORT CALL TO LIMA CONTROLLER
from flet import theme  # ADDED IMPORT FOR FLET THEME
from datetime import datetime  # Added import for datetime module

last_save_time = "" # set to current date

def create_counter(quantity):
    # Create text field for quantity with plus and minus buttons
    quantity_text = ft.TextField(value=str(quantity), text_align=ft.TextAlign.RIGHT, width=70)

    def minus_click(e):
        quantity_text.value = str(max(0, int(quantity_text.value) - 1))
        quantity_text.update()

    def plus_click(e):
        quantity_text.value = str(int(quantity_text.value) + 1)
        quantity_text.update()

    minus_button = ft.IconButton(ft.icons.REMOVE, on_click=minus_click)
    plus_button = ft.IconButton(ft.icons.ADD, on_click=plus_click)

    # Arrange plus and minus buttons and text field in a row layout
    counter_row = ft.Row(
        controls=[minus_button, quantity_text, plus_button],
        alignment=ft.MainAxisAlignment.CENTER,  # Align buttons and text field in the center
    )

    # Create the counter container
    counter_container = ft.Container(
        content=counter_row,
        width=200,  # Adjust width as needed
        height=50,
        border_radius=5,
        bgcolor=ft.colors.BLACK12,  # Adjust color as needed
        padding=10,
        margin=5,
    )
    return counter_container

def create_container(row):
    # Unpack row data
    item_id, item_name, item_size, quantity = row  ## the item_id is currently unused, but for any future changes, item_id is a string, NOT A INT
    item_name = item_name.replace("'", "") ## ADDED format your text chris!!! this was suppose to be UI code, cant be anywhere else since extracting strings from lists makes strings have that stupid '' apostrophes around it
    item_size  = item_size.replace("'", "")  ## ADDED ditto above
    ## the previous statement that the controller cannot send strings without the ' apostrophes might be incorrect, but having this code in GUI is good for extra error checking regardless of whatever happens to strings
    # Create pretext for labels
    name_label = ft.Text(f"Name: {item_name}")
    size_label = ft.Text(f"Size: {item_size}")

    # Create the counter container
    counter_container = create_counter(quantity)

    # Combine labels and counter container in a column layout
    content = ft.Column(
        controls=[name_label, size_label, counter_container],  # Controller needs this back
        alignment=ft.MainAxisAlignment.START  # Align to the left side
    )

    # Create the main container
    container = ft.Container(
        content=content,
        width=1500,  # Adjust width as needed
        height=150,
        border_radius=5,
        bgcolor=ft.colors.WHITE,
        padding=10,
        margin=10,
    )
    return container

def main(page: ft.Page):
    global last_save_time

    # Set the Flet page theme
    page.theme = theme.Theme(color_scheme_seed="Blue")
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_height, page.window_width = 1000, 1500

    # Update the page to reflect theme changes
    page.update()

    # Load and add the image
    image_path = "Logo.png"  # Update with the filename of your image
    image = ft.Image(src=image_path, width=300, height=300)  # Adjust width and height as needed

    # Create a button to add a new item
    add_item_button = ft.ElevatedButton("Add Item", on_click=lambda e: open_add_item_dialog(e, page))
    
    # Create a button to save changes
    save_changes_button = ft.ElevatedButton("Save Changes", on_click=lambda e: save_new_item(page))

    # Create a button to display LIMA history
    lima_history_button = ft.ElevatedButton("LIMA History", on_click=lambda e: display_lima_history(page))

    # Create a container for the image and buttons
    header_row = ft.Row(
        controls=[image, add_item_button, save_changes_button, lima_history_button],
        alignment=ft.MainAxisAlignment.START,
    )

    # Add the header container to the page
    page.add(header_row)

    ## ADDED LimaController.py integration
    collection = []
    for row in lc.sendAvailableLiquors():
        container = create_container(row)
        collection.append(container)

    container_names = collection

    # Function to open the add item dialog
    def open_add_item_dialog(event, page):
        # Define labels for each text field
        labels = ["Item Name:", "Item Size:", "Quantity:"]

        # Create a list to hold the label and input field pairs
        input_fields = []

        # Create labels and input fields
        for index, label_text in enumerate(labels):
            label = ft.Text(label_text)
            # Use dropdown for size input
            if label_text == "Item Size:":
                dropdown_options = [
                    ft.dropdown.Option("50 mL"),
                    ft.dropdown.Option("100 mL"),
                    ft.dropdown.Option("200 mL"),
                    ft.dropdown.Option("375 mL"),
                    ft.dropdown.Option("750 mL"),
                    ft.dropdown.Option("1 L"),
                    ft.dropdown.Option("1.5 L"),
                    ft.dropdown.Option("1.75 L"),
                ]
                input_field = ft.Dropdown(options=dropdown_options, width=150)
            else:
                input_field = ft.TextField(value="", text_align=ft.TextAlign.LEFT, width=150)
            input_fields.append(ft.Row([label, input_field]))  # Combine label and input field in a row

        # Define the actions (buttons) of the alert dialog
        actions = [
            ft.TextButton("Save Item", on_click=lambda e: save_item(page, input_fields)),
            ft.TextButton("Cancel", on_click=lambda e: close_dialog(page))
        ]

        # Arrange the labels and input fields in a column layout
        content = ft.Column(
            controls=input_fields,  # List containing label-input field pairs
            spacing=10  # Adjust spacing between labels and input fields
        )

        # Create the alert dialog
        dlg = ft.AlertDialog(
            title=ft.Text("Add New Item"),
            content=content,
            actions=actions
        )

        # Open the alert dialog
        page.dialog = dlg
        dlg.open = True
        page.update()

    def save_item(page, input_fields=None):  ### this method saves a new item entry(???)
        if input_fields:
            item_name = input_fields[0].controls[1].value
            item_size = input_fields[1].controls[1].value
            quantity = input_fields[2].controls[1].value

            # Create a new container for the new item
            new_row = (None, item_name, item_size, int(quantity))
            new_container = create_container(new_row)

            # Add the new container to the list of containers
            container_names.append(new_container)

            # Close the dialog
            close_dialog(page)



    # Function to close the dialog
    def close_dialog(page):
        # Close the alert dialog if open
        if page.dialog:
            page.dialog.open = False
            page.update()

    def save_new_item(page):  ## does not save a new "item" but rather just saves every single item container currently displayed in the UI
        global last_save_time
        # Record the current date and time
        last_save_time = datetime.now()
        lc.ContainerUnbundle(container_names)  ## this should be a method call to Controller that sends the containers generated by the previous method call, line 93

        # Close the dialog
        close_dialog(page)

        # Record the current date and time

        # Display an alert indicating changes have been saved
        alert = ft.AlertDialog(
            title=ft.Text("Changes Saved"),
            content=ft.Text("The changes have been saved."),
            actions=[ft.TextButton("OK", on_click=lambda e: close_alert(page))]
        )
        page.dialog = alert
        alert.open = True
        page.update()

    def close_alert(page):
        page.dialog.open = False
        page.update()

    def get_lima_history_text():  ## is the order hisotry string all of it every single one
        return lc.sendOrderHistory()  ## this is a method call to get order hisotry strings

    # Function to update the LIMA History alert with the current date and time
    def update_lima_history_alert(new_text):
        global last_save_time
        if not last_save_time:
            current_time_str = "n/a"
        else:
            current_time_str = last_save_time.strftime("%Y-%m-%d %H:%M:%S")
        new_text += f"\nLast saved at: {current_time_str}"
        alert = page.dialog
        if alert:
            alert.content.text = new_text  # Update the content of the alert
            page.update()

    # Function to display LIMA history
    def display_lima_history(page):
        lima_history_text = get_lima_history_text()
        update_lima_history_alert(lima_history_text)
        last_save_time_text = last_save_time.strftime("%Y-%m-%d %H:%M:%S") if last_save_time else lc.sendLatestOrderTime()
        ## the last save time is either the time the user clicked "save changes" or the last time the order history was updated according to the controller
        alert_content = ft.Column(
            controls=[
                ft.Text(lima_history_text),
                ft.Text(f"Last Save Time: {last_save_time_text}")
            ]
        )
        alert = ft.AlertDialog(
            title=ft.Text("LIMA History"),
            content=alert_content,
            actions=[ft.TextButton("OK", on_click=lambda e: close_alert(page))]
        )
        page.dialog = alert
        alert.open = True
        page.update()

    # Create a Column to contain the containers and enable scrolling for the whole page
    containers_column = ft.Column(
        controls=container_names,
        scroll=ft.ScrollMode.ALWAYS,  # Enable scrolling always
        expand=True  # Ensure the column expands to fill available space
    )

    # Add the Column to the page
    page.add(containers_column)

# Start the Flet app
ft.app(main)
