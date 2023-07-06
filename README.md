# aws_s3_transfer_docker
Docker image builder for the tool to transfer s3 objects from one account to another


## Setup

This tool requires docker to use.

Alteratively, you can pull the app and use it locally if preferred


### add the following 
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

`Delete Files` : If set to ```True``` the files from the source bucket will be deleted. default is ```False```

Once you have these, you can run the following.

```
s3_account_transfer -s <source account profile> -d <destination account profile> -sb <source bucket name> -db <destination bucket name> -del <True|False>
```
```
docker run --rm -it -v ~/.aws:/root/.aws joelhutson/s3_account_transfer:latest -s <source account profile> -d <destination account profile> -sb <source bucket name> -db <destination bucket name> -del <True|False>
```

or

```
s3_account_transfer --source <source account profile> --destination <destination account profile> --source_bucket <source bucket name> --destination_bucket <destination bucket name> --delete_files <True|False>
```

```
docker run --rm -it -v ~/.aws:/root/.aws joelhutson/s3_account_transfer:latest --source <source account profile> --destination <destination account profile> --source_bucket <source bucket name> --destination_bucket <destination bucket name> --delete_files <True|False>
```

## Example

```
s3_account_transfer -s web-nonprod -d web-prod -sb my-source-bucket -db my-destination-bucket
```
```
docker run --rm -it -v ~/.aws:/root/.aws joelhutson/s3_account_transfer:latest -s web-nonprod -d web-prod -sb my-source-bucket -db my-destination-bucket
```

or

```
s3_account_transfer --source web-nonprod --destination web-prod --source_bucket my-source-bucket --destination_bucket my-destination-bucket
```
```
docker run --rm -it -v ~/.aws:/root/.aws joelhutson/s3_account_transfer:latest --source web-nonprod --destination web-prod --source_bucket my-source-bucket --destination_bucket my-destination-bucket
```


The s3 transfer applicaion will show a progress bar that should continus to progress unless there is an issue.

![Alt text]("/../main/images/example.png?raw=true "Optional Title"")