# S3 Transfer Application

This application provides a graphical user interface (GUI) for transferring files between Amazon S3 buckets. It allows you to select source and destination profiles, choose buckets, and perform various transfer options.

## Folders

- `app/`: Contains the application code and resources.
    - `app.py`: Entry point of the application.
    - `aws.py`: AWS-related functions for retrieving profiles and bucket information.
    - `autocomplete.py`: Autocomplete combobox for profile selection.
    - `encryption.py`: Functions for encryption of bucket objects.
    - `gui.py`: GUI components and layout definition.
    - `profile_selection.py`: Handles source and destination profile selection.
    - `s3_operations.py`: Functions for copying, deleting, and encrypting S3 objects.
    - `s3_transfer_app.py`: Main application class and event callbacks.
    - `source_destination_profiles.py`: Input fields for source and destination profiles.
    - `terminal.py`: Terminal-like text box for displaying logs and errors.
    - `transfer_options.py`: Handles transfer options like delete source and encryption.

## Functionality

- Source and Destination Profile Selection: Users can select source and destination profiles from a dropdown populated with profiles from `.aws/config` and `.aws/credentials` files.
- Autocomplete: The profile selection dropdown provides autocomplete functionality based on the available profiles.
- Terminal Window: The application includes a terminal-like text box for displaying logs and errors.
- Bucket Selection: Upon selecting the source and destination profiles, the application checks for available buckets and populates dropdowns with bucket names for selection.
- Transfer Options: Users can choose to delete the source objects after transfer and enable encryption for the destination bucket.
- Encryption: The application supports encryption of bucket objects using the appropriate encryption algorithm (AES256 or KMS).
- User Interface: The GUI provides an intuitive interface for profile selection, bucket selection, transfer options, and terminal output.

## How to Use

1. Ensure you have the necessary AWS credentials set up in the `.aws/config` and `.aws/credentials` files.
2. Open the application by running `app.py`.
3. Select the source and destination profiles from the dropdowns.
4. If available, choose the source and destination buckets from the dropdowns.
5. Enable transfer options such as deleting the source objects and encryption if desired.
6. Click the "Transfer" button to initiate the file transfer.
7. Monitor the terminal window for logs and errors.
8. Close the application when finished.

Please note that this is a simplified explanation of the application's functionality. Refer to the code and specific file documentation for more detailed information on each component and function.

