import scrapy

class CaseItem(scrapy.Item):
    case_number = scrapy.Field()
    name = scrapy.Field()
    court = scrapy.Field()
    hearing = scrapy.Field(),
    charge = scrapy.Field()
    charge_code = scrapy.Field()
    charge_class = scrapy.Field()
    offense_date = scrapy.Field()
    charge_code_section = scrapy.Field()
    concluded_by = scrapy.Field()
    sentence_y = scrapy.Field()
    sentence_m = scrapy.Field()
    sentence_d = scrapy.Field()
    probation_type = scrapy.Field()
    probation_y = scrapy.Field()
    probation_m = scrapy.Field()
    probation_d = scrapy.Field()
    race = scrapy.Field()
    gender = scrapy.Field()
    birth_date = scrapy.Field()
    judge = scrapy.Field()
    attorney = scrapy.Field()
#
class DatesItem(scrapy.Item):
    court = scrapy.Field()
    date = scrapy.Field()