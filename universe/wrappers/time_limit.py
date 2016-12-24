import logging

from universe import pyprofile, vectorized

logger = logging.getLogger(__name__)

DEFAULT_MAX_EPISODE_SECONDS = 20 * 60.  # Default to 20 minutes if there is no explicit limit


class TimeLimit(vectorized.Wrapper):
    def _configure(self, **kwargs):
        super(TimeLimit, self)._configure(**kwargs)
        self.max_episode_seconds = self.env.spec.tags.get('wrapper_config.TimeLimit.max_episode_seconds', None)
        self.max_episode_steps = self.env.spec.tags.get('wrapper_config.TimeLimit.max_episode_steps', None)

        if self.max_episode_seconds is None and self.max_episode_steps is None:
            self.max_episode_seconds = DEFAULT_MAX_EPISODE_SECONDS

    def _step(self, action_n):
        observation_n, reward_n, done_n, info = self.env.step(action_n)
        return observation_n, reward_n, done_n, info