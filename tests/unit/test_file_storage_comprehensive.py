"""Comprehensive tests for file storage functionality.

Tests cover local and Azure file storage, including read/write operations,
error handling, and path management with mocked external services.
"""

import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

import pytest

from ingenious.files.files_repository import FileStorage, IFileStorage


class TestIFileStorageInterface:
    """Test the abstract file storage interface."""

    def test_interface_defines_required_methods(self):
        """Test that IFileStorage defines all required abstract methods."""
        required_methods = [
            "write_file",
            "read_file",
            "delete_file",
            "list_files",
            "list_directories",
            "check_if_file_exists",
            "get_base_path",
        ]

        for method in required_methods:
            assert hasattr(IFileStorage, method), f"Missing method: {method}"

    def test_cannot_instantiate_abstract_class(self):
        """Test that IFileStorage cannot be instantiated directly."""
        with pytest.raises(TypeError):
            IFileStorage(Mock(), Mock())


class TestFileStorageInitialization:
    """Test FileStorage initialization and backend loading."""

    def test_initialization_loads_local_storage(self):
        """Test that initialization loads local storage backend."""
        mock_config = Mock()
        mock_fs_config = Mock()
        mock_fs_config.storage_type = "local"
        mock_fs_config.add_sub_folders = True
        mock_config.file_storage.revisions = mock_fs_config

        with patch("ingenious.files.files_repository.importlib.import_module") as mock_import:
            mock_module = Mock()
            mock_repo_class = Mock()
            mock_repo_instance = Mock()
            mock_repo_class.return_value = mock_repo_instance
            mock_module.local_FileStorageRepository = mock_repo_class
            mock_import.return_value = mock_module

            storage = FileStorage(config=mock_config, Category="revisions")

            mock_import.assert_called_once_with("ingenious.files.local")
            assert storage.repository == mock_repo_instance

    def test_initialization_raises_on_unsupported_storage_type(self):
        """Test that ValueError is raised for unsupported storage types."""
        mock_config = Mock()
        mock_fs_config = Mock()
        mock_fs_config.storage_type = "unsupported_storage"
        mock_fs_config.add_sub_folders = True
        mock_config.file_storage.revisions = mock_fs_config

        with patch("ingenious.files.files_repository.importlib.import_module") as mock_import:
            mock_import.side_effect = ImportError("No module found")

            with pytest.raises(ValueError, match="Unsupported File Storage client type"):
                FileStorage(config=mock_config, Category="revisions")

    def test_initialization_raises_on_missing_class(self):
        """Test that ValueError is raised when class is not found in module."""
        mock_config = Mock()
        mock_fs_config = Mock()
        mock_fs_config.storage_type = "local"
        mock_fs_config.add_sub_folders = True
        mock_config.file_storage.revisions = mock_fs_config

        with patch("ingenious.files.files_repository.importlib.import_module") as mock_import:
            mock_module = Mock(spec=[])  # Module without the expected class
            mock_import.return_value = mock_module

            with pytest.raises(ValueError, match="Unsupported File Storage client type"):
                FileStorage(config=mock_config, Category="revisions")


