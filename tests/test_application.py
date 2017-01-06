import sys
import pytest
sys.path.append('../engel')

from engel.application import Application

from engel.websocket import EventProcessor, EventServer


class TestApplicationStructure():

    @pytest.fixture(scope="class")
    def app_no_base(self):
        class MyApp(Application):
            pass

        return MyApp

    @pytest.fixture(scope="class")
    def app_base(self):
        class MyApp(Application):
            base_title = "{0} | Base"

        return MyApp()

    def test_application_raises_when_no_base_title(self, app_no_base):
        with pytest.raises(NotImplementedError):
            app_no_base()

    def test_application_has_eventprocessor(self, app_base):
        assert hasattr(app_base, 'processor') and isinstance(app_base.processor, EventProcessor), 'Application.processor should be an instance of websocket.EventProcessor'

    def test_application_has_eventserver(self, app_base):
        assert hasattr(app_base, 'server') and isinstance(app_base.server, EventServer), 'Application.server should be an instance of websocket.EventServer'

    def test_application_has_services(self, app_base):
        assert hasattr(app_base, 'services') and app_base.services == {}, 'Application should set Application.services = {}.'

    def test_application_has_views(self, app_base):
        assert hasattr(app_base, 'views') and app_base.views == {}, 'Application should set Application.views = {}.'

    def test_application_has_current_view(self, app_base):
        assert hasattr(app_base, 'current_view'), 'Application should have Application.current_view.'

    def test_application_sets_current_view(self, app_base):
        assert app_base.current_view is None, 'Application should set Application.current_view = "None".'

    def test_application_registers_init(self, app_base):
        assert 'init' in app_base.processor.handlers and len(app_base.processor.handlers.keys()) == 1

    def test_application_unregister_unregisters(self, app_base):
        app_base.register('load', 2, 'a')
        assert 'load' in app_base.processor.handlers and str(id(2)) in app_base.processor.handlers['load'] and app_base.processor.handlers['load'][
            str(id(2))] == [2], 'Application.register() should register with the EventProcessor.'
        app_base.unregister('load', 2, 'a')
        assert app_base.processor.handlers['load'][str(id(2))] == [], 'Application.unregister() should unregister from the EventProcessor.'
