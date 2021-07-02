resource "aws_vpc_endpoint" "private-from-lambda-to-s3" {
    vpc_id = "${aws_vpc.vpc.id}"
    service_name = "com.amazonaws.ap-northeast-1.s3"
    route_table_ids = ["${aws_route_table.private_route_table.id}"]

    policy = <<POLICY
{
    "Statement": [
        {
            "Action": "*",
            "Effect": "Allow",
            "Resource": "*",
            "Principal": "*"
        }
    ]
}
POLICY
}

resource "aws_vpc_endpoint" "api_gateway" {
    vpc_id = "${aws_vpc.vpc.id}"
    service_name = "com.amazonaws.ap-northeast-1.execute-api"
    vpc_endpoint_type = "Interface"
    security_group_ids = [
      aws_security_group.lambda.id,
    ]
    subnet_ids = [aws_subnet.private_subnet_1.id, aws_subnet.private_subnet_2.id]
    private_dns_enabled = true
    policy = <<POLICY
{
    "Statement": [
        {
            "Action": "*",
            "Effect": "Allow",
            "Resource": "*",
            "Principal": "*"
        }
    ]
}
POLICY
}
