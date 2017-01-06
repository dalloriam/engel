import sys
import pytest

sys.path.append('../engel')

from engel.widgets.media import Image, Video, ImageLink, Audio


class TestImageStructure():

    @pytest.fixture(scope="class")
    def img(self):
        return Image(id='id', img_url="//img")

    def test_widget_media_image_html_tag(self, img):
        assert img.html_tag == 'img', 'Image should set Image.html_tag = "img".'

    def test_widget_media_image_has_source(self, img):
        assert hasattr(img, 'source') and isinstance(img.__class__.source, property), 'Image should have a property Image.source.'

    def test_widget_media_sets_image_source(self, img):
        assert img.source == '//img', 'Image.build() should set Image.source.'


class TestVideoStructure():

    @pytest.fixture(scope="class")
    def vid(self):
        return Video(id='id', vid_url="//vid")

    def test_widget_media_video_html_tag(self, vid):
        assert vid.html_tag == 'video', 'Video should set Video.html_tag = "video".'

    def test_widget_media_video_has_source(self, vid):
        assert hasattr(vid, 'source') and isinstance(vid.__class__.source, property), 'Video should have a property Video.source.'

    def test_widget_media_video_sets_source(self, vid):
        assert vid.source == '//vid', 'Video.build() should set Video.source.'


class TestImageLinkStructure():

    @pytest.fixture(scope="class")
    def lnk(self):
        return ImageLink(id="id", link="//link", img_url="//img")

    def test_widget_media_imagelink_html_tag(self, lnk):
        assert lnk.html_tag == "a", 'ImageLink should set ImageLink.html_tag = "a"'

    def test_widget_media_imagelink_has_target(self, lnk):
        assert hasattr(lnk, 'target') and isinstance(lnk.__class__.target, property)

    def test_widget_media_imagelink_sets_target(self, lnk):
        assert lnk.target == '//link'

    def test_widget_media_imagelink_has_image(self, lnk):
        assert len(lnk.children) == 1, 'ImageLink.build() should add a child to ImageLink.children().'

    def test_widget_media_imagelink_image_is_valid(self, lnk):
        assert isinstance(lnk.children[0], Image), 'ImageLink.children[0] should be an Image.'
        assert lnk.children[0].source == '//img', 'ImageLink.build() should pass img_url to child Image.'


class TestAudioStructure():

    @pytest.fixture(scope="class")
    def aud(self):
        return Audio(id='id', audio_path="//audio")

    def test_widget_media_audio_html_tag(self, aud):
        assert aud.html_tag == 'audio', 'Audio should set Audio.html_tag = "audio".'

    def test_widget_media_audio_has_source(self, aud):
        assert hasattr(aud, 'source') and isinstance(aud.__class__.source, property), 'Audio should have property Audio.source.'

    def test_widget_media_audio_sets_source(self, aud):
        assert aud.source == '//audio'
