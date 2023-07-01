import pytest
from pixelsprocessor.data.pixeldb import PixelDb
from pixelsprocessor.context import PixelProcessingContext, PixelProcessingContextManager, PixelContextException

@pytest.fixture
def pixeldb():
    return PixelDb([], [])

@pytest.fixture
def root_config():
    return {"steps": ["step1", "step2", "step3"]}

def test_contextmanager(pixeldb, root_config):
    root_context = PixelProcessingContext(pixeldb, root_config)
    contextmanager = PixelProcessingContextManager(root_context)
    assert isinstance(contextmanager._context, PixelProcessingContext)

    # Test context for step1
    with contextmanager("step1") as context:
        assert isinstance(context, PixelProcessingContext)
        assert context.pixeldb == pixeldb
        assert context.config == root_config

        # Test writing to config
        context.config["foo"] = "bar"

        # Test that step1 is not completed
        with pytest.raises(PixelContextException):
            contextmanager._checkout("step12")

    # Test context for step2
    with contextmanager.requires("step1")("step2") as context:
        assert isinstance(context, PixelProcessingContext)
        assert context.pixeldb == pixeldb

        # Test that step1 could not change step2's config
        with pytest.raises(KeyError):
            assert context.config["foo"] != "bar", "step1 could write to global config"

        assert context.config == root_config

    # Test context for step3
    with contextmanager.requires("step1", "step2")("step3") as context:
        assert isinstance(context, PixelProcessingContext)
        assert context.pixeldb == pixeldb
        assert context.config == root_config

    # Test exception for missing step
    with pytest.raises(PixelContextException):
        with contextmanager.requires("step10")("step3") as context:
            pass

    # Test exception for missing step
    with pytest.raises(PixelContextException):
        with contextmanager.requires("step1", "step10")("step3") as context:
            pass

def test_contextmanager_step_data(pixeldb, root_config):
    root_context = PixelProcessingContext(pixeldb, root_config)
    contextmanager = PixelProcessingContextManager(root_context)

    # Test context for step1
    with contextmanager("step1") as context:
        assert isinstance(context, PixelProcessingContext)
        assert context.pixeldb == pixeldb
        assert context.config == root_config

        # Add data to step1
        context["foo"] = "bar"

    # Test context for step2
    with contextmanager.requires("step1")("step2") as context:
        assert isinstance(context, PixelProcessingContext)
        assert context.pixeldb == pixeldb
        assert context.config == root_config

        # Test that data from step1 is still in context
        assert context["foo"] == "bar"

        # Add data to step2
        context["baz"] = "qux"

    assert root_context["foo"] == "bar"
    assert root_context["baz"] == "qux"

    with contextmanager("step12") as context:
        assert isinstance(context, PixelProcessingContext)
        assert context.pixeldb == pixeldb
        assert context.config == root_config

    # Test that data from step2 is not in context
    assert root_context["baz"] == "qux"
    
    # Test we cannot checkout for step1 again
    with pytest.raises(PixelContextException):
        with contextmanager("step1") as context:
            pass
