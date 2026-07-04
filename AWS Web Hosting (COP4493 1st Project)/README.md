# COP4493-AWS Academy Cloud Computing Fundamentals Project-1

Provided HTML and CSS files are uploaded here.

When a change is made on `main` branch, `.github/workflows/deployment.yml` will be triggered and upload all these objects to the S3 bucket.
To update the website, the EC2 instance should be restarted and S3 instance should be synchronized again using the following in the EC2 instance terminal;

```bash
sudo systemctl restart httpd
sudo aws s3 sync s3://s3-website-hosting-burakdmrc /var/www/html
```

⚠️ Due to changing keys and IDs in AWS Academy, secrets must be updated in each session before triggering a deployment.

## URL and Account ID

- URL of Website: [lb-website-hosting-burakdmrc-1713133902.us-east-1.elb.amazonaws.com](lb-website-hosting-burakdmrc-1713133902.us-east-1.elb.amazonaws.com)
- AWS Account ID: 895084669974
