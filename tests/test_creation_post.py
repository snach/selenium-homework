# -*- coding: utf-8 -*-

from selenium.webdriver.support.ui import WebDriverWait
from test_base import Page
from test_base import Component
from seismograph.ext import selenium
from base_case import BaseCase


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

    MUSIC = "//a[@id='openmusic']"
    MUSIC_BLOCK = "//div[@id='swtch'][@class='posting-form_controls  posting-form_controls__off']"
    MUSIC_SEARCH = "//div[@class='it_w search-input']/label/input[@class='search-input_it it'][@type='text']"
    TRACK = "//span[@class='posting-form_track_info ellip'][1]"
    BUTTON_ADD_TRACK = "//div[@class='form-actions __center']/a[@class='button-pro form-actions_yes']"

    ICO_SETTINGS = "//span[@class='tico toggler lp']/i[@class='tico_img ic ic_settings']"
    MENU_SETTINGS = "//div[@class='jcol-l']/div[@class='iblock-cloud_dropdown h-mod __active']"
    NO_COMMENT = "//div[@class='nowrap']/input[@name='st.toggleComments']"

    def set_text(self, text):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.VISIBLE_BLOCK)
        )
        self.driver.find_element_by_xpath(self.TEXT_POST).send_keys(text)

    def set_music(self, search_text):
        self.driver.find_element_by_xpath(self.MUSIC).click()
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.MUSIC_BLOCK)
        )
        self.driver.find_element_by_xpath(self.MUSIC_SEARCH).send_keys(search_text)
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.TRACK)
        ).click()

        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.BUTTON_ADD_TRACK)
        ).click()

    def set_no_comment(self):
        self.driver.find_element_by_xpath(self.ICO_SETTINGS).click()
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.MENU_SETTINGS)
        )
        self.driver.find_element_by_xpath(self.NO_COMMENT).click()

    def submit(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.SUBMIT)
        ).click()


class LastPost(Component):
    LAST_POST = "//div[@class='groups_post-w __search-enabled'][1]//div[@class='media-text_cnt']//" \
                "div[@class='media-text_cnt_tx textWrap']"
    LAST_POST_A = "//div[@class='groups_post-w __search-enabled'][1]//div[@class='media-text_cnt']/" \
                  "div[@class='media-text_cnt_tx textWrap']/a[@class='media-text_a']"
    FALLING_MENU = "//div[@class='mlr_top_ac']/div[@class='ic12 ic12_arrow-down lp']"
    DELETE_POST = "//span[@class='tico']/i[@class='tico_img ic ic_delete']"

    ICO_X = "//div[@class='media-layer_close']/div[@class='ic media-layer_close_ico']"
    TEXT_POST_DELETED = "//span[@class='delete-stub_info']"

    TRACK_IN_LAST_POST = "//div[@class='groups_post-w __search-enabled'][1]//a[@class='track_song']"

    COMMENT_IN_LAST_POST = "//div[@class='groups_post-w __search-enabled'][1]//a[@class='h-mod widget_cnt']"
                          # "/span[@class='widget_ico ic12 ic12_comment']"
    COMMENT_CLOSED = "//div[@class='disc_simple_input_cont'][@style='display: block;']//" \
                     "input[@class='disc_simple_input disc_simple_input__im']"

    def get_last_post_text(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.LAST_POST)
        ).text

    def get_track(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.LAST_POST)
        )
        return self.driver.find_element_by_xpath(self.TRACK_IN_LAST_POST).text

    def is_last_post_without_comments(self):
        text_lock = u"Комментарии к этой теме закрыты администрацией"

        comment = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.COMMENT_IN_LAST_POST)
        )
        comment.click()
        comment.click()
        comment.click()
        # self.driver.find_element_by_xpath(self.COMMENT_IN_LAST_POST).click()
        comment_block = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.COMMENT_CLOSED)
        )
        return comment_block.get_attribute('value') == text_lock

    def delete(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.LAST_POST)
        ).click()

        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.FALLING_MENU)
        ).click()

        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.DELETE_POST)
        ).click()

        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.TEXT_POST_DELETED)
        )
        self.driver.find_element_by_xpath(self.ICO_X).click()


suite = selenium.Suite(__name__, require=['selenium'])


@suite.register
class CreationPostTest(BaseCase):
    group_page = GroupPage
    text = str

    def teardown(self):
        last_post = self.group_page.get_last_post
        last_post.delete()
        self.group_page.refresh_page()
        last_post_text = last_post.get_last_post_text()
        self.assertion.not_equal(self.text, last_post_text)

        self.driver.quit()

    def test_simple_post(self):
        self.text = u"simple post with simple text"
        self.group_page = GroupPage(self.driver)
        self.group_page.open()
        self.new_post = self.group_page.creating_post

        new_post = self.group_page.creating_post
        new_post.set_text(self.text)
        new_post.submit()

        last_post = self.group_page.get_last_post
        last_post_text = last_post.get_last_post_text()
        self.assertion.equal(self.text, last_post_text)
        self.group_page.refresh_page()

    def test_post_with_music(self):
        self.text = u"This is post with music"
        search_text = u"Лабутены"

        self.group_page = GroupPage(self.driver)
        self.group_page.open()
        self.new_post = self.group_page.creating_post

        new_post = self.group_page.creating_post
        new_post.set_text(self.text)
        new_post.set_music(search_text)
        new_post.submit()

        last_post = self.group_page.get_last_post
        self.text = self.text + u'\n#музыка'
        last_post_text = last_post.get_last_post_text()
        self.assertion.equal(self.text, last_post_text)

        track = last_post.get_track()
        self.assertion.equal(search_text, track)
        self.group_page.refresh_page()

    def test_post_without_comments(self):
        self.text = u"This is post without comments"

        self.group_page = GroupPage(self.driver)
        self.group_page.open()
        self.new_post = self.group_page.creating_post

        new_post = self.group_page.creating_post
        new_post.set_text(self.text)
        new_post.set_no_comment()
        new_post.submit()


        last_post = self.group_page.get_last_post
        last_post_text = last_post.get_last_post_text()
        self.assertion.equal(self.text, last_post_text)
        self.assertion.true(last_post.is_last_post_without_comments())
        self.group_page.refresh_page()

