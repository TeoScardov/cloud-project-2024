resource "aws_route53_zone" "ebook_store_zone" {
  name = "elastic-book-store.com"
}

resource "aws_route53_record" "entrypoint_web_lb_record" {
  zone_id = aws_route53_zone.ebook_store_zone.zone_id
  name    = "elastic-book-store.com"
  type    = "A"
  records = [aws_lb.web_lb.dns_name]
}

resource "aws_route53_record" "entrypoint_app_lb_record" {
  zone_id = aws_route53_zone.ebook_store_zone.zone_id
  name    = "api.elastic-book-store.com"
  type    = "A"
  records = [aws_lb.app_lb.dns_name]
}