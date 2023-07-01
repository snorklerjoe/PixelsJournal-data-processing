"""Context manager for pixelsprocessor module."""

from pixelsprocessor.data.pixeldb import PixelDb
from typing import Dict, List, Optional, Any, Mapping

class PixelContextException(Exception):
    """Exception raised when a PixelContextManager is used incorrectly.
    """
    pass

class PixelProcessingContext(Dict[str, Any]):
    """Context for a step in the processing pipeline."""

    def __init__(self, pixeldb: PixelDb, root_config: Dict[str, Any], _step_ctx: Optional[Mapping[str, Any]] = None) -> None:
        self.pixeldb = pixeldb
        self.config = root_config.copy()
        self.__step_data: Dict[str, Any] = _step_ctx if _step_ctx is not None else {}

    def clone(self, deep: bool = False) -> 'PixelProcessingContext':
        """Clones the context.
        A shallow clone offers reasonable sandboxing for the individual steps
        A deep clone does not allow a step to export data to be used by another step
        """
        return PixelProcessingContext(
            self.pixeldb,
            self.config.copy(),
            self.__step_data if not deep else self.__step_data.copy()
        )

    def clone_from(self, original: 'PixelProcessingContext', deep: bool = False) -> None:
        """ Clones the context from another context.
        Note that existing step data will be overwritten by data of the same key but not otherwise erased
        """
        intermidiate = original.clone(deep=deep)
        PixelProcessingContext.__init__(self, intermidiate.pixeldb, intermidiate.config)
        self.__step_data.update(intermidiate.__step_data)

    def __setitem__(self, key: str, data: Any):
        self.__step_data[key] = data
    
    def __getitem__(self, key: str) -> Any:
        return self.__step_data[key]

class PixelProcessingContextManager:
    """ Context manager for pixelsprocessor module.

    Example usage:
    ```
    root_context = PixelProcessingContext(pixeldb, config)
    contextmanager = PixelProcessingContextManager(root_context)
    with contextmanager("step1") as context:
        # Do something with context
    with contextmanager.requires("step1")("step2") as context:
        # Do something with context
    
    # This will raise an exception because step10 is not completed
    with contextmanager.requires("step10")("step3") as context:
        # Do something with context
    ```
    """

    def __init__(self, context: PixelProcessingContext) -> None:
        self._context = context
        # As steps are completed, this list will be updated with the names of the steps
        self._steps_completed: List[str] = []
        self._current_step: str = None

    def _checkout(self, step_name: str, _requires: Optional[List[str]] = None) -> PixelProcessingContext:
        """Checks out the context for a step in the processing pipeline.

        Args:
            step_name (str): The name of the step to check out.

        Returns:
            PixelProcessingContext: The context for the step.
        """
        if _requires is not None:
            for step in _requires:
                if step not in self._steps_completed:
                    raise PixelContextException(f"Attempted to check out context for step {step_name} but step {step} has not been completed.")
        if step_name in self._steps_completed:
            raise PixelContextException(f"Attempted to check out context for step {step_name} but it has already been completed. Please use unique step names.")
        if self._current_step is not None:
            raise PixelContextException(f"Attempted to check out context for step {step_name} but step {self._current_step} has not been checked in.")
        self._current_step = step_name
        return self._context.clone()

    def _checkin(self, step_name: str) -> None:
        """Checks in the context for a step in the processing pipeline.

        Args:
            step_name (str): The name of the step to check in.
        """
        if step_name != self._current_step:
            raise PixelContextException(f"Attempted to check in step {step_name} but current step is {self._current_step}")
        self._steps_completed.append(step_name)
        self._current_step = None

    def __call__(self, step_name: str) -> None:
        """Checks out the context for a step in the processing pipeline.

        Args:
            step_name (str): The name of the step to check out.
        """
        class SimpleStepContext(PixelProcessingContext):
            def __init__(self, context_manager: PixelProcessingContextManager, step_name: str) -> None:
                super().clone_from(context_manager._context)
                self.context_manager = context_manager
                self.step_name = step_name

            def __enter__(self):
                return self.context_manager._checkout(self.step_name)

            def __exit__(self, exc_type, exc_value, traceback):
                self.context_manager._checkin(self.step_name)

        return SimpleStepContext(self, step_name)

    def requires(self, *req_step_names: List[str]) -> None:
        """Checks that a step or steps has/have been completed before checking out the context for another step.

        Args:
            an unpacked list of step names (str): The names of the steps to check.
        """

        class RequirementContextManager(PixelProcessingContextManager):
            def __init__(self, context_manager: PixelProcessingContextManager, req_step_names: List[str]) -> None:
                super().__init__(context_manager._context.clone())
                self.req_step_names = req_step_names
                self._steps_completed = context_manager._steps_completed
                self._current_step = context_manager._current_step

            def __call__(self, step_name: str) -> None:
                class CompoundStepContext(PixelProcessingContext):
                    def __init__(self, context_manager: PixelProcessingContextManager, step_name: str) -> None:
                        super().clone_from(context_manager._context)
                        self.context_manager = context_manager
                        self.step_name = step_name
                        self.prerequisites = req_step_names

                    def __enter__(self):
                        return self.context_manager._checkout(self.step_name, self.prerequisites)

                    def __exit__(self, exc_type, exc_value, traceback):
                        self.context_manager._checkin(self.step_name)

                return CompoundStepContext(self, step_name)

        if isinstance(self, RequirementContextManager):
            raise PixelContextException("Attempted to nest requirements. This is not supported- Please use a single requires() call.")

        return RequirementContextManager(self, req_step_names)
