from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter


class CasesPipeline:
    # def from_crawler(cls, crawler):
    #     pipeline = cls()
    #     crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
    #     crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
    #     return pipeline

    # def spider_opened(self, spider):
    #     self.file = open('output.csv', 'w+b')
    #     self.exporter = CsvItemExporter(self.file)
    #     self.exporter.start_exporting()

    # def spider_closed(self, spider):
    #     self.exporter.finish_exporting()
    #     self.file.close()

    # def process_item(self, item, spider):
    #     if isinstance(item, CaseItem):
    #         self.exporter.export_item(item)
    #         return item


    def open_spider(self, spider):
        self.court_to_exporter = {}

    def close_spider(self, spider):
        for exporter, csv_file in self.court_to_exporter.values():
            exporter.finish_exporting()
            csv_file.close()

    def _exporter_for_item(self, item):
        if isinstance(item, CaseItem):
            adapter = ItemAdapter(item)
            court = adapter['court']
            if court not in self.court_to_exporter:
                csv_file = open(f'{court}.csv', 'wb')
                exporter = CsvItemExporter(csv_file)
                exporter.start_exporting()
                self.court_to_exporter[court] = (exporter, csv_file)
            return self.court_to_exporter[year][0]

    def process_item(self, item, spider):
        if isinstance(item, CaseItem):
            exporter = self._exporter_for_item(item)
            exporter.export_item(item)
            return item

class DatesPipeline:

    def open_spider(self, spider):
        self.file = open('dates_finished.csv', 'wb')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        
        if isinstance(item, DatesItem):
            self.exporter.export_item(item)
            return item

           
