import sys
import os
import logging
import logging.config
import copy
import types

# https://stackoverflow.com/questions/30249069/listing-contents-of-a-bucket-with-boto3
# import settings

__version__ = "1.0"

def identifyImage(args):
    """ http://www.blog.pythonlibrary.org/2020/02/09/how-to-check-if-a-file-is-a-valid-image-with-python/"""
    """ See https://stackoverflow.com/questions/10937350/how-to-check-type-of-files-without-extensions-in-python/24433682 """
    import imghdr

    fn = args[0]

    print imghdr.what(fn)
    

def renderTemplate(args):
    """ Usage : renderTemplte templateName inputdata """
    from jinja2 import Template, FileSystemLoader, Environment

    templateFn = args[0]
    inFn = args[1]

    logging.info('Loading %s', inFn)
    with open(inFn, 'r') as f:
            values = [i.strip() for i in f.readlines()]

    templateLoader = FileSystemLoader(searchpath="./")
    templateEnv = Environment(loader=templateLoader)

    template = templateEnv.get_template(templateFn)

    output = template.render(slotTypeName="RailLineNames",
                slotTypeVersion="1.00", slotTypeValues=values)

    print output


def listMyBuckets(args):
    import boto3
# Let's use Amazon S3
    s3 = boto3.resource('s3')
# Print out bucket names
    for bucket in s3.buckets.all():
        # print type(bucket)
        # print dir(bucket)
        print(bucket.name)


def listMyBucketsV2(args):
    """ uses s3 client """
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-creating-buckets.html
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html
    import boto3
    s3 = boto3.client('s3')

    # https://stackoverflow.com/questions/49814173/boto3-get-only-s3-buckets-of-specific-region
    for bucket in s3.list_buckets()["Buckets"]:
        # print s3.get_bucket_location(Bucket=bucket['Name'])['LocationConstraint'] == 'eu-west-1':
        print(bucket["Name"]), s3.get_bucket_location(Bucket=bucket['Name'])['LocationConstraint']

    response = s3.list_buckets()

    for b in response:
        print b.get_bucket_location()
# Output the bucket names
    print('Existing buckets:')
    for bucket in response['Buckets']:
        # print({bucket["Name"]})
        print(bucket["Name"])


def listRegions(args):
    import boto3

    ec2 = boto3.client('ec2')

# Retrieves all regions/endpoints that work with EC2
    response = ec2.describe_regions()
    print('Regions:', response['Regions'])

# Retrieves availability zones only for region of the ec2 object
    response = ec2.describe_availability_zones()
    print('Availability Zones:', response['AvailabilityZones'])



def uploadFile(args):
# bucketName = "Your S3 BucketName"
# Key = "Original Name and type of the file you want to upload into s3"
# outPutname = "Output file name(The name you want to give to the file after we upload to s3)"
    import boto3

    bucketName = args[0]
    key = args[1]
    outPutname = args[2]

    s3 = boto3.client('s3')
    s3.upload_file(key, bucketName, outPutname)


def downloadFile(args):
    """https://qiita.com/hengsokvisal/items/329924dd9e3f65dd48e7"""
# bucketName = "Your S3 BucketName"
# Key = "Original Name and type of the file you want to upload into s3"
# outPutname = "Output file name(The name you want to give to the file after we upload to s3)"
    import boto3
    import botocore

    bucketName = args[0]
    key = args[1]
    outPutname = args[2]

    try:
        s3 = boto3.client('s3')
        s3.download_file(bucketName, key, outPutname)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise


########
# SQS
########
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs.html
def sqs(args):
    import boto3
    # Print out each queue name, which is part of its ARN
    # Get the service resource
    sqs = boto3.resource('sqs')

    for queueName in args:
        queue = sqs.get_queue_by_name(QueueName=queueName)
        # You can now access identifiers and attributes
        print(queue.url)
        print(queue.attributes.get('DelaySeconds'))


def sqsList(args):
    import boto3
    # Print out each queue name, which is part of its ARN
    # Get the service resource
    sqs = boto3.resource('sqs')
    for queue in sqs.queues.all():
        print(queue.url)


def sqsPublish0(args):
    import boto3

    theTitle = args[0]
    # Get the service resource
    sqs = boto3.resource('sqs')

    # Get the queue
    queue = sqs.get_queue_by_name(QueueName='ocr-bills-details.fifo')

    # Create a new message
    response = queue.send_message(MessageBody=theTitle, MessageGroupId="neededForFIFO", MessageDeduplicationId="neededForFIFO")

    # The response is NOT a resource, but gives you a message ID and MD5
    print(response.get('MessageId'))
    print(response.get('MD5OfMessageBody'))


# Create SQS client
def sqsPublish(args):
    import boto3
    sqs = boto3.client('sqs')
    theTitle = args[0]

    queue_url = 'https://sqs.ap-southeast-2.amazonaws.com/632663685106/ocr-bills-details.fifo'

    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        # DelaySeconds=10,
        MessageAttributes={
            'Title': {
                'DataType': 'String',
                'StringValue': theTitle
            },
            'Author': {
                'DataType': 'String',
                'StringValue': 'John Grisham'
            },
            'WeeksOn': {
                'DataType': 'Number',
                'StringValue': '6'
            }
        },
        MessageGroupId="neededForFIFO",
        MessageDeduplicationId="neededForFIFO",
        MessageBody=(
            'Information about current NY Times fiction bestseller for '
            'week of 12/11/2016.'
        )
    )

    print(response['MessageId'])


def sqsReceiveDelete(args):
    import boto3

    # Create SQS client
    sqs = boto3.client('sqs')

    queue_url = 'https://sqs.ap-southeast-2.amazonaws.com/632663685106/ocr-bills-details.fifo'

    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=10,
        WaitTimeSeconds=0
    )

    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']

    print('Received and deleted message: %s' % message)

    # Delete received message from queue
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )


def _showAll(args):
    all = copy.copy(args.items())
    print "Script version", __version__

    for name, f in all:
        if isinstance(f, types.FunctionType):
            if not name.startswith("_"):
                print "******************************"
                print "Function ** %s **" % name
                print "******************************"
                if f.__doc__ is not None:
                    print '\t', f.__doc__


if __name__ == '__main__':
    REVISION = "$LastChangedRevision: 10220 $"
    if os.path.exists("logging.conf"):
        logging.config.fileConfig("logging.conf")
        logging.info("Using logging.conf for logging settings.")
    else:
        logging.basicConfig(level=logging.INFO)

    logging.info('Version =%s', REVISION)
    if len(sys.argv) < 2:
        _showAll(locals())
        os._exit(0)

    # Globals
    fnName = sys.argv[1]
    logging.info('Function *** %s ***', fnName)

    if fnName not in locals():
        logging.error("Unknown function '%s'", fnName)
        os._exit(0)

    n = locals()[fnName](args=sys.argv[2:])
    sys.stdout.flush()

    logging.info('** bye')
    os._exit(0)
