#!/usr/bin/env python

# Copyright 2024 The HuggingFace Inc. team. All rights reserved.
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

from __future__ import annotations

import gymnasium as gym
import mujoco
import mujoco.viewer


class PassiveViewerWrapper(gym.Wrapper):
    """Gym wrapper that opens a passive MuJoCo viewer automatically.

    The wrapper starts a MuJoCo viewer in passive mode as soon as the
    environment is created so the user no longer needs to use
    ``mujoco.viewer.launch_passive`` or any context–manager boiler-plate.

    The viewer is kept in sync after every ``reset`` and ``step`` call and is
    closed automatically when the environment itself is closed or deleted.
    """

    def __init__(
        self,
        env: gym.Env,
        *,
        show_left_ui: bool = False,
        show_right_ui: bool = False,
    ) -> None:
        super().__init__(env)

        # Launch the interactive viewer.  We expose *model* and *data* from the
        # *unwrapped* environment to make sure we operate on the base MuJoCo
        # objects even if other wrappers have been applied before this one.
        self._viewer = mujoco.viewer.launch_passive(
            env.unwrapped.model,
            env.unwrapped.data,
            show_left_ui=show_left_ui,
            show_right_ui=show_right_ui,
        )

        # Make sure the first frame is rendered.
        self._viewer.sync()

    # ---------------------------------------------------------------------
    # Gym API overrides

    def reset(self, **kwargs):  # type: ignore[override]
        observation, info = self.env.reset(**kwargs)
        self._viewer.sync()
        return observation, info

    def step(self, action):  # type: ignore[override]
        observation, reward, terminated, truncated, info = self.env.step(action)
        self._viewer.sync()
        return observation, reward, terminated, truncated, info

    def close(self) -> None:  # type: ignore[override]
        # Close the viewer first to free the OpenGL context.
        try:
            self._viewer.close()
        finally:
            # Always forward the close call even if the viewer is already shut
            # down so resources held by the underlying environment are freed.
            self.env.close()

    def __del__(self):
        # "close" may raise if called during interpreter shutdown; guard just
        # in case.
        if hasattr(self, "_viewer"):
            try:  # noqa: SIM105
                self._viewer.close()
            except Exception:  # pragma: no cover
                pass
