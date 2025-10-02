import importlib
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Union

from ingenious.config.main_settings import IngeniousSettings
from ingenious.models.config import Config, FileStorageContainer


class IFileStorage(ABC):
    """Abstract interface for file storage implementations.

    Attributes:
        config: Ingenious configuration settings
        fs_config: File storage container configuration
    """

    def __init__(self, config: Union[Config, IngeniousSettings], fs_config: FileStorageContainer):
        """Initialize file storage interface.

        Args:
            config: Ingenious configuration settings
            fs_config: File storage container configuration
        """
        self.config: Union[Config, IngeniousSettings] = config
        self.fs_config: FileStorageContainer = fs_config

    @abstractmethod
    async def write_file(self, contents: str, file_name: str, file_path: str) -> str:
        """Write a file to the file storage.

        Args:
            contents: File contents to write
            file_name: Name of the file
            file_path: Path where the file should be written

        Returns:
            Path to the written file
        """
        pass

    @abstractmethod
    async def read_file(self, file_name: str, file_path: str) -> str:
        """Read a file from the file storage.

        Args:
            file_name: Name of the file to read
            file_path: Path where the file is located

        Returns:
            File contents as string
        """
        pass

    @abstractmethod
    async def delete_file(self, file_name: str, file_path: str) -> str:
        """Delete a file from the file storage.

        Args:
            file_name: Name of the file to delete
            file_path: Path where the file is located

        Returns:
            Confirmation message or path of deleted file
        """
        pass

    @abstractmethod
    async def list_files(self, file_path: str) -> List[str]:
        """List files in the file storage.

        Args:
            file_path: Path to list files from

        Returns:
            List of file names
        """
        pass

    @abstractmethod
    async def list_directories(self, file_path: str) -> List[str]:
        """List directories in the file storage.

        Args:
            file_path: Path to list directories from

        Returns:
            List of directory names
        """
        pass

    @abstractmethod
    async def check_if_file_exists(self, file_path: str, file_name: str) -> bool:
        """Check if a file exists in the file storage.

        Args:
            file_path: Path where the file should be located
            file_name: Name of the file to check

        Returns:
            True if file exists, False otherwise
        """
        pass

    @abstractmethod
    async def get_base_path(self) -> str:
        """Get the base path of the file storage.

        Returns:
            Base path as string
        """
        pass


class FileStorage:
    """File storage facade with dynamic backend selection.

    Attributes:
        config: Ingenious configuration settings
        add_sub_folders: Whether to add subfolder structure
        repository: Underlying file storage implementation
    """

    def __init__(self, config: Union[Config, IngeniousSettings], Category: str = "revisions"):
        """Initialize file storage with specified category.

        Args:
            config: Ingenious configuration settings
            Category: Storage category (revisions, data, etc.)

        Raises:
            ValueError: If storage type is unsupported
        """
        self.config = config
        self.add_sub_folders = getattr(self.config.file_storage, Category).add_sub_folders

        # Get the file storage config for the specified category
        fs_config = getattr(self.config.file_storage, Category)
        storage_type = fs_config.storage_type

        # Build module name based on the category's storage type
        module_name = f"ingenious.files.{storage_type.lower()}"

        # Dynamically import the module based on the storage type
        class_name = f"{storage_type}_FileStorageRepository"

        try:
            module = importlib.import_module(module_name)
            repository_class = getattr(module, class_name)
            self.repository: IFileStorage = repository_class(
                config=self.config, fs_config=fs_config
            )

        except (ImportError, AttributeError) as e:
            raise ValueError(
                f"Unsupported File Storage client type: {module_name}.{class_name}"
            ) from e

    async def write_file(self, contents: str, file_name: str, file_path: str) -> str:
        """Write a file using the configured storage backend.

        Args:
            contents: File contents to write
            file_name: Name of the file
            file_path: Path where the file should be written

        Returns:
            Path to the written file
        """
        return await self.repository.write_file(
            contents=contents, file_name=file_name, file_path=file_path
        )

    async def get_base_path(self) -> str:
        """Get the base path of the storage backend.

        Returns:
            Base path as string
        """
        return await self.repository.get_base_path()

    async def read_file(self, file_name: str, file_path: str) -> str:
        """Read a file using the configured storage backend.

        Args:
            file_name: Name of the file to read
            file_path: Path where the file is located

        Returns:
            File contents as string
        """
        return await self.repository.read_file(file_name, file_path)

    async def delete_file(self, file_name: str, file_path: str) -> str:
        """Delete a file using the configured storage backend.

        Args:
            file_name: Name of the file to delete
            file_path: Path where the file is located

        Returns:
            Confirmation message or path of deleted file
        """
        return await self.repository.delete_file(file_name, file_path)

    async def list_files(self, file_path: str) -> List[str]:
        """List files using the configured storage backend.

        Args:
            file_path: Path to list files from

        Returns:
            List of file names
        """
        return await self.repository.list_files(file_path)

    async def list_directories(self, file_path: str) -> List[str]:
        """List directories using the configured storage backend.

        Args:
            file_path: Path to list directories from

        Returns:
            List of directory names
        """
        return await self.repository.list_directories(file_path)

    async def check_if_file_exists(self, file_path: str, file_name: str) -> bool:
        """Check if a file exists using the configured storage backend.

        Args:
            file_path: Path where the file should be located
            file_name: Name of the file to check

        Returns:
            True if file exists, False otherwise
        """
        return await self.repository.check_if_file_exists(file_path, file_name)

    async def get_prompt_template_path(self, revision_id: str | None = None) -> str:
        """Get the path for prompt templates.

        Args:
            revision_id: Optional revision identifier

        Returns:
            Path to prompt templates directory
        """
        if revision_id:
            template_path = str(Path("templates") / Path("prompts") / Path(revision_id))
        else:
            template_path = str(Path("templates") / Path("prompts"))
        return template_path

    async def get_data_path(self, revision_id: str | None = None) -> str:
        if self.add_sub_folders:
            if revision_id:
                template_path = str(Path("functional_test_outputs") / Path(revision_id))
            else:
                template_path = str(Path("functional_test_outputs"))
        else:
            template_path = ""
        return template_path

    async def get_output_path(self, revision_id: str | None = None) -> str:
        if revision_id:
            template_path = str(Path("functional_test_outputs") / Path(revision_id))
        else:
            template_path = str(Path("functional_test_outputs"))
        return template_path

    async def get_events_path(self, revision_id: str | None = None) -> str:
        if revision_id:
            template_path = str(Path("functional_test_outputs") / Path(revision_id))
        else:
            template_path = str(Path("functional_test_outputs"))
        return template_path
