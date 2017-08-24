import requests, json
from collections import Iterable
from xml.dom import minidom, Node
import re


class Parser:
    def __init__(self, data):
        self.json = False
        if data.startswith('{'):
            self.json = True
            self.data = data
        else:
            comp = re.compile(r'>(\s*)<')
            data = comp.sub('><', data)
            self.dom = minidom.parseString(data)
            self.dom.normalize()
            self.data = None

    def start(self):
        return self.nodes(self.dom) if not self.json else json.loads(self.data)

    def array_parse(self, node_element):
        a = []
        for node in node_element.childNodes:
            a.append(self.nodes(node))
        return a

    def nodes(self, element):
        """
        :param element: 
        :type element: object xml.dom.Node
        :return: dict
        """
        d = {}
        for node in element.childNodes:
            if node.nodeType == Node.TEXT_NODE:
                try:
                    return int(node.nodeValue)
                except ValueError:
                    return node.nodeValue
            elif node.nodeType == Node.ELEMENT_NODE:
                if 'list' in node.attributes.keys():
                    d[node.nodeName] = self.array_parse(node)
                else:
                    d[node.nodeName] = self.nodes(node)
        return d if len(d) > 0 else ''


def stringify_values(dictionary):
    stringified_values_dict = {}
    for key, value in dictionary.items():
        if isinstance(value, Iterable) and not isinstance(value, (str, bytes, bytearray)):
            value = u','.join(map(str, value))
        stringified_values_dict[key] = value
    return stringified_values_dict


def json_iter_parse(data):
    for key in data.keys():
        yield {key: data[key]}


class VkRequest(requests.Session):
    def request(self, method, url, **kwargs):
        kwargs['headers'] = {'User-Agent': 'VKAndroidApp/4.12-1170'}
        response = super().request(method, url, **kwargs)
        return response
