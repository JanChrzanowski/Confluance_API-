from ssl import VerifyMode

import pandas as pd
import numpy as np

from atlassian import Confluence
from urllib.request import urlopen
from bs4 import BeautifulSoup
from html.parser import HTMLParser


confluence = Confluence(
    url=url,
    token=api_token,
)


class Confluance_Edit_Page(Confluence):

    def __init__(self, space, page_name):

        self.space = space
        self.page_name = page_name
        self.page_id  = confluence.get_page_by_title(space=space, title=page_name)["id"]
        self.page_content = confluence.get_page_by_id(self.page_id, expand="body.storage")["body"]["storage"]["value"]

        if confluence.page_exists(self.space, self.page_name):
            print("{} exists ready to edit".format(str(self.page_name)))
    
    def get_table(self,table_number):

        table = pd.read_html(self.page_content)
        number_of_tables = len(table)
        
        if 0 < table_number <= number_of_tables:
            df = table[table_number - 1]
            return df
        else:
            raise Exception("Sorry, there is only {} tables on this page".format(number_of_tables))

    def replace_table(self,table_to_replace_number,table):

        soup = BeautifulSoup(self.page_content, "lxml")
        number_of_tables = len(soup(["table"]))

        if 0 < table_to_replace_number <= number_of_tables:
            script = soup(["table"])[table_to_replace_number - 1]
            script.replaceWith(BeautifulSoup(table.to_html(), 'html.parser'))
        else: 
            raise Exception("Sorry, there is only {} tables on this page".format(number_of_tables))

        confluence.update_page(self.page_id, self.page_name, str(soup) ,minor_edit = False)
        self.page_content = confluence.get_page_by_id(self.page_id, expand="body.storage")["body"]["storage"]["value"]
    

    def copy_page(self,page_to_copy):

        page_id  = confluence.get_page_by_title(space=self.space, title=page_to_copy)["id"]
        page = confluence.get_page_by_id(page_id, expand="body.storage")
        page_content = page["body"]["storage"]["value"]
        confluence.update_page(self.page_id, self.page_name, page_content ,minor_edit = False)
        self.page_content = confluence.get_page_by_id(self.page_id, expand="body.storage")["body"]["storage"]["value"]


    # TO DO:

    def copy_page_with_children():
 
    #def replace_image():
        pass

    def get_image():
        pass

    def get_paragraph():
        pass

    def replace_paragraph():
        pass

    # TO DO: Create automate to find tables to replace