class TestFileStorageOperations:
    """Test FileStorage file operations."""

    @pytest.fixture
    def mock_file_storage(self):
        """Create a mock file storage for testing."""
        mock_config = Mock()
        mock_fs_config = Mock()
        mock_fs_config.storage_type = "local"
        mock_fs_config.add_sub_folders = True
        mock_config.file_storage.revisions = mock_fs_config

        with patch("ingenious.files.files_repository.importlib.import_module") as mock_import:
            mock_module = Mock()
            mock_repo = AsyncMock()
            mock_module.local_FileStorageRepository = Mock(return_value=mock_repo)
            mock_import.return_value = mock_module

            storage = FileStorage(config=mock_config, Category="revisions")
            return storage

    @pytest.mark.asyncio
    async def test_write_file_delegates_to_repository(self, mock_file_storage):
        """Test that write_file delegates to the repository."""
        mock_file_storage.repository.write_file = AsyncMock(return_value="success")

        result = await mock_file_storage.write_file(
            contents="test content",
            file_name="test.txt",
            file_path="/path/to",
        )

        mock_file_storage.repository.write_file.assert_called_once_with(
            contents="test content",
            file_name="test.txt",
            file_path="/path/to",
        )
        assert result == "success"

    @pytest.mark.asyncio
    async def test_read_file_delegates_to_repository(self, mock_file_storage):
        """Test that read_file delegates to the repository."""
        mock_file_storage.repository.read_file = AsyncMock(return_value="file content")

        result = await mock_file_storage.read_file(
            file_name="test.txt",
            file_path="/path/to",
        )

        mock_file_storage.repository.read_file.assert_called_once_with("test.txt", "/path/to")
        assert result == "file content"

    @pytest.mark.asyncio
    async def test_delete_file_delegates_to_repository(self, mock_file_storage):
        """Test that delete_file delegates to the repository."""
        mock_file_storage.repository.delete_file = AsyncMock(return_value="deleted")

        result = await mock_file_storage.delete_file(
            file_name="test.txt",
            file_path="/path/to",
        )

        mock_file_storage.repository.delete_file.assert_called_once_with("test.txt", "/path/to")
        assert result == "deleted"

    @pytest.mark.asyncio
    async def test_list_files_delegates_to_repository(self, mock_file_storage):
        """Test that list_files delegates to the repository."""
        mock_file_storage.repository.list_files = AsyncMock(return_value="file1.txt,file2.txt")

        result = await mock_file_storage.list_files(file_path="/path/to")

        mock_file_storage.repository.list_files.assert_called_once_with("/path/to")
        assert result == "file1.txt,file2.txt"

    @pytest.mark.asyncio
    async def test_list_directories_delegates_to_repository(self, mock_file_storage):
        """Test that list_directories delegates to the repository."""
        mock_file_storage.repository.list_directories = AsyncMock(return_value=["dir1", "dir2"])

        result = await mock_file_storage.list_directories(file_path="/path/to")

        mock_file_storage.repository.list_directories.assert_called_once_with("/path/to")
        assert result == ["dir1", "dir2"]

    @pytest.mark.asyncio
    async def test_check_if_file_exists_delegates_to_repository(self, mock_file_storage):
        """Test that check_if_file_exists delegates to the repository."""
        mock_file_storage.repository.check_if_file_exists = AsyncMock(return_value=True)

        result = await mock_file_storage.check_if_file_exists(
            file_path="/path/to",
            file_name="test.txt",
        )

        mock_file_storage.repository.check_if_file_exists.assert_called_once_with(
            "/path/to", "test.txt"
        )
        assert result is True

    @pytest.mark.asyncio
    async def test_get_base_path_delegates_to_repository(self, mock_file_storage):
        """Test that get_base_path delegates to the repository."""
        mock_file_storage.repository.get_base_path = AsyncMock(return_value="/base/path")

        result = await mock_file_storage.get_base_path()

        mock_file_storage.repository.get_base_path.assert_called_once()
        assert result == "/base/path"


