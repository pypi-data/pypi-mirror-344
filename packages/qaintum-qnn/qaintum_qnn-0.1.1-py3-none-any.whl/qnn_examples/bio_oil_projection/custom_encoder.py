# Copyright 2025 The qAIntum.ai Authors. All Rights Reserved.
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
# ==============================================================================

# qnn_examples/bio_oil_production/custom_encoder.py

import pennylane as qml

class CustomFeatureEncoder:
    """Encodes input features into quantum states."""
    def __init__(self, num_wires):
        self.num_wires = num_wires

    def encode(self, x):
        for i in range(self.num_wires):
            if i < 5:
                qml.Rotation(x[i], wires=i)
            elif i == 5:
                qml.Squeezing(x[i], 0, wires=i)
            elif i == 6:
                qml.Displacement(x[i], 0, wires=i)
            elif i == 7:
                qml.Kerr(x[i], wires=i)

