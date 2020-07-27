# simple-kafka-to-s3
Very simple Kafka to S3 uploalder


# S3 


## Set envs

```
export ACCESS_KEY_ID=<your_ceph_s3_access_key_id>
export SECRET_ACCESS_KEY=<your_ceph_s3_secret_access_key>
export CEPH_S3_ENDPOINT=<your_ceph_s3_endpoint>
export S3_BUCKET=<your_ceph_s3_bucket>
export S3_PATH=<your_ceph_s3_path>
```

E.g.

```
export ACCESS_KEY_ID=cmjJ8LbFD5wi0Jf9Jo68
export SECRET_ACCESS_KEY=GPRzLereAIUeaZq9mCaRbyVWw01c8F1crkAo3xFR
export CEPH_S3_ENDPOINT=s3-openshift-storage.apps.ocp4.stormshift.coe.muc.redhat.com
export S3_BUCKET=manuela-ml
export S3_PATH=data
```

## prep target bucket
```
s3cmd --access_key=$ACCESS_KEY_ID --secret_key=$SECRET_ACCESS_KEY --ssl  --host=$CEPH_S3_ENDPOINT  --host-bucket="$CEPH_S3_ENDPOINT/$S3_BUCKET/" mb s3://$S3_BUCKET

```
## clean target bucket

s3cmd --access_key=$ACCESS_KEY_ID --secret_key=$SECRET_ACCESS_KEY --ssl  --host=$CEPH_S3_ENDPOINT  --host-bucket="$CEPH_S3_ENDPOINT/$S3_BUCKET/" del -r s3://$S3_BUCKET/$S3_PATH


## Create secret

aws_access_key_id=<aws_s3_access_key>
aws_secret_access_key=<aws_s3_secret_key>

```
oc create secret generic kafka-to-s3-creds --from-literal=ACCESS_KEY_ID=$ACCESS_KEY_ID --from-literal=SECRET_ACCESS_KEY=$SECRET_ACCESS_KEY
oc get secret kafka-to-s3-cred
```

