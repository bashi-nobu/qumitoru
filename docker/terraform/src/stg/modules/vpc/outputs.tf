output "cidr_block" {
  value = "${aws_vpc.vpc.cidr_block}"
}

output "vpc_id" {
  value = "${aws_vpc.vpc.id}"
}

output "public_subnet_1_id" {
  value = "${aws_subnet.public_subnet_1.id}"
}

output "public_subnet_2_id" {
  value = "${aws_subnet.public_subnet_2.id}"
}

output "private_subnet_1_id" {
  value = "${aws_subnet.private_subnet_1.id}"
}

output "private_subnet_2_id" {
  value = "${aws_subnet.private_subnet_2.id}"
}

output "aws_security_group_alb_id"{
  value = "${aws_security_group.alb.id}"
}

output "aws_security_group_db_id"{
  value = "${aws_security_group.db.id}"
}

output "aws_security_group_instance_id"{
  value = "${aws_security_group.instance.id}"
}

output "aws_db_subnet_group_main_name"{
  value = "${aws_db_subnet_group.main.name}"
}

output "aws_security_group_lambda_id" {
  value = "${aws_security_group.lambda.id}"
}

output "aws_security_group_rds_proxy_id" {
  value = "${aws_security_group.rds_proxy.id}"
}

output "aws_vpc_endpoint_api_gateway_id" {
  value = "${aws_vpc_endpoint.api_gateway.id}"
}

output "aws_vpc_endpoint_lambda_dns" {
  value = "${aws_vpc_endpoint.api_gateway.dns_entry[0].dns_name}"
}
