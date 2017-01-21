import logging

from alcs.agent.Agent import Agent
from alcs.environment.Environment import Environment
from .ALP import apply_alp
from .GA import apply_ga
from .RL import apply_rl
from .ACS2Utils import generate_initial_classifiers,\
    generate_match_set, generate_action_set, choose_action

logger = logging.getLogger(__name__)


class ACS2(Agent):

    def __init__(self, environment: Environment):
        super().__init__(environment)
        self.classifiers = generate_initial_classifiers()

    def evaluate(self, generations, **kwargs) -> None:
        time = 0
        perception = None
        action = None
        action_set = None
        reward = None
        previous_perception = None
        previous_action_set = None

        self.env.insert_animat()

        # Get the animat initial perception
        perception = self.env.get_animat_perception()

        for _ in range(generations):
            logger.info('\n\nGeneration [%d]', time)
            logger.info('%s', perception)

            # Reset the environment and put the animat randomly
            # inside the maze when he found the reward (next trial starts)
            if self.env.animat_has_finished():
                self.env.insert_animat()

            # Generate initial (general) classifiers if no classifier
            # are in the population.
            if len(self.classifiers) == 0:
                self.classifiers = generate_initial_classifiers()

            # Select classifiers matching the perception
            match_set = generate_match_set(self.classifiers, perception)

            # If not the beginning of the trial
            if previous_action_set is not None:  # time != 0
                logger.info("Triggering learning modules on previous "
                            "action set")
                apply_alp(self.classifiers,
                          action,
                          time,
                          previous_action_set,
                          perception,
                          previous_perception)
                apply_rl(match_set,
                         previous_action_set,
                         reward)
                apply_ga(self.classifiers,
                         previous_action_set,
                         time)

            # Remove previous action set
            previous_action_set = None

            action = choose_action(match_set)
            action_set = generate_action_set(match_set, action)

            # Execute action and obtain reward
            reward = self.env.execute_action(action)

            # Next time slot
            time += 1
            previous_perception = perception
            perception = self.env.get_animat_perception()

            # If new state was introduced
            if self.env.trial_was_successful():
                logger.info("Trial successful. Triggering learning modules")
                apply_alp(self.classifiers,
                          action,
                          time,
                          action_set,
                          perception,
                          previous_perception)
                apply_rl(match_set,
                         action_set,
                         reward)
                apply_ga(self.classifiers,
                         action_set,
                         time)

            # TODO: check this line
            previous_action_set = action_set