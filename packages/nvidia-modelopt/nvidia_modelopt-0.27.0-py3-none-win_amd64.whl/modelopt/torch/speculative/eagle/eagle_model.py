# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Eagle model to support eagle decoding."""

from modelopt.torch.opt.dynamic import DynamicModule


class EagleModel(DynamicModule):
    """Base Eagle Model."""

    def _setup(self):
        self._register_temp_attribute("eagle_num_layers", 0)
        self._register_temp_attribute("eagle_module", None)

    def modify(self, eagle_num_layers, use_input_layernorm_in_first_layer, use_last_layernorm):
        """Base Eagle Model modify function. Child class should implement the details."""
        self.eagle_num_layers = eagle_num_layers
        self.use_input_layernorm_in_first_layer = use_input_layernorm_in_first_layer
        self.use_last_layernorm = use_last_layernorm
