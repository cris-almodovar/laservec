# Copyright 2019 Cris Almodovar
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import grpc
from laservec.laservec_pb2_grpc import LaserGrpcApiStub
from laservec.laservec_pb2 import VectorizeRequest
import numpy as np


class LASER(object):
    def __init__(self, url: str):
        self.url = url
        self.channel = grpc.insecure_channel(url)
        self.stub = LaserGrpcApiStub(self.channel)

    def close(self):
        self.stub = None
        self.channel.close()
        self.channel = None

    def vectorize(self, text: str, lang: str=None):
        assert self.channel is not None
        assert self.stub is not None

        req = VectorizeRequest(text=text, lang=lang)
        res = self.stub.vectorize(req)
        if res:
            return res.lang, np.array(res.embedding)
        return None, None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
