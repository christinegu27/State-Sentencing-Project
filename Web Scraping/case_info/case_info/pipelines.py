from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
from items import CaseItem
from items import DatesItem


class CasesPipeline:

#     # def open_spider(self, spider):
#     #     self.file = open('courts.csv', 'wb')
#     #     self.exporter = CsvItemExporter(self.file)
#     #     self.exporter.start_exporting()

#     # def close_spider(self, spider):
#     #     self.exporter.finish_exporting()
#     #     self.file.close()

#     # def process_item(self, item, spider):
        
#     #     # if isinstance(item, CaseItem):
#     #     self.exporter.export_item(item)
#     #     return item

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
            return self.court_to_exporter[court][0]

        elif isinstance(item,DatesItem):
            if "dates" not in self.court_to_exporter:
                csv_file = open('dates_finished.csv', 'wb')
                exporter = CsvItemExporter(csv_file)
                exporter.start_exporting()
                self.court_to_exporter["dates"] = (exporter, csv_file)
            return self.court_to_exporter["dates"][0]

    def process_item(self, item, spider):
        # if isinstance(item, CaseItem):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
            # print(item['name'])
        return item

# class DatesPipeline:

#     def open_spider(self, spider):
#         self.file = open('dates_finished.csv', 'wb')
#         self.exporter = CsvItemExporter(self.file)
#         self.exporter.start_exporting()

#     def close_spider(self, spider):
#         self.exporter.finish_exporting()
#         self.file.close()

#     def process_item(self, item, spider):
        
#         if isinstance(item, DatesItem):
#             self.exporter.export_item(item)
#             print(item['date'])
#             return item

# class DaPipeline:

#     def open_spider(self, spider):
#         self.file = open('dates_finished.csv', 'wb')
#         self.exporter = CsvItemExporter(self.file)
#         self.exporter.start_exporting()

#     def close_spider(self, spider):
#         self.exporter.finish_exporting()
#         self.file.close()

#     def process_item(self, item, spider):
        
#         if isinstance(item, DaItem):
#             self.exporter.export_item(item)
#             print(item['date'])
#             return item

