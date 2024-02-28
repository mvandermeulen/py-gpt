#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.02.27 22:00:00                  #
# ================================================== #

from llama_index.core.indices.base import BaseIndex
from .base import BaseStore


class Storage:
    def __init__(self, window=None):
        """
        Storage handler

        :param window: Window instance
        """
        self.window = window
        self.storages = {}
        self.indexes = {}

    def get_storage(self) -> BaseStore or None:
        """
        Get current vector store provider

        :return: vector store provider instance
        """
        current = self.window.core.config.get("llama.idx.storage")
        if current is None \
                or current == "_" \
                or current not in self.storages:
            return None
        return self.storages[current]

    def register(self, name: str, storage=None):
        """
        Register vector store provider

        :param name: vector store provider name (ID)
        :param storage: vector store provider instance
        """
        storage.attach(window=self.window)
        self.storages[name] = storage

    def get_ids(self) -> list:
        """
        Return all vector store providers IDs

        :return: list of vector store providers (IDs)
        """
        return list(self.storages.keys())

    def exists(self, id: str = None) -> bool:
        """
        Check if index exists

        :param id: index name
        :return: True if exists
        """
        storage = self.get_storage()
        if storage is None:
            raise Exception('Storage engine not found!')
        return storage.exists(id)

    def create(self, id: str):
        """
        Create empty index

        :param id: index name
        """
        storage = self.get_storage()
        if storage is None:
            raise Exception('Storage engine not found!')
        storage.create(id)

    def get(self, id: str, service_context=None) -> BaseIndex:
        """
        Get index instance

        :param id: index name
        :param service_context: service context
        :return: index instance
        """
        storage = self.get_storage()
        if storage is None:
            raise Exception('Storage engine not found!')
        return storage.get(
            id=id,
            service_context=service_context,
        )

    def store(self, id: str, index: BaseIndex = None):
        """
        Store index

        :param id: index name
        :param index: index instance
        """
        storage = self.get_storage()
        if storage is None:
            raise Exception('Storage engine not found!')
        storage.store(
            id=id,
            index=index,
        )

    def remove(self, id: str) -> bool:
        """
        Clear index only

        :param id: index name
        :return: True if success
        """
        storage = self.get_storage()
        if storage is None:
            raise Exception('Storage engine not found!')
        return storage.remove(id)

    def truncate(self, id: str) -> bool:
        """
        Truncate and clear index

        :param id: index name
        :return: True if success
        """
        storage = self.get_storage()
        if storage is None:
            raise Exception('Storage engine not found!')
        return storage.truncate(id)

    def remove_document(self, id: str, doc_id: str) -> bool:
        """
        Remove document from index

        :param id: index name
        :param doc_id: document ID
        :return: True if success
        """
        storage = self.get_storage()
        if storage is None:
            raise Exception('Storage engine not found!')
        return storage.remove_document(
            id=id,
            doc_id=doc_id,
        )
