boto3-oversize
==============

Messages published using Amazon SNS have a [maximum size of 256KiB](https://aws.amazon.com/about-aws/whats-new/2013/06/18/amazon-sqs-announces-256KB-large-payloads/),
which can be a limitation for certain use cases. AWS provides an
[extended client library for Java](https://aws.amazon.com/about-aws/whats-new/2020/08/amazon-sns-launches-client-library-supporting-message-payloads-of-up-to-2-gb/)
that transparently uploads messages exceeding this threshold to S3 and restores them when the
messages are received. This Python package provides the same functionality for
[boto3](https://aws.amazon.com/sdk-for-python/).

## Installation

1. Create an Amazon S3 bucket that will store message payloads that exceed the maximum size.
   * While the Java library deletes payloads from S3 when they are retrieved, this is not
     appropriate when there are multiple subscribers to the topic. Instead, apply a
     [S3 lifecycle configuration](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)
     to expire the message payloads after a reasonable length of time, e.g., 14 days.
2. Install this package, e.g., `pip install boto3-oversize`.
3. Define the `OVERSIZE_PAYLOAD_BUCKET_NAME` environment variable as the name of the bucket you created;
   ensure your AWS access credentials have permission to call `PutObject` and `GetObject` in the
   root of the bucket.

## Usage

The library provides replacement implementations of the core boto3 entry points that transparently
apply the necessary changes to the SNS and SQS clients, both for the low-level client and service
resource. Simply reference `boto3_oversize` instead of `boto3`.

### Low-level client example

```python
import boto3_oversize

sns_client = boto3_oversize.client('sns')
response = sns_client.create_topic(Name='example-large-payload-topic')
sns_client.publish(TopicArn=response['TopicArn'], Message='example-message')
```

### Service resource example

```python
import boto3_oversize

sqs_client = boto3_oversize.resource('sqs')
queue = sqs_client.create_queue(QueueName='example-large-payload-queue')
messages = queue.receive_messages()
```

## Implementation

Calls to publish messages are intercepted and the message body sized check against the limit,
reduced by a small percentage to consider SNS message envelope overhead if raw message delivery is
not enabled. If the message exceeds this threshold, it is uploaded to an S3 bucket and the SNS
message replaced with the object ARN.

When receiving messages, the SQS client checks if the entire message body appears to be an S3 object
ARN. If it is, the object is retrieved from S3 and returned to the caller as the message body.
