import json
from pathlib import Path
from typing import Callable, Optional, Union

from langchain_core.documents import Document
from langchain_community.document_loaders.base import BaseLoader


class JSONLoader(BaseLoader):
    def __init__(
        self,
        file_path: Union[str, Path],
        content_key: Optional[str] = None,
        metadata_func: Optional[Callable[[dict], dict]] = None,
    ):
        """
        Initialize the JSONLoader.

        Args:
            file_path (Union[str, Path]): The path to the JSON file.
            content_key (Optional[str]): The key to extract content from each item in the JSON data.
            metadata_func (Optional[Callable[[dict], dict]]): A function to extract metadata from each item.
        """
        self.file_path = Path(file_path).resolve()
        self._content_key = content_key
        self._metadata_func = metadata_func

    def create_documents(self, data: list[dict]) -> list[Document]:
        """
        Create a list of Document instances from the provided JSON data.

        Args:
            data (List[dict]): The JSON data to create documents from.

        Returns:
            List[Document]: A list of Document instances.
        """
        documents = []
        for item in data:
            content = self.get_content(item)
            metadata = self._metadata_func(item) if self._metadata_func else {}
            document = Document(page_content=content, metadata=metadata)
            documents.append(document)
        return documents

    def get_content(self, item: dict) -> str:
        """
        Get the content from the item.

        Args:
            item (dict): The item to extract content from.

        Returns:
            str: The extracted content.
        """
        if self._content_key:
            return item.get(self._content_key, "")

        return "\n".join([f"{key}: {value}" for key, value in item.items()])

    def load(self) -> list[Document]:
        """
        Load and return documents from the JSON file.

        Returns:
            List[Document]: A list of Document instances loaded from the JSON file.
        """
        docs = []
        with open(self.file_path, mode="r", encoding="utf-8") as json_file:
            try:
                data = json.load(json_file)
                docs = self.create_documents(data)
            except json.JSONDecodeError:
                print("Error: Invalid JSON format")
        return docs
