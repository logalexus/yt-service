import json
import time
import os
import logging
import undetected_chromedriver as webdriver
import uploader.logger

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import DefaultDict, Optional, Tuple
from uploader.constant import Constant
from collections import defaultdict
from datetime import datetime
from pathlib import Path


class YouTubeUploader:
    def __init__(
        self,
        video_path: str,
        metadata_json_path: Optional[str] = None,
        thumbnail_path: Optional[str] = None
    ) -> None:
        self.video_path = video_path
        self.thumbnail_path = thumbnail_path
        self.metadata_dict = self.__load_metadata(metadata_json_path)
        self.logger = logging.getLogger("YT")
        self.__init_browser()
        self.__inject_user_cookies()
        self.__inject_youtube_consent_cookie()
        self.__validate_inputs()

    def __init_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument('--disable-dev-shm-usage')
        options.page_load_strategy = "eager"

        self.browser = webdriver.Chrome(options=options, headless=True, version_main=114)
        self.browser.implicitly_wait(5)
        self.wait = WebDriverWait(self.browser, 360)

    def upload(self):
        try:
            return self.__upload()
        except Exception as e:
            print(e)
            raise

    def __load_metadata(self, metadata_json_path: Optional[str] = None) -> DefaultDict[str, str]:
        if metadata_json_path is None:
            return defaultdict(str)
        with open(metadata_json_path, encoding='utf-8') as metadata_json_file:
            return defaultdict(str, json.load(metadata_json_file))

    def __inject_user_cookies(self) -> None:
        with open("data/cookie.json", "r") as cookies_json:
            cookies = json.load(cookies_json)

        self.browser.get(Constant.YOUTUBE_URL)
        for cookie in cookies:
            self.browser.add_cookie(
                {
                    "name": cookie["name"],
                    "value": cookie["value"],
                    "domain": cookie["domain"]
                }
            )

    def __inject_youtube_consent_cookie(self) -> None:
        self.browser.add_cookie(
            {
                "name": "CONSENT",
                "value": "YES+yt.453767233.en+FX+299",
                        "domain": ".youtube.com",
            }
        )

    def __validate_inputs(self):
        if not self.metadata_dict[Constant.VIDEO_TITLE]:
            self.logger.warning(
                "The video title was not found in a metadata file")
            self.metadata_dict[Constant.VIDEO_TITLE] = Path(
                self.video_path).stem
            self.logger.warning("The video title was set to {}".format(
                Path(self.video_path).stem))
        if not self.metadata_dict[Constant.VIDEO_DESCRIPTION]:
            self.logger.warning(
                "The video description was not found in a metadata file")

    def __clear_field(self, field):
        field.click()
        time.sleep(Constant.USER_WAITING_TIME)
        field.send_keys(Keys.CONTROL + 'a')
        time.sleep(Constant.USER_WAITING_TIME)
        field.send_keys(Keys.BACKSPACE)

    def __write_in_field(self, field, string, select_all=False):
        if select_all:
            self.__clear_field(field)
        else:
            field.click()
            time.sleep(Constant.USER_WAITING_TIME)

        field.send_keys(string)

    def __upload(self) -> Tuple[bool, Optional[str]]:
        edit_mode = self.metadata_dict[Constant.VIDEO_EDIT]
        if edit_mode:
            self.browser.get(edit_mode)
            time.sleep(Constant.USER_WAITING_TIME)
        else:
            self.browser.get(Constant.YOUTUBE_URL)
            time.sleep(Constant.USER_WAITING_TIME)
            self.browser.get(Constant.YOUTUBE_UPLOAD_URL)
            time.sleep(Constant.USER_WAITING_TIME)
            absolute_video_path = str(Path.cwd() / self.video_path)

            self.logger.debug('Finding file input')
            
            # self.wait.until(EC.element_to_be_clickable((By.XPATH, Constant.INPUT_FILE_VIDEO))).send_keys(
            #      absolute_video_path)

            self.browser.find_element(By.XPATH, Constant.INPUT_FILE_VIDEO).send_keys(
                absolute_video_path)

            self.logger.debug('Attached video {}'.format(self.video_path))

            try:
                # find_element status container
                uploading_status_container = None
                while uploading_status_container is None:
                    time.sleep(Constant.USER_WAITING_TIME)
                    uploading_status_container = self.browser.find_element(
                        By.XPATH, Constant.UPLOADING_STATUS_CONTAINER)
            except Exception:
                self.logger.debug('Not found status container. Perhaps video uploaded immediately')

        if self.thumbnail_path is not None:
            absolute_thumbnail_path = str(Path.cwd() / self.thumbnail_path)
            self.browser.find_element(By.XPATH, Constant.INPUT_FILE_THUMBNAIL).send_keys(
                absolute_thumbnail_path)
            change_display = "document.getElementById('file-loader').style = 'display: block! important'"
            self.browser.driver.execute_script(change_display)
            self.logger.debug('Attached thumbnail {}'.format(self.thumbnail_path))

        title_field, description_field = self.browser.find_elements(
            By.ID, Constant.TEXTBOX_ID)
        title_field.click()
        self.__write_in_field(
            title_field, self.metadata_dict[Constant.VIDEO_TITLE], select_all=True)
        self.logger.debug('The video title was set to \"{}\"'.format(
            self.metadata_dict[Constant.VIDEO_TITLE]))

        video_description = self.metadata_dict[Constant.VIDEO_DESCRIPTION]
        video_description = video_description.replace("\n", Keys.ENTER)
        if video_description:
            self.__write_in_field(description_field, video_description, select_all=True)
            self.logger.debug('Description filled.')

        kids_section = self.browser.find_element(
            By.NAME, Constant.NOT_MADE_FOR_KIDS_LABEL)
        kids_section.location_once_scrolled_into_view
        time.sleep(Constant.USER_WAITING_TIME)

        kids_section.find_element(By.ID, Constant.RADIO_LABEL).click()
        self.logger.debug('Selected \"{}\"'.format(Constant.NOT_MADE_FOR_KIDS_LABEL))

        # Playlist
        playlist = self.metadata_dict[Constant.VIDEO_PLAYLIST]
        if playlist:
            self.browser.find_element(By.CLASS_NAME, Constant.PL_DROPDOWN_CLASS).click()
            time.sleep(Constant.USER_WAITING_TIME)
            search_field = self.browser.find_element(By.ID, Constant.PL_SEARCH_INPUT_ID)
            self.__write_in_field(search_field, playlist)
            time.sleep(Constant.USER_WAITING_TIME * 2)
            playlist_items_container = self.browser.find_element(
                By.ID, Constant.PL_ITEMS_CONTAINER_ID)
            # Try to find_element playlist
            self.logger.debug('Playlist xpath: "{}".'.format(
                Constant.PL_ITEM_CONTAINER.format(playlist)))
            playlist_item = self.browser.find_element(
                By.XPATH, Constant.PL_ITEM_CONTAINER.format(playlist), playlist_items_container)
            if playlist_item:
                self.logger.debug('Playlist found.')
                playlist_item.click()
                time.sleep(Constant.USER_WAITING_TIME)
            else:
                self.logger.debug('Playlist not found. Creating')
                self.__clear_field(search_field)
                time.sleep(Constant.USER_WAITING_TIME)

                new_playlist_button = self.browser.find_element(
                    By.CLASS_NAME, Constant.PL_NEW_BUTTON_CLASS)
                new_playlist_button.click()

                create_playlist_container = self.browser.find_element(
                    By.ID, Constant.PL_CREATE_PLAYLIST_CONTAINER_ID)
                playlist_title_textbox = self.browser.find_element(
                    By.XPATH, "//textarea", create_playlist_container)
                self.__write_in_field(playlist_title_textbox, playlist)

                time.sleep(Constant.USER_WAITING_TIME)
                create_playlist_button = self.browser.find_element(
                    By.CLASS_NAME, Constant.PL_CREATE_BUTTON_CLASS)
                create_playlist_button.click()
                time.sleep(Constant.USER_WAITING_TIME)

            done_button = self.browser.find_element(
                By.CLASS_NAME, Constant.PL_DONE_BUTTON_CLASS)
            done_button.click()

        # Advanced options
        self.browser.find_element(By.ID, Constant.ADVANCED_BUTTON_ID).click()
        self.logger.debug('Clicked MORE OPTIONS')
        time.sleep(Constant.USER_WAITING_TIME)

        # Tags
        tags = self.metadata_dict[Constant.VIDEO_TAGS]
        if tags:
            tags_container = self.browser.find_element(By.ID, Constant.TAGS_CONTAINER_ID)
            tags_field = self.browser.find_element(
                By.ID, Constant.TAGS_INPUT, tags_container)
            self.__write_in_field(tags_field, ','.join(tags))
            self.logger.debug('The tags were set to \"{}\"'.format(tags))

        self.browser.find_element(By.ID, Constant.NEXT_BUTTON).click()
        self.logger.debug('Clicked {} one'.format(Constant.NEXT_BUTTON))

        self.browser.find_element(By.ID, Constant.NEXT_BUTTON).click()
        self.logger.debug('Clicked {} two'.format(Constant.NEXT_BUTTON))

        self.browser.find_element(By.ID, Constant.NEXT_BUTTON).click()
        self.logger.debug('Clicked {} three'.format(Constant.NEXT_BUTTON))

        schedule = self.metadata_dict[Constant.VIDEO_SCHEDULE]
        if schedule:
            upload_time_object = datetime.strptime(schedule, "%m/%d/%Y, %H:%M")
            self.browser.find_element(By.ID, Constant.SCHEDULE_CONTAINER_ID).click()
            self.browser.find_element(By.ID, Constant.SCHEDULE_DATE_ID).click()
            self.browser.find_element(By.XPATH, Constant.SCHEDULE_DATE_TEXTBOX).clear()
            self.browser.find_element(By.XPATH, Constant.SCHEDULE_DATE_TEXTBOX).send_keys(
                datetime.strftime(upload_time_object, "%b %e, %Y"))
            self.browser.find_element(
                By.XPATH, Constant.SCHEDULE_DATE_TEXTBOX).send_keys(Keys.ENTER)
            self.browser.find_element(By.XPATH, Constant.SCHEDULE_TIME).click()
            self.browser.find_element(By.XPATH, Constant.SCHEDULE_TIME).clear()
            self.browser.find_element(By.XPATH, Constant.SCHEDULE_TIME).send_keys(
                datetime.strftime(upload_time_object, "%H:%M"))
            self.browser.find_element(
                By.XPATH, Constant.SCHEDULE_TIME).send_keys(Keys.ENTER)
            self.logger.debug(f"Scheduled the video for {schedule}")
        else:
            public_main_button = self.browser.find_element(
                By.NAME, Constant.PUBLIC_BUTTON)
            public_main_button.find_element(By.ID, Constant.RADIO_LABEL).click()
            self.logger.debug('Made the video {}'.format(Constant.PUBLIC_BUTTON))

        video_id = self.__get_video_id()

        # Check status container and upload progress
        try:
            uploading_status_container = self.browser.find_element(
                By.XPATH, Constant.UPLOADING_STATUS_CONTAINER)
            while uploading_status_container is not None:
                uploading_progress = uploading_status_container.get_attribute('value')
                self.logger.debug('Upload video progress: {}%'.format(uploading_progress))
                time.sleep(Constant.USER_WAITING_TIME * 5)
                uploading_status_container = self.browser.find_element(
                    By.XPATH, Constant.UPLOADING_STATUS_CONTAINER)
        except Exception:
            pass

        self.logger.debug('Upload container gone.')

        done_button = self.browser.find_element(By.ID, Constant.DONE_BUTTON)

        # Catch such error as
        # "File is a duplicate of a video you have already uploaded"
        if done_button.get_attribute('aria-disabled') == 'true':
            error_message = self.browser.find_element(
                By.XPATH, Constant.ERROR_CONTAINER).text
            self.logger.error(error_message)
            return False, None

        done_button.click()
        self.logger.debug(
            "Published the video with video_id = {}".format(video_id))
        time.sleep(Constant.USER_WAITING_TIME)
        self.browser.get(Constant.YOUTUBE_URL)
        self.__quit()
        return True, video_id

    def __get_video_id(self) -> Optional[str]:
        video_id = None
        try:
            video_url_container = self.browser.find_element(
                By.XPATH, Constant.VIDEO_URL_CONTAINER)
            video_url_element = video_url_container.find_element(
                By.XPATH, Constant.VIDEO_URL_ELEMENT)
            video_id = video_url_element.get_attribute(
                Constant.HREF).split('/')[-1]
        except Exception:
            self.logger.warning(Constant.VIDEO_NOT_FOUND_ERROR)
            pass
        return video_id

    def __quit(self):
        self.browser.quit()


if __name__ == "__main__":
    uploader = YouTubeUploader("shared/videos/xxx.mp4")
    uploader.upload()
