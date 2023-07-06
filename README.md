# aws_s3_transfer_docker
Docker image builder for the tool to transfer s3 objects from one account to another


## Setup

To use the tool you first need to add the following to your `.zshrc` file (Or whatever your preferred environment is).

```
s3_account_transfer(){
        docker run --rm -it \
        -v ~/.aws:/root/.aws \
        joelhutson/s3_account_transfer:latest \
	$@
}
```
Restart your terminal environment when complete


## How to

Once this is setup, you will need the following

`Source Profile` : The profile that contains the data that needs to be transferred

`Destination Profile` : The profile that requires the data to be transferred to it

`Source Bucket` : The bucket that contains the data that needs to be downloaded

`Destination Bucket` : The destination bucket that the date will be transferred to

Once you have these, you can run the following.

```s3_account_transfer <source account profile> -d <destination account profile> -sb <source bucket name> -db <destination bucket name>```

or

```s3_account_transfer --source <source account profile> --destination <destination account profile> --source_bucket <source bucket name> --destination_bucket <destination bucket name>```



## Example

```s3_account_transfer -s web-nonprod -d web-prod -sb my-source-bucket -db my-destination-bucket```

or

```s3_account_transfer --source web-nonprod --destination web-prod --source_bucket my-source-bucket --destination_bucket my-destination-bucket```
