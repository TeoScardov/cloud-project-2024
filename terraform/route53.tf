resource "aws_route53_zone" "ebook_store_zone" {
  name = "elastic-book-store.com"
}

resource "aws_route53_record" "entrypoint_web_lb_record" {
  zone_id = "Z02206093VPBVHGDFKYG7"#aws_route53_zone.ebook_store_zone.zone_id
  name    = "elastic-book-store.com"
  type    = "A"
  #ttl     = "300"
  alias {
    name    = aws_lb.web_lb.dns_name
    zone_id = aws_lb.web_lb.zone_id
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "entrypoint_app_lb_record" {
  zone_id = "Z02206093VPBVHGDFKYG7"#aws_route53_zone.ebook_store_zone.zone_id
  name    = "api.elastic-book-store.com"
  type    = "A"
  #ttl     = "300"

  alias {
    name    = aws_lb.app_lb.dns_name
    zone_id = aws_lb.app_lb.zone_id
    evaluate_target_health = true
  }
}