##################
## ecr endpoint ##
##################

resource "aws_vpc_endpoint" "ecr-api-endpoint" {
    vpc_id = aws_vpc.ebook_store_vpc.id
    service_name = "com.amazonaws.us-east-1.ecr.api"
    vpc_endpoint_type = "Interface"
    private_dns_enabled = true
    subnet_ids = [
#        aws_subnet.ebook_store_public_subnet_web_1.id, aws_subnet.ebook_store_public_subnet_web_2.id,
        aws_subnet.ebook_store_private_subnet_application_1.id, aws_subnet.ebook_store_private_subnet_application_2.id]

    security_group_ids = [aws_security_group.endpoints_sg.id]

    tags = {
        Name = "ecr-api-endpoint"
    }
  
}

resource "aws_vpc_endpoint" "ecr-dkr-endpoint" {
    vpc_id = aws_vpc.ebook_store_vpc.id
    service_name = "com.amazonaws.us-east-1.ecr.dkr"
    vpc_endpoint_type = "Interface"
    private_dns_enabled = true
    subnet_ids = [
#        aws_subnet.ebook_store_public_subnet_web_1.id, aws_subnet.ebook_store_public_subnet_web_2.id,
        aws_subnet.ebook_store_private_subnet_application_1.id, aws_subnet.ebook_store_private_subnet_application_2.id]
    
    security_group_ids = [aws_security_group.endpoints_sg.id]

    tags = {
        Name = "ecr-dkr-endpoint"
    }
  
}

resource "aws_vpc_endpoint" "secretmanager-endpoint" {
  vpc_id       = aws_vpc.ebook_store_vpc.id
  service_name = "com.amazonaws.us-east-1.secretsmanager"
  vpc_endpoint_type = "Interface"
  subnet_ids = [
#        aws_subnet.ebook_store_public_subnet_web_1.id, aws_subnet.ebook_store_public_subnet_web_2.id,
        aws_subnet.ebook_store_private_subnet_application_1.id, aws_subnet.ebook_store_private_subnet_application_2.id]

  security_group_ids = [aws_security_group.endpoints_sg.id]

  tags = {
    Name = "secretmanager-endpoint"
  }

} 
resource "aws_vpc_endpoint" "logs-endpoint" {
  vpc_id       =  aws_vpc.ebook_store_vpc.id
  service_name = "com.amazonaws.us-east-1.logs"
  vpc_endpoint_type = "Interface"
  subnet_ids = [
#        aws_subnet.ebook_store_public_subnet_web_1.id, aws_subnet.ebook_store_public_subnet_web_2.id,
        aws_subnet.ebook_store_private_subnet_application_1.id, aws_subnet.ebook_store_private_subnet_application_2.id]

  security_group_ids = [aws_security_group.endpoints_sg.id]

  tags = {
      Name = "logs-endpoint"
  }

} 
resource "aws_vpc_endpoint" "ssm-endpoint" {
  vpc_id       =  aws_vpc.ebook_store_vpc.id
  service_name = "com.amazonaws.us-east-1.ssmmessages"
  vpc_endpoint_type = "Interface"
  subnet_ids = [
#        aws_subnet.ebook_store_public_subnet_web_1.id, aws_subnet.ebook_store_public_subnet_web_2.id,
        aws_subnet.ebook_store_private_subnet_application_1.id, aws_subnet.ebook_store_private_subnet_application_2.id]

  security_group_ids = [aws_security_group.endpoints_sg.id]

  tags = {
      Name = "ssm-endpoint"
  }
}
