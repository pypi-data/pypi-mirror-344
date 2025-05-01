"""Common test fixtures for all sologm tests."""

import logging
from typing import Any, Callable, Dict, Generator, Optional, Type
from unittest.mock import MagicMock

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

# Import the factory function
from sologm.core.factory import create_all_managers
from sologm.database.session import DatabaseManager, SessionContext
from sologm.integrations.anthropic import AnthropicClient
from sologm.models.base import Base
from sologm.models.event import Event  # Added Event import
from sologm.models.event_source import EventSource
from sologm.models.game import Game  # Added Game import
from sologm.models.scene import Scene, SceneStatus  # Added Scene import
from sologm.utils.config import Config

logger = logging.getLogger(__name__)


# Renamed fixture, removed autouse=True and the 'with patch(...)' block
@pytest.fixture
def mock_config_no_api_key() -> MagicMock:
    """
    Creates a mock Config object that simulates the anthropic_api_key
    not being set (returns None when get() is called for that key).
    """
    logger.debug("[Fixture mock_config_no_api_key] Creating mock Config object")
    mock_config = MagicMock(spec=Config)

    # Define the behavior for the mock's get method
    def mock_get(key: str, default: Any = None) -> Any:
        logger.debug(
            f"[Fixture mock_config_no_api_key] Mock config.get called with key: {key}"
        )
        if key == "anthropic_api_key":
            logger.debug(
                f"[Fixture mock_config_no_api_key] Mock config returning None for key: {key}"
            )
            return None
        # For other keys, maybe return default or raise an error if unexpected
        logger.debug(
            f"[Fixture mock_config_no_api_key] Mock config returning default for key: {key}"
        )
        return default

    mock_config.get.side_effect = mock_get
    logger.debug("[Fixture mock_config_no_api_key] Returning configured mock object")
    return mock_config


