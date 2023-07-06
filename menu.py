import argparse
import sys
import functions


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--source_profile",
        help="Source Profile.  The profile that contains the data that needs to be transferred",
        required=True,
    )

    parser.add_argument(
        "-d",
        "--destination_profile",
        help="Destination Profile. The profile that requires the data to be transferred to it",
        required=True,
    )

    parser.add_argument(
        "-sb",
        "--source_bucket",
        help="Source Bucket. The bucket that contains the data that needs to be downloaded",
        default="ap-southeast-2",
        required=True,
    )

    parser.add_argument(
        "-db",
        "--destination_bucket",
        help="Destination Bucket, The destination bucket that the date will be transferred to",
        required=True,
    )

    parser.add_argument(
        "-del",
        "--delete_files",
        help="Delete Files, If set to true, the files in the source bucket will be deleted after they have successfully been uploaded to new bucket",
        required=False,
        default=False
    )




    # initialize variables
    args = parser.parse_args(sys.argv[1:])

    source = args.source_profile
    destination = args.destination_profile
    source_bucket = args.source_bucket
    destination_bucket = args.destination_bucket
    delete_files = args.delete_files


    # Start the app when all params are available
    functions.transfer(source,destination,source_bucket,destination_bucket,delete_files)
