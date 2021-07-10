resource "aws_db_subnet_group" "main" {
  name       = "db-qumitoru-${var.env}-subnet"
  subnet_ids = [aws_subnet.public_subnet_1.id, aws_subnet.public_subnet_2.id]
}
