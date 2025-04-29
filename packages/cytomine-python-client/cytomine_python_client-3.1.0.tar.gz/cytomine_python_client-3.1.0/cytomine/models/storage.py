# -*- coding: utf-8 -*-

# * Copyright (c) 2009-2024. Authors: see NOTICE file.
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *      http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.

# pylint: disable=invalid-name

from typing import Any, Dict, List, Optional

from cytomine.models.collection import Collection
from cytomine.models.model import Model


class Storage(Model):
    def __init__(
        self,
        name: Optional[str] = None,
        id_user: Optional[int] = None,
        **attributes: Any,
    ) -> None:
        super().__init__()
        self.name = name
        self.user = id_user
        self.populate(attributes)


class StorageCollection(Collection):
    def __init__(
        self,
        filters: Optional[Dict[str, Any]] = None,
        max: int = 0,
        offset: int = 0,
        **parameters: Any,
    ) -> None:
        super().__init__(Storage, filters, max, offset)
        self._allowed_filters = [None]

        self.all = None
        self.set_parameters(parameters)


class UploadedFile(Model):
    # Old codes
    UPLOADED = 0
    CONVERTED = 1
    DEPLOYED = 2
    ERROR_FORMAT = 3
    ERROR_CONVERT = 4
    UNCOMPRESSED = 5
    TO_DEPLOY = 6
    # --

    DETECTING_FORMAT = 10
    ERROR_FORMAT = 11
    EXTRACTING_DATA = 20
    ERROR_EXTRACTION = 21
    CONVERTING = 30
    ERROR_CONVERSION = 31
    DEPLOYING = 40
    ERROR_DEPLOYMENT = 41
    DEPLOYED = 100
    EXTRACTED = 102
    CONVERTED = 104

    def __init__(
        self,
        original_filename: Optional[str] = None,
        filename: Optional[str] = None,
        size: Optional[int] = None,
        ext: Optional[str] = None,
        content_type: Optional[str] = None,
        id_projects: Optional[List[int]] = None,
        id_storage: Optional[int] = None,
        id_user: Optional[int] = None,
        id_image_server: Optional[int] = None,
        status: Optional[int] = None,
        id_parent: Optional[int] = None,
        **attributes: Any,
    ):
        super().__init__()
        self.originalFilename = original_filename
        self.filename = filename
        self.path = None
        self.size = size
        self.ext = ext
        self.contentType = content_type
        self.projects = id_projects
        self.storage = id_storage
        self.imageServer = id_image_server
        self.user = id_user
        self.status = status
        self.statusText = None
        self.parent = id_parent
        self.populate(attributes)

    def __str__(self) -> str:
        return f"[{self.callback_identifier}] {self.id} : {self.filename}"


class UploadedFileCollection(Collection):
    def __init__(
        self,
        filters: Optional[Dict[str, Any]] = None,
        max: int = 0,
        offset: int = 0,
        **parameters: Any,
    ) -> None:
        super().__init__(UploadedFile, filters, max, offset)
        self._allowed_filters = [None]

        self.all = None
        self.parent = None
        self.onlyRoots = None
        self.set_parameters(parameters)