class TestFileStoragePathHelpers:
    """Test FileStorage path helper methods."""

    @pytest.fixture
    def mock_file_storage(self):
        """Create a mock file storage for testing."""
        mock_config = Mock()
        mock_fs_config = Mock()
        mock_fs_config.storage_type = "local"
        mock_fs_config.add_sub_folders = True
        mock_config.file_storage.revisions = mock_fs_config

        with patch("ingenious.files.files_repository.importlib.import_module") as mock_import:
            mock_module = Mock()
            mock_repo = AsyncMock()
            mock_module.local_FileStorageRepository = Mock(return_value=mock_repo)
            mock_import.return_value = mock_module

            storage = FileStorage(config=mock_config, Category="revisions")
            return storage

    @pytest.mark.asyncio
    async def test_get_prompt_template_path_without_revision(self, mock_file_storage):
        """Test getting prompt template path without revision ID."""
        result = await mock_file_storage.get_prompt_template_path()

        expected = str(Path("templates") / Path("prompts"))
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_prompt_template_path_with_revision(self, mock_file_storage):
        """Test getting prompt template path with revision ID."""
        result = await mock_file_storage.get_prompt_template_path(revision_id="rev-123")

        expected = str(Path("templates") / Path("prompts") / Path("rev-123"))
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_data_path_with_sub_folders(self, mock_file_storage):
        """Test getting data path with sub-folders enabled."""
        mock_file_storage.add_sub_folders = True

        result = await mock_file_storage.get_data_path(revision_id="rev-123")

        expected = str(Path("functional_test_outputs") / Path("rev-123"))
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_data_path_without_sub_folders(self, mock_file_storage):
        """Test getting data path with sub-folders disabled."""
        mock_file_storage.add_sub_folders = False

        result = await mock_file_storage.get_data_path(revision_id="rev-123")

        assert result == ""

    @pytest.mark.asyncio
    async def test_get_output_path_without_revision(self, mock_file_storage):
        """Test getting output path without revision ID."""
        result = await mock_file_storage.get_output_path()

        expected = str(Path("functional_test_outputs"))
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_output_path_with_revision(self, mock_file_storage):
        """Test getting output path with revision ID."""
        result = await mock_file_storage.get_output_path(revision_id="rev-456")

        expected = str(Path("functional_test_outputs") / Path("rev-456"))
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_events_path_without_revision(self, mock_file_storage):
        """Test getting events path without revision ID."""
        result = await mock_file_storage.get_events_path()

        expected = str(Path("functional_test_outputs"))
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_events_path_with_revision(self, mock_file_storage):
        """Test getting events path with revision ID."""
        result = await mock_file_storage.get_events_path(revision_id="rev-789")

        expected = str(Path("functional_test_outputs") / Path("rev-789"))
        assert result == expected


