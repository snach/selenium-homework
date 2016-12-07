# -*- coding: utf-8 -*-

import os

import unittest
# import seismograph
import urlparse
import time

from selenium.webdriver import DesiredCapabilities, Remote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

from test_base import Page
from test_base import Component

from test_auth import AuthPage
from test_auth import AuthForm

class GroupPage(Page):

    PATH = "/group/53389738115166"
    CREATE_POST = "//div[@class='input_placeholder']"

    @property
    def creating_post(self):
        self.driver.find_element_by_xpath(self.CREATE_POST).click()
        return NewPost(self.driver)

    @property
    def get_last_post(self):
        return LastPost(self.driver)

    def refresh_page(self):
        self.driver.refresh()


class NewPost(Component):
    TEXT_POST = "//div[@id='posting_form_text_field']"
    SUBMIT = "//input[@value='Поделиться'][@class='button-pro']"
    VISIBLE_BLOCK = "//div[@class='posting-form']/div[@class='posting-form_overlay invisible']"

    def set_text(self, text):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.VISIBLE_BLOCK)
        )
        self.driver.find_element_by_xpath(self.TEXT_POST).send_keys(text)

    def submit(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.SUBMIT)
        )
        self.driver.find_element_by_xpath(self.SUBMIT).click()


class LastPost(Component):
    LAST_POST = "//div[@class='groups_post-w __search-enabled'][1]//div[@class='media-text_cnt']//" \
                "div[@class='media-text_cnt_tx textWrap']"
    LAST_POST_A = "//div[@class='groups_post-w __search-enabled'][1]//div[@class='media-text_cnt']/" \
                  "div[@class='media-text_cnt_tx textWrap']/a[@class='media-text_a']"
    FALLING_MENU = "//div[@class='mlr_top_ac']/div[@class='ic12 ic12_arrow-down lp']"
    DELETE_POST = "//span[@class='tico']/i[@class='tico_img ic ic_delete']"

    ICO_X = "//div[@class='media-layer_close']/div[@class='ic media-layer_close_ico']"
    TEXT_POST_DELETED = "//span[@class='delete-stub_info']"

    def is_last_post_new_post(self, text):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.LAST_POST)
        )
        if self.driver.find_element_by_xpath(self.LAST_POST).text == text:
            return True
        else:
            return False

    def delete(self):

        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.LAST_POST_A)
        )
        self.driver.find_element_by_xpath(self.LAST_POST).click()

        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.FALLING_MENU)
        )
        self.driver.find_element_by_xpath(self.FALLING_MENU).click()

        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.DELETE_POST)
        )
        self.driver.find_element_by_xpath(self.DELETE_POST).click()

        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.TEXT_POST_DELETED)
        )
        self.driver.find_element_by_xpath(self.ICO_X).click()


class CreationPostTest(#seismograph.Case):

    unittest.TestCase):
    USERLOGIN = 'technopark30'
    USERNAME = u'Евдакия Фёдорова'
    PASSWORD = os.environ.get('PASSWORD', 'testQA1')
    # new_post = NewPost
    group_page = GroupPage

    def setUp(self):
        browser = os.environ.get('BROWSER', 'FIREFOX')
        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_form = auth_page.form
        auth_form.open_form()
        auth_form.set_login(self.USERLOGIN)
        auth_form.set_password(self.PASSWORD)
        auth_form.submit()

        user_name = auth_page.user_block.get_username()
        self.assertEqual(user_name, self.USERNAME)

        self.group_page = GroupPage(self.driver)
        self.group_page.open()
        self.new_post = self.group_page.creating_post

    def tearDown(self):
        self.driver.quit()

    def test_simple_post(self):
        text = "simple post with simple text"

        new_post = self.group_page.creating_post
        new_post.set_text(text)
        new_post.submit()
        last_post = self.group_page.get_last_post
        self.assertTrue(last_post.is_last_post_new_post(text))
        self.group_page.refresh_page()
        last_post.delete()
        self.group_page.refresh_page()
        self.assertFalse(last_post.is_last_post_new_post(text))
