import sys
import pytest

sys.path.append('../engel')

from engel.widgets.text import Title, Paragraph, Span, TextLink


class TestTitleStructure():

    @pytest.fixture(scope="class")
    def title(self):
        return Title(id='id', text='mytitle')

    def test_widget_text_title_sets_size(self, title):
        assert title.size == 1, 'Title.build() should set size = 1.'

    def test_widget_text_title_html_tag(self, title):
        assert title._get_html_tag() == "h1", 'Title._get_html_tag() should return a tag of the form: "h{0}".format(self.size).'

    def test_widget_text_title_sets_content(self, title):
        assert title.content == 'mytitle', 'Title.build() should set Title.content.'


class TestParagraphStructure():

    @pytest.fixture(scope="class")
    def par(self):
        return Paragraph(id='id', text='mytext')

    def test_widget_text_paragraph_html_tag(self, par):
        assert par.html_tag == 'p', 'Paragraph should set Paragraph.html_tag = "p".'

    def test_widget_text_paragraph_sets_content(self, par):
        assert par.content == 'mytext', 'Paragraph.build() should set Paragraph.content.'


class TestSpanStructure():

    @pytest.fixture(scope="class")
    def span(self):
        return Span(id='id', text="mytext")

    def test_widget_text_span_html_tag(self, span):
        assert span.html_tag == "span", 'Span should set Span.html_tag = "span".'

    def test_widget_text_span_sets_content(self, span):
        assert span.content == "mytext", "Span.build() should set Span.content."


class TestTextLinkStructure():

    @pytest.fixture(scope="class")
    def link(self):
        return TextLink(id='id', text="mytext", url="//path")

    def test_widget_text_textlink_html_tag(self, link):
        assert link.html_tag == "a", 'TextLink should set TextLink.html_tag = "a"'

    def test_widget_text_textlink_has_target(self, link):
        assert hasattr(link, 'target') and isinstance(link.__class__.target, property), 'TextLink should have a property TextLink.target.'

    def test_widget_text_textlink_sets_target(self, link):
        assert link.target == "//path", 'TextLink.build() should set TextLink.target.'

    def test_widget_text_textlink_sets_content(self, link):
        assert link.content == "mytext", 'TextLink.build() should set TextLink.content.'