class TestLocalFileStorageIntegration:
    """Integration tests for local file storage (using temp directories)."""

    @pytest.fixture
    def temp_storage_dir(self):
        """Create a temporary directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir

    @pytest.mark.asyncio
    async def test_local_storage_write_and_read(self, temp_storage_dir):
        """Test writing and reading files with local storage."""
        # This test uses mocking since we're testing the abstraction layer
        mock_config = Mock()
        mock_fs_config = Mock()
        mock_fs_config.storage_type = "local"
        mock_fs_config.add_sub_folders = True
        mock_fs_config.base_path = temp_storage_dir
        mock_config.file_storage.revisions = mock_fs_config

        with patch("ingenious.files.files_repository.importlib.import_module") as mock_import:
            mock_module = Mock()
            mock_repo = AsyncMock()
            mock_repo.write_file = AsyncMock(return_value="written")
            mock_repo.read_file = AsyncMock(return_value="test content")
            mock_module.local_FileStorageRepository = Mock(return_value=mock_repo)
            mock_import.return_value = mock_module

            storage = FileStorage(config=mock_config, Category="revisions")

            # Write file
            await storage.write_file(
                contents="test content",
                file_name="test.txt",
                file_path="subdir",
            )

            # Read file
            content = await storage.read_file(
                file_name="test.txt",
                file_path="subdir",
            )

            assert content == "test content"


class TestAzureFileStorageMocking:
    """Test Azure file storage with mocked Azure SDK."""

    @pytest.mark.asyncio
    async def test_azure_storage_initialization(self):
        """Test Azure storage backend initialization."""
        mock_config = Mock()
        mock_fs_config = Mock()
        mock_fs_config.storage_type = "azure"
        mock_fs_config.add_sub_folders = True
        mock_fs_config.connection_string = "DefaultEndpointsProtocol=https;..."
        mock_fs_config.container_name = "test-container"
        mock_config.file_storage.revisions = mock_fs_config

        with patch("ingenious.files.files_repository.importlib.import_module") as mock_import:
            mock_module = Mock()
            mock_repo = AsyncMock()
            mock_module.azure_FileStorageRepository = Mock(return_value=mock_repo)
            mock_import.return_value = mock_module

            storage = FileStorage(config=mock_config, Category="revisions")

            mock_import.assert_called_once_with("ingenious.files.azure")
            assert storage.repository == mock_repo

    @pytest.mark.asyncio
    async def test_azure_storage_write_file(self):
        """Test writing file to Azure storage."""
        mock_config = Mock()
        mock_fs_config = Mock()
        mock_fs_config.storage_type = "azure"
        mock_fs_config.add_sub_folders = True
        mock_config.file_storage.revisions = mock_fs_config

        with patch("ingenious.files.files_repository.importlib.import_module") as mock_import:
            mock_module = Mock()
            mock_repo = AsyncMock()
            mock_repo.write_file = AsyncMock(return_value="blob_url")
            mock_module.azure_FileStorageRepository = Mock(return_value=mock_repo)
            mock_import.return_value = mock_module

            storage = FileStorage(config=mock_config, Category="revisions")

            result = await storage.write_file(
                contents="azure content",
                file_name="azure_test.txt",
                file_path="azure/path",
            )

            mock_repo.write_file.assert_called_once_with(
                contents="azure content",
                file_name="azure_test.txt",
                file_path="azure/path",
            )
            assert result == "blob_url"

    @pytest.mark.asyncio
    async def test_azure_storage_list_files(self):
        """Test listing files from Azure storage."""
        mock_config = Mock()
        mock_fs_config = Mock()
        mock_fs_config.storage_type = "azure"
        mock_fs_config.add_sub_folders = True
        mock_config.file_storage.revisions = mock_fs_config

        with patch("ingenious.files.files_repository.importlib.import_module") as mock_import:
            mock_module = Mock()
            mock_repo = AsyncMock()
            mock_repo.list_files = AsyncMock(return_value="file1.txt,file2.txt,file3.txt")
            mock_module.azure_FileStorageRepository = Mock(return_value=mock_repo)
            mock_import.return_value = mock_module

            storage = FileStorage(config=mock_config, Category="revisions")

            result = await storage.list_files(file_path="azure/path")

            mock_repo.list_files.assert_called_once_with("azure/path")
            assert "file1.txt" in result


class TestFileStorageErrorHandling:
    """Test error handling in file storage."""

    @pytest.mark.asyncio
    async def test_write_file_error_propagation(self):
        """Test that write errors are propagated."""
        mock_config = Mock()
        mock_fs_config = Mock()
        mock_fs_config.storage_type = "local"
        mock_fs_config.add_sub_folders = True
        mock_config.file_storage.revisions = mock_fs_config

        with patch("ingenious.files.files_repository.importlib.import_module") as mock_import:
            mock_module = Mock()
            mock_repo = AsyncMock()
            mock_repo.write_file = AsyncMock(side_effect=IOError("Permission denied"))
            mock_module.local_FileStorageRepository = Mock(return_value=mock_repo)
            mock_import.return_value = mock_module

            storage = FileStorage(config=mock_config, Category="revisions")

            with pytest.raises(IOError, match="Permission denied"):
                await storage.write_file(
                    contents="test",
                    file_name="test.txt",
                    file_path="/readonly",
                )

    @pytest.mark.asyncio
    async def test_read_file_not_found_propagation(self):
        """Test that file not found errors are propagated."""
        mock_config = Mock()
        mock_fs_config = Mock()
        mock_fs_config.storage_type = "local"
        mock_fs_config.add_sub_folders = True
        mock_config.file_storage.revisions = mock_fs_config

        with patch("ingenious.files.files_repository.importlib.import_module") as mock_import:
            mock_module = Mock()
            mock_repo = AsyncMock()
            mock_repo.read_file = AsyncMock(side_effect=FileNotFoundError("File not found"))
            mock_module.local_FileStorageRepository = Mock(return_value=mock_repo)
            mock_import.return_value = mock_module

            storage = FileStorage(config=mock_config, Category="revisions")

            with pytest.raises(FileNotFoundError, match="File not found"):
                await storage.read_file(
                    file_name="nonexistent.txt",
                    file_path="/missing",
                )
