import flet as ft
import pandas as pd
import ydata_profiling

def main(page: ft.Page):
    page.title = "Data Profiling App"
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.colors.BLUE,
            secondary=ft.colors.GREEN,
            background=ft.colors.WHITE
        )
    )
    page.fonts = {
        "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap"
    }
    page.update()

    # UI Elements
    progress_bar = ft.ProgressBar(width=400, height=10, visible=False)  # Increase width and decrease height
    progress_text = ft.Text("Processing...", visible=False)
    error_text = ft.Text("", color=ft.colors.RED, visible=False)
    success_text = ft.Text("", color=ft.colors.GREEN, visible=False)
    download_button = ft.ElevatedButton("Process and Download", icon=ft.icons.DOWNLOAD, visible=False)

    df = None  # Initialize the DataFrame variable

    # Event handlers
    def on_file_picker_result(e: ft.FilePickerResultEvent):
        nonlocal df
        print("File picker result received")  # Debugging
        if e.files:
            file_path = e.files[0].path
            print(f"Selected file path: {file_path}")  # Debugging
            if not file_path.endswith('.csv'):
                error_text.value = "Please upload a CSV file."
                error_text.visible = True
                page.update()
                return

            try:
                df = pd.read_csv(file_path)
                print("DataFrame loaded successfully")  # Debugging
                if df is not None and not df.empty:
                    success_text.value = "CSV file loaded successfully."
                    success_text.visible = True
                    download_button.visible = True
                    error_text.visible = False
                    show_download_section()  # Make sure the section is visible
                else:
                    error_text.value = "Loaded file is empty or invalid."
                    error_text.visible = True
                    download_button.visible = False
                page.update()
            except Exception as ex:
                print(f"Error loading CSV file: {str(ex)}")  # Debugging
                error_text.value = f"Error loading CSV file: {str(ex)}"
                error_text.visible = True
                success_text.visible = False
                download_button.visible = False
                page.update()

    def on_save_picker_result(e: ft.FilePickerResultEvent):
        if e.path and df is not None:
            save_path = e.path
            if not save_path.endswith('.html'):
                save_path += '.html'

            progress_bar.visible = True
            progress_text.visible = True
            error_text.visible = False
            success_text.visible = False
            page.update()

            try:
                profile = ydata_profiling.ProfileReport(df, minimal=True)
                profile.to_file(save_path)
                progress_text.visible = False
                progress_bar.visible = False
                success_text.value = "Data profiling report saved successfully."
                success_text.visible = True
                page.update()
            except Exception as ex:
                print(f"Error generating report: {str(ex)}")  # Debugging
                progress_text.visible = False
                progress_bar.visible = False
                error_text.value = f"Error generating report: {str(ex)}"
                error_text.visible = True
                page.update()

    # File pickers
    file_picker = ft.FilePicker(on_result=on_file_picker_result)
    save_picker = ft.FilePicker(on_result=on_save_picker_result)
    page.overlay.append(file_picker)
    page.overlay.append(save_picker)

    # Header (Removed borders, added icon)
    header = ft.Container(
        content=ft.Row(
            [
                ft.Icon(name=ft.icons.ANALYTICS, color=ft.colors.BLUE, size=40),
                ft.Text("Data Profiling App", size=28, weight="bold", color=ft.colors.BLUE, font_family="Roboto")
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=ft.padding.all(20),  # Padding for the container
        border_radius=10,
        margin=10  # Margin outside the container
    )

    # Description
    description = ft.Text(
        "Upload your CSV file to generate a data profiling report. The report will be saved in HTML format, which can be opened in any web browser.",
        size=18,
        font_family="Roboto"
    )

    # Upload Button with Padding
    upload_button = ft.ElevatedButton(
        "Choose CSV file", 
        icon=ft.icons.UPLOAD_FILE, 
        on_click=lambda _: file_picker.pick_files(allow_multiple=False)
    )

    # Layout: Use Container for Download Section
    download_section = ft.Container(
        content=ft.Column(
            [
                progress_text,
                progress_bar,
                error_text,
                success_text,
                download_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        padding=ft.padding.all(15),  # Padding for the container
        border=ft.border.all(color=ft.colors.LIGHT_BLUE, width=2),
        border_radius=10,
        visible=False  # Initially hidden, will be shown after file upload
    )

    # Main Layout
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    header,
                    description,
                    upload_button,
                    download_section  # Encapsulated section
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=ft.padding.all(40)  # Apply padding to the entire column layout
        )
    )

    # Show download section when ready
    def show_download_section():
        download_section.visible = True
        page.update()

    download_button.on_click = lambda e: save_picker.save_file()

ft.app(target=main)
