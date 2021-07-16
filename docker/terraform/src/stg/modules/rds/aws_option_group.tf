# option group
resource "aws_db_option_group" "main" {
  name                     = "qumitoru-tf-${var.env}-mysql57"
  option_group_description = "qumitoru option group"
  engine_name              = "mysql"
  major_engine_version     = "5.7"
}
