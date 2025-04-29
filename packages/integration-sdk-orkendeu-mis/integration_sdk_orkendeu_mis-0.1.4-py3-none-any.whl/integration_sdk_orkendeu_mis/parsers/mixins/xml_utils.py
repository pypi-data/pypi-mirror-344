from typing import Optional, Dict, Any, List, Union
from lxml import etree


class XMLUtilsMixin:
    """
    Миксин для работы с XML.
    """

    def parse_xml(self, data: bytes) -> etree.Element:
        """
        Парсит XML-данные и возвращает корневой элемент.

        :param data: Данные в формате XML.
        :return: Корневой элемент XML.
        """

        return etree.fromstring(data, parser=etree.XMLParser(recover=True))

    def element_to_dict(self, element: etree.Element) -> Dict[str, Any]:
        """
        Рекурсивно конвертирует XML-элемент в dict.

        :param element: Элемент XML.
        :return: Dict, представляющий элемент XML.
        """

        result = {}
        for child in element:
            tag = etree.QName(child).localname
            if len(child):
                result[tag] = self.element_to_dict(child)
            else:
                result[tag] = child.text

        return result


    def extract_items(self, root: etree.Element, path: str) -> List[Dict[str, Any]]:
        """
        Извлекает список элементов по XPath и конвертирует их в dict.

        :param root: Корневой элемент XML.
        :param path: XPath для поиска элементов.
        :return: Извлеченный текст или None, если тег не найден.
        """

        items = root.findall(path, namespaces=root.nsmap)
        return [self.element_to_dict(item) for item in items]
