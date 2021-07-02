resource "aws_route_table" "public_route_table" {
  vpc_id = "${aws_vpc.vpc.id}"
}

resource "aws_route_table" "private_route_table" {
  vpc_id = "${aws_vpc.vpc.id}"
}
