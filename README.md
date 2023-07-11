

# S3 Transfer App

The S3 Transfer App is a graphical user interface (GUI) tool for transferring files between Amazon S3 buckets. It allows you to select source and destination profiles, choose source and destination buckets, and perform file transfers with various options such as encryption.

## Folder Structure

The app follows a specific folder structure to organize the code and resources:

```
s3_transfer_app/
├── aws/
│   ├── __init__.py
│   ├── credentials.py
│   └── config.py
├── ui/
│   ├── __init__.py
│   ├── autocomplete.py
│   ├── profile_selection.py
│   ├── transfer_options.py
│   └── terminal.py
├── app.py
├── requirements.txt
└── README.md
```

- The `aws` folder contains the code for interacting with AWS services, including retrieving profiles, getting bucket lists, and performing file transfers.
- The `ui` folder contains the user interface components of the app, including autocomplete functionality, profile selection, transfer options, and the terminal widget.
- The `app.py` file is the entry point of the application that sets up the main app window and runs the event loop.
- The `Dockerfile` is used to build a Docker image for the app.
- The `requirements.txt` file lists the Python dependencies required by the app.

## Prerequisites

Before running the app, ensure that you have the following:

- Python 3.x installed on your machine.
- AWS CLI configured with the necessary profiles and credentials.
- Docker (optional, for creating a Docker image).

## Running the App

To run the app locally, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/s3_transfer_app.git`
2. Navigate to the project directory: `cd s3_transfer_app`
3. Install the Python dependencies: `pip install -r requirements.txt`
4. Run the app: `python app.py`
5. The app window should open, and you can start using the S3 Transfer App.


## Contribution

Feel free to contribute to the project by submitting bug reports, feature requests, or pull requests on the project's GitHub repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

