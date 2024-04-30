#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# ******************************************************************************/

import logging
import websocket

logger = logging.getLogger(__name__)

class WebSocketHelper:
    def __init__(self, verbose):
        self.__ws = websocket.WebSocket()

        if verbose is True:
            websocket.enableTrace(verbose)

    def connect(self, url) -> None:
        self.__ws.connect(url, subprotocols=["ocpp1.6"])

        logger.debug("Connected to url {'url':'%s'}.", url)

    def disconnect(self) -> None:
        self.__ws.shutdown()

        logger.debug("Disconnected!")

    def send(self, msg) -> None:
        self.__ws.send(msg)

        logger.debug("To Central-System {'msg':'%s'}.", msg)

    def receive(self) -> str:
        msg = self.__ws.recv()

        logger.debug("From Central-System {'msg':'%s'}.", msg)

        return msg
