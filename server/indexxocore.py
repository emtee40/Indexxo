"""Core indexer functionality"""
import asyncio
import logging
import os
from pathlib import Path

from peewee import *

# Database object must be declared like this for dynamic database
# file support. Prepare database file before using it.
db = SqliteDatabase(None)


class BaseModel(Model):
    """This is a recommended way from peewee documentation"""
    class Meta:
        database = db


class FileObjectBase(BaseModel):
    """Represents one file/folder/space as a row in database"""

    full_path = TextField(primary_key=True)
    """Full path to this file/folder (Formatted as provided by pathlib)"""
    full_name = TextField()
    """Full file name with extension, without path"""
    name = TextField()
    """File name without extension"""
    extension = TextField(null=True)
    """File extension. Can be None/null for folders"""
    size = IntegerField()
    """Size of this file/folder in bytes"""

    type = TextField()
    """
    File/folder type. Types are:

    space — Top level folders that were that contain file and folders.
    
    folder — Contains folders and files.
    
    document — Anything that usually has some sort of text.

    image — Different picture files.

    video — Moving pictures.

    audio — Music, songs, audio files.

    archive — Archives and similar compressed files.

    program — Executable applications.

    other — Anything else.
    """
    parent = TextField(null=True)
    """Parent folder path. Can be None/null for top level folders"""
    mtime = FloatField()
    """Last modified date"""

    def to_json(self):
        """
        Convert this object into a json. Needed for WEB API.
        """
        return {
            "full_path": self.full_path,
            "full_name": self.full_name,
            "name": self.name,
            "extension": self.extension,
            "size": self.size,
            "type": self.type,
            "parent": self.parent,
            "mtime": self.mtime
        }


class Indexxo():
    """File indexer."""
    filetypes: dict = {}
    """File types dictionary. Extension (key) and file type (value)."""
    space_paths: list[Path] = []
    """List of paths that will be indexed while indexing"""
    ignore_paths: list[Path] = []
    """List of paths that will be ignored while indexing"""
    refresh_interval = 3600
    """Seconds between refreshing index"""
    loop = asyncio.new_event_loop()
    """Loop for async tasks"""

    def __init__(
        self,
        filetypes: dict,
        space_paths: list[Path],
        ignore_paths: list[Path],
        refresh_interval: int
    ):
        """
        Initialize Indexer

        Args:
            filetypes (dict): Key-value pair of extensions and associated types.
            space_paths (list[Path]): Paths that will be indexed right after indexer start up.
            ignore_paths (list[Path]): Paths that will not be indexed.
            refresh_interval (int): Amount of seconds between successful index refreshes.
        """
        self.setup_database()
        self.filetypes = filetypes
        self.space_paths = space_paths
        self.ignore_paths = ignore_paths
        self.refresh_interval = refresh_interval

    def setup_database(self):
        """
        Connects to database, creates tables if needed and clears them.
        """
        db.init("database.sqlite")
        db.connect()
        # This will not fail even if table already exists.
        db.create_tables([FileObjectBase])
        FileObjectBase.delete().execute()

    def start_indexing(self):
        """
        Start indexer loop. Refreshes index periodically.
        """
        async def looper():
            while True:
                logging.info("REFRESHING THE INDEX")
                FileObjectBase.delete().execute()

                all_spaces = self.space_paths.copy()
                for space in all_spaces:
                    await self._discover(space)

                await asyncio.sleep(self.refresh_interval)
                logging.info("REFRESH SUCCESSFUL")

        self.loop.run_until_complete(looper())

    async def add_space(self, path: Path):
        """
        Add specified path to list of indexed paths.
        If space was added while refreshing the index, this space will
        be indexed concurrently.
        """
        await self._discover(path)
        self.space_paths.append(path)

    def get_spaces(self) -> list[FileObjectBase]:
        """
        Get list of all row from database with type 'space'.

        Returns:
            list[FileObjectBase]: List of spaces (indexed top-level folder)
        """
        return (FileObjectBase.select().where(
            FileObjectBase.type == "space"
        ))

    def get_content(self, path: Path) -> tuple[list[FileObjectBase], FileObjectBase | None]:
        """
        Get content of the specified folder. IF folder doesn't exist, will return same as if 
        the folder was empty.

        Args:
            path (Path): Folder full path.

        Returns:
            tuple[list[FileObjectBase], FileObjectBase | None]: Returns multiple things: list 
            of children files/folders, parent object. Folder can be empty and parent folder is 
            None for top-level folders and spaces.
        """
        content: list[FileObjectBase] = (FileObjectBase.select().where(
            FileObjectBase.parent == path
        ))

        # Need to explicitly set empty list if folder is empty.
        if content.count() == 0:
            content = []

        parent: FileObjectBase | None = (FileObjectBase.get_or_none(
            FileObjectBase.full_path == path.parent
        ))

        return content, parent

    def find_files(self, query: str) -> list[FileObjectBase]:
        """Find file or folder with the same full name.

        Args:
            query (str): String to match.

        Returns:
            list[FileObjectBase]: List of matches.
        """
        query = query.lower()
        search_res: list[FileObjectBase] = (FileObjectBase.select().where(
            # No need to lower in database
            (FileObjectBase.full_name.contains(query))
        ))
        return search_res

    async def _discover(self, path: Path):
        """Indexes folder and adds it's file/folders to index.

        Args:
            path (Path): Folder full path.
        """
        all_files: list[dict] = []
        # Storing folder sizes like this for performance.
        folder_sizes: dict[Path] = {}
        for directory, folders, files in os.walk(path, topdown=False):
            directory = Path(directory)
            # Ignoring if needed
            if directory in self.ignore_paths:
                continue

            sizes = 0

            for file in files:
                file_path = directory / Path(file)
                # Ignoring if needed
                if file_path in self.ignore_paths:
                    continue

                full_name = file_path.name
                name, ext = os.path.splitext(file)
                type = self._get_file_type(ext[1:])
                size = file_path.stat().st_size
                parent = str(file_path.parent)
                mtime = file_path.stat().st_mtime

                sizes += size

                all_files.append(
                    {
                        "full_path": file_path,
                        "full_name": full_name,
                        "name": name,
                        "extension": ext,
                        "type": type,
                        "size": size,
                        "parent": parent,
                        "mtime": mtime
                    }
                )

            # Getting sizes of children folders
            for folder in folders:
                full_folder_path = directory / Path(folder)
                # Ignoring if needed
                if full_folder_path in self.ignore_paths:
                    continue

                sizes += folder_sizes[full_folder_path]

            # Adding directory
            all_files.append(
                {
                    "full_path": directory,
                    "full_name": os.path.basename(directory),
                    "name": os.path.basename(directory),
                    "extension": None,
                    "type": "folder",
                    # We calculate ignored files too (probably will be changed)
                    "size": sizes,
                    "parent": directory.parent,
                    "mtime": directory.stat().st_mtime
                }
            )
            folder_sizes.update({directory: sizes})

        # Can be 0 for empty folders.
        if len(all_files) > 1:
            # Last element is always the top directory, i.e. space
            space = all_files[-1]
            space["type"] = "space"
            space["parent"] = None

        # Bigger chunk sizes crash sqlite
        for batch in chunked(all_files, 500):
            FileObjectBase.insert_many(batch).execute()

    def _get_file_type(self, ext: str) -> str:
        """Get file type by it's extension.

        Args:
            ext (str): Extension

        Returns:
            str: File type.
        """
        try:
            return self.filetypes[ext]
        except KeyError:
            return "other"