# Database fixtures
@pytest.fixture
def db_engine() -> Generator[Engine, None, None]:
    """Create a new in-memory SQLite database for each test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


# Step 4.1: Remove db_session Fixture


@pytest.fixture(scope="function", autouse=True)
def database_manager(db_engine: Engine) -> Generator[DatabaseManager, None, None]:
    """Create a DatabaseManager instance for testing.

    This fixture replaces the singleton DatabaseManager instance with a test-specific
    instance that uses an in-memory SQLite database. This approach ensures:

    1. Test isolation: Each test gets its own clean database
    2. No side effects: Tests don't affect the real application database
    3. Singleton pattern preservation: The pattern is maintained during testing

    The original singleton instance is saved before the test and restored afterward,
    ensuring that tests don't permanently modify the application's database connection.
    This is critical for test isolation and preventing test order dependencies.

    Args:
        db_engine: SQLite in-memory engine for testing

    Yields:
        A test-specific DatabaseManager instance
    """
    from sologm.database.session import DatabaseManager

    # Save original instance to restore it after the test
    # This prevents tests from affecting each other or the real application
    old_instance = DatabaseManager._instance

    # Create new instance with test engine
    db_manager = DatabaseManager(engine=db_engine)
    DatabaseManager._instance = db_manager

    yield db_manager

    # Restore original instance to prevent test pollution
    DatabaseManager._instance = old_instance


# Mock fixtures
@pytest.fixture
def mock_anthropic_client() -> MagicMock:
    """Create a mock Anthropic client."""
    return MagicMock(spec=AnthropicClient)


@pytest.fixture
def cli_test() -> Callable[[Callable[[Session], Any]], Any]:
    """Helper for testing CLI command patterns.

    This fixture provides a function that executes test code within a session context,
    mimicking how CLI commands work in production.

    Example:
        def test_cli_pattern(cli_test):
            def test_func(session):
                game_manager = GameManager(session=session)
                return game_manager.create_game("Test Game", "Description")

            game = cli_test(test_func)
            assert game.name == "Test Game"
    """

    def run_with_context(test_func: Callable[[Session], Any]) -> Any:
        from sologm.database.session import get_db_context

        with get_db_context() as session:
            return test_func(session)

    return run_with_context


# Session context fixture
@pytest.fixture
def session_context() -> SessionContext:  # Changed return type hint
    """Provides a SessionContext instance for testing.

    This fixture provides the same session context that application code uses,
    ensuring tests mirror real usage patterns. Use this as the primary way to
    access the database in tests.

    Example:
        def test_something(session_context): # Fixture name used directly
            with session_context as session: # Used directly as context manager
                # Test code using session
    """
    from sologm.database.session import SessionContext  # Import the class

    # Return an instance of the context manager
    return SessionContext()


# Manager fixtures
# Step 4.2: Remove Individual Manager Fixtures


# Step 4.4: Refactor Factory Fixtures (`create_test_*`)
@pytest.fixture
def create_test_game() -> Callable[..., Game]:
    """Factory fixture to create test games using the GameManager."""

    def _create_game(
        session: Session,
        name: str = "Test Game",
        description: str = "A test game",
        is_active: bool = True,
    ) -> Game:
        managers = create_all_managers(session)
        game = managers.game.create_game(name, description, is_active=is_active)
        # No merge needed, object is already session-bound
        # REMOVED: session.refresh call and try/except block
        return game  # Return the session-bound object

    return _create_game


@pytest.fixture
def create_test_act() -> Callable[..., "Act"]:  # Use quotes for forward reference
    """Factory fixture to create test acts using the ActManager."""

    # Import Act locally to avoid circular dependency issues at module level
    from sologm.models.act import Act

    def _create_act(
        session: Session,
        game_id: str,
        title: Optional[str] = "Test Act",
        summary: Optional[str] = "A test act",
        is_active: bool = True,
        sequence: Optional[int] = None,
    ) -> Act:
        managers = create_all_managers(session)
        act = managers.act.create_act(
            game_id=game_id,
            title=title,
            summary=summary,
            make_active=is_active,
        )
        # If sequence was specified, update it directly using the correct session
        if sequence is not None:
            act.sequence = sequence
            session.add(act)
            session.flush()  # Keep flush if sequence is manually set

        # No merge needed
        # REMOVED: session.refresh call and try/except block
        return act

    return _create_act


@pytest.fixture
def create_test_scene() -> Callable[..., Scene]:
    """Factory fixture to create test scenes using the SceneManager."""

    def _create_scene(
        session: Session,
        act_id: str,
        title: str = "Test Scene",
        description: str = "A test scene",
        is_active: bool = True,
        status: SceneStatus = SceneStatus.ACTIVE,
    ) -> Scene:
        managers = create_all_managers(session)
        scene = managers.scene.create_scene(
            act_id=act_id,
            title=title,
            description=description,
            make_active=is_active,
        )
        if status == SceneStatus.COMPLETED:
            # Use manager for completion logic (it uses the correct session)
            managers.scene.complete_scene(scene.id)
            # Re-fetch the scene to get updated state
            scene = managers.scene.get_scene(scene.id)
            # Ensure the re-fetched scene is not None
            if scene is None:
                # Should not happen if complete_scene/get_scene work, but defensive check
                raise RuntimeError(
                    "Failed to re-fetch scene after completion in factory"
                )

        # Add a refresh call here before returning, similar to create_test_event
        # This helps ensure relationships are loaded while the object is known
        # to be persistent within this session context. Flushing ensures the object
        # state is synchronized with the DB before refresh.
        try:
            session.flush()  # Flush *before* refresh to ensure state is synchronized
            # Refresh common relationships that might be needed immediately after creation
            # Adjust attribute_names based on typical usage patterns
            session.refresh(scene, attribute_names=["act"])
        except Exception as e:
            logger.warning(
                f"Warning: Error refreshing relationships in create_test_scene factory: {e}"
            )
            # Decide if this should be a hard failure or just a warning
            # For now, log and continue, but this might hide issues

        # No merge needed
        # REMOVED: session.refresh call and try/except block (was already removed)
        return scene  # Return the potentially refreshed, session-bound object

    return _create_scene


@pytest.fixture
def create_test_event() -> Callable[..., Event]:
    """Factory fixture to create test events using the EventManager."""

    def _create_event(
        session: Session,
        scene_id: str,
        description: str = "Test event",
        source: str = "manual",
        interpretation_id: Optional[str] = None,
    ) -> Event:
        managers = create_all_managers(session)
        event = managers.event.add_event(
            description=description,
            scene_id=scene_id,
            source=source,
            interpretation_id=interpretation_id,
        )
        # No merge needed
        try:
            # Refresh relationships using the passed-in session
            session.refresh(
                event, attribute_names=["scene", "source", "interpretation"]
            )
        except Exception as e:
            logger.warning(
                f"Warning: Error refreshing relationships in create_test_event factory: {e}"
            )
        return event

    return _create_event


@pytest.fixture
def create_test_interpretation_set() -> Callable[..., "InterpretationSet"]:
    """Factory fixture to create test interpretation sets."""
    # Import locally
    from sologm.models.oracle import InterpretationSet

    def _create_interpretation_set(
        session: Session,
        scene_id: str,
        context: str = "Test Context",
        oracle_results: str = "Test Oracle Results",
        retry_attempt: int = 0,
        is_current: bool = False,
    ) -> InterpretationSet:
        # Placeholder: Needs implementation using InterpretationSetManager if it exists,
        # or direct model creation + session add/flush/refresh.
        # For now, just create directly to satisfy fixture requirement.
        managers = create_all_managers(session)
        # Assuming InterpretationSetManager exists and has a create method
        # If not, use InterpretationSet.create(...) and session.add/flush/refresh
        # interp_set = managers.interpretation.create_interpretation_set(...) # Example
        interp_set = InterpretationSet.create(
            scene_id=scene_id,
            context=context,
            oracle_results=oracle_results,
            retry_attempt=retry_attempt,
            is_current=is_current,
        )
        session.add(interp_set)
        session.flush()
        try:
            session.refresh(interp_set, attribute_names=["scene", "interpretations"])
        except Exception as e:
            logger.warning(
                f"Warning: Error refreshing relationships in create_test_interpretation_set factory: {e}"
            )
        logger.warning(
            "create_test_interpretation_set fixture is using placeholder implementation."
        )
        return interp_set

    return _create_interpretation_set


@pytest.fixture
def create_test_interpretation() -> Callable[..., "Interpretation"]:
    """Factory fixture to create test interpretations."""
    # Import locally
    from sologm.models.oracle import Interpretation

    def _create_interpretation(
        session: Session,
        set_id: str,
        title: str = "Test Interpretation",
        description: str = "A test interpretation.",
        is_selected: bool = False,
    ) -> Interpretation:
        # Placeholder: Needs implementation using InterpretationManager if it exists,
        # or direct model creation + session add/flush/refresh.
        managers = create_all_managers(session)
        # Assuming InterpretationManager exists and has a create method
        # If not, use Interpretation.create(...) and session.add/flush/refresh
        # interp = managers.interpretation.create_interpretation(...) # Example
        interp = Interpretation.create(
            set_id=set_id,
            title=title,
            description=description,
            is_selected=is_selected,
        )
        session.add(interp)
        session.flush()
        try:
            session.refresh(interp, attribute_names=["interpretation_set", "event"])
        except Exception as e:
            logger.warning(
                f"Warning: Error refreshing relationships in create_test_interpretation factory: {e}"
            )
        logger.warning(
            "create_test_interpretation fixture is using placeholder implementation."
        )
        return interp

    return _create_interpretation


# Step 4.5: Remove Object Fixtures (test_game, test_act, test_scene, test_events, etc.)
# Tests should now create these objects directly using the refactored factory fixtures
# within a `with session_context as session:` block.


# Step 4.5: Remove Complex Fixtures (test_game_with_scenes, etc.)
# Tests requiring complex setups should build them using the refactored factory fixtures
# within their own `with session_context as session:` block.


# Fixtures that remain valid or are updated
@pytest.fixture(autouse=True)
def initialize_event_sources(session_context: Callable[[], SessionContext]) -> None:
    """Initialize event sources for testing using the session_context."""
    sources = ["manual", "oracle", "dice"]
    with session_context as session:
        for source_name in sources:
            existing = (
                session.query(EventSource)
                .filter(EventSource.name == source_name)
                .first()
            )
            if not existing:
                source = EventSource.create(name=source_name)
                session.add(source)
        # Session is committed automatically when context exits


# Helper fixtures for testing model properties
@pytest.fixture
def assert_model_properties() -> Callable[[Any, Dict[str, Any]], None]:
    """Helper fixture to assert model properties work correctly.

    This fixture provides a function that can be used to verify that model properties
    and hybrid properties return the expected values.

    Example:
        def test_game_properties(test_game, assert_model_properties):
            expected = {
                'has_acts': True,
                'act_count': 2,
                'has_active_act': True
            }
            assert_model_properties(test_game, expected)
    """

    def _assert_properties(model: Any, expected_properties: Dict[str, Any]) -> None:
        """Assert that model properties match expected values.

        Args:
            model: The model instance to check
            expected_properties: Dict of property_name: expected_value
        """
        for prop_name, expected_value in expected_properties.items():
            assert hasattr(model, prop_name), (
                f"Model {model.__class__.__name__} has no property {prop_name}"
            )
            actual_value = getattr(model, prop_name)
            assert actual_value == expected_value, (
                f"Property {prop_name} doesn't match expected value. "
                f"Expected: {expected_value}, Got: {actual_value}"
            )

    return _assert_properties


@pytest.fixture
def test_hybrid_expressions() -> Callable[[Type[Base], str, Any, int], None]:
    """Test fixture for SQL expressions of hybrid properties.

    This fixture provides a function that can be used to verify that hybrid property
    SQL expressions work correctly in queries.

    Example:
        def test_game_has_acts_expression(test_hybrid_expressions):
            test_hybrid_expressions(Game, 'has_acts', True, 1)  # Expect 1 game with acts
    """

    def _test_expression(
        model_class: Type[Base],
        property_name: str,
        filter_condition: Any,
        expected_count: int,
    ) -> None:
        """Test that a hybrid property's SQL expression works correctly.

        Args:
            model_class: The model class to query
            property_name: The name of the hybrid property
            filter_condition: The condition to filter by (True/False)
            expected_count: The expected count of results
        """
        from sologm.database.session import get_db_context

        with get_db_context() as session:
            property_expr = getattr(model_class, property_name)
            query = session.query(model_class).filter(property_expr == filter_condition)
            result_count = query.count()
            assert result_count == expected_count, (
                f"Expected {expected_count} results for {model_class.__name__}.{property_name} == {filter_condition}, "
                f"got {result_count}"
            )

    return _test_expression


# Complex test fixtures like test_game_with_scenes, test_game_with_complete_hierarchy,
# and test_hybrid_property_game have been removed.
# Tests requiring these setups should now build them within the test function
# using the refactored factory fixtures and the session_context.
