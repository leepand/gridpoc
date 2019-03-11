from random import random, choice, uniform, betavariate
from math import log, exp, expm1
import json
import redis

DEFAULT_PREFIX="MAB_EXP"
def _key(k):
    return "{0}:{1}".format(DEFAULT_PREFIX, k)

class BanditEncoder(json.JSONEncoder):
    """Json serializer for Bandits"""
    def default(self, obj):
        if isinstance(obj, Bandit):
            dict_repr = obj.__dict__
            dict_repr['bandit_type'] = obj.__class__.__name__
            return dict_repr
        return json.JSONEncoder.default(self, obj)

class BanditDecoder(json.JSONDecoder):
    """Json Marshaller for Bandits"""
    def decode(self, obj):
        dict_repr = json.loads(obj)
        for key in dict_repr.keys():
            if 'bandit_type' not in dict_repr[key].keys():
                raise TypeError("Serialized object is not a valid bandit")
            dict_repr[key] = Bandit.fromdict(dict_repr[key])
        return dict_repr



class Bandit(object):
    """The primary bandit interface.  Don't use this unless you really
    want uniform random arm selection (which defeats the whole purpose, really)
    Used as a control to test against and as an interface to define methods against.
    """        
    @classmethod
    def fromdict(cls, dict_spec):
        extra_args = dict([(key, value) for key, value in dict_spec.items() if key not in ["arms", "pulls", "reward", "values", "bandit_type", "confidence"]])

        bandit = globals()[dict_spec["bandit_type"]](**extra_args)
        bandit.arms = dict_spec["arms"]
        bandit.pulls = dict_spec["pulls"]
        bandit.reward = dict_spec["reward"]
        bandit.values = dict_spec["values"]
        bandit.confidence = dict_spec.get("confidence", [0.0] * len(bandit.arms))
        return bandit

    def __init__(self,exp_name):
        self.redis=redis.StrictRedis(db=3)
        self.exp_name=exp_name
        #pipe = self.redis.pipeline()
        self.arms_key="p:{0}:{1}:mab".format(self.exp_name, "arms")
        self.pulls_key = "p:{0}:{1}:mab".format(self.exp_name, "pulls")
        self.reward_key = "p:{0}:{1}:mab".format(self.exp_name, "reward")
        self.confidence_key="p:{0}:{1}:mab".format(self.exp_name, "confidence")
        self.values_key = "p:{0}:{1}:mab".format(self.exp_name, "values")
        
        
        if self.redis.hget(self.arms_key,'mab_exp') is not None:
            self.arms= eval(self.redis.hget(self.arms_key,'mab_exp'))
        else:
            self.arms = []

        if  self.redis.hget(self.pulls_key,'mab_exp') is not None:
            self.pulls=eval(self.redis.hget(self.pulls_key,'mab_exp'))
        else:
            self.pulls = []
        if  self.redis.hget(self.reward_key,'mab_exp') is not None:
            self.reward=eval(self.redis.hget(self.reward_key,'mab_exp'))
        else:
            self.reward = []
        if  self.redis.hget(self.values_key,'mab_exp') is not None:
            self.values=eval(self.redis.hget(self.values_key,'mab_exp'))
        else:
            self.values = []
        
        if  self.redis.hget(self.confidence_key,'mab_exp') is not None:
            self.confidence=eval(self.redis.hget(self.confidence_key,'mab_exp'))
        else:
            self.confidence = []


        
    def BanditEncoder(self):
        dict_repr = self.__dict__
        dict_repr['bandit_type'] = self.__class__.__name__
        return dict_repr
    def BanditDecoder(exp_dict):
        dict_repr = Bandit.fromdict(exp_dict)
        return dict_repr
    def add_arm(self, arm_id, value=None):

        self.arms.append(arm_id)
        self.pulls.append(0)
        self.reward.append(0.0)
        self.confidence.append(0.0)
        self.values.append(value)
        #self.arms=list(set(self.arms))
        self.redis.hset(self.confidence_key,'mab_exp',self.confidence)
        self.redis.hset(self.arms_key,'mab_exp',self.arms)
        self.redis.hset(self.pulls_key,'mab_exp',self.pulls)
        self.redis.hset(self.reward_key,'mab_exp',self.reward)
        self.redis.hset(self.values_key,'mab_exp',self.values)
        
    

    def pull_arm(self, arm_id):
        ind = self.arms.index(arm_id)
        if ind > -1:
            self.pulls[ind] += 1

        #self.redis.hset(self.confidence_key,'mab_exp',self.confidence)
        #self.redis.hset(self.arms_key,'mab_exp',self.arms)
        self.redis.hset(self.pulls_key,'mab_exp',self.pulls)
        #self.redis.hset(self.reward_key,'mab_exp',self.reward)
        #self.redis.hset(self.values_key,'mab_exp',self.values)
        
    def reward_arm(self, arm_id, reward):
        ind = self.arms.index(arm_id)
        if ind > -1:
            self.reward[ind] += reward
        self._update(ind, reward)
        
        #self.redis.hset(self.arms_key,'mab_exp',self.arms)
        #self.redis.hset(self.pulls_key,'mab_exp',self.pulls)
        self.redis.hset(self.reward_key,'mab_exp',self.reward)
        #self.redis.hset(self.values_key,'mab_exp',self.values)
        


    def _update(self, arm_index, reward):
        n = max(1, self.pulls[arm_index])
        current = self.confidence[arm_index]
        self.confidence[arm_index] = ((n - 1) / float(n)) * current + (1 / float(n)) * reward
        self.redis.hset(self.confidence_key,'mab_exp',self.confidence)
        
    def suggest_arm(self):
        """Uniform random for default bandit.
        Just uses random.choice to choose between arms
        """
        return self[random.choice(self.arms)]
    def obj_by_name(self, obj_name, slim=False):
        key="p:{0}:{1}:mab".format(self.exp_name, obj_name)
        return self.redis.hget(key,'mab_exp')#objectified
    def __getitem__(self, key):
        ind = self.arms.index(key)
        if ind > -1:
            arm = {
                    "id":self.arms[ind],
                    "pulls":self.pulls[ind],
                    "reward":self.reward[ind],
                    "value":self.values[ind]
                    }
            return arm
        else:
            raise KeyError("Arm is not found in this bandit")

    def __str__(self):
        output = '%s  ' % self.__class__.__name__
        output += '; '.join(['%s:%s' % (key, val) for key, val in self.__dict__.items()])
        return output

class EpsilonGreedyBandit(Bandit):
    """Epsilon Greedy Bandit implementation.  Aggressively favors the present winner.
    Will assign winning arm 1.0 - epsilon of the time, uniform random between arms
    epsilon % of the time.
    Will "exploit" the present winner more often with lower values of epsilon, "explore"
    other candidates more often with higher values of epsilon.
    :param epsilon: The percentage of the time to "explore" other arms, E.G a value of
                    0.1 will perform random assignment for %10 of traffic
    :type epsilon: float
    """

    def __init__(self,exp_name, epsilon=0.1):
        super(EpsilonGreedyBandit, self).__init__(exp_name)
        self.epsilon = epsilon
        self.exp_name=exp_name

    def suggest_arm(self):
        """Get an arm according to the EpsilonGreedy Strategy
        """
        random_determination = random()
        if random_determination > self.epsilon:
            key = self._ind_max()
        else:
            key = choice(self.arms)

        return self[key]

    def _ind_max(self):
        return self.arms[self.confidence.index(max(self.confidence))]

    def __str__(self):
        return Bandit.__str__(self)

    def __repr(self):
        return Bandit.__str__(self)

def all_same(items):
    return all(x == items[0] for x in items)

class NaiveStochasticBandit(Bandit):
    """A naive weighted random Bandit.  Favors the winner by giving it greater weight
    in random selection.
    Winner will eventually flatten out the losers if margin is great enough
    """

    def __init__(self,exp_name):
        super(NaiveStochasticBandit, self).__init__(exp_name)
        self.exp_name=exp_name

    def _compute_weights(self):
        weights = []
        for ind, n in enumerate(self.pulls):
            reward = self.reward[ind]
            try:
                weights.append(1.0 * (float(reward)/float(n)))
            except ZeroDivisionError:
                weights.append(1.0/len(self.arms))
        return weights

    def suggest_arm(self):
        """Get an arm according to the Naive Stochastic Strategy
        """
        weights = self._compute_weights()
        random_determination = uniform(0.0, 1.0)

        cum_weight = 0.0
        for ind, weight in enumerate(weights):
            cum_weight += weight
            if cum_weight > random_determination:
                return self[self.arms[ind]]
        return self[self.arms[0]]


class SoftmaxBandit(NaiveStochasticBandit):

    def __init__(self, exp_name,tau=0.1):
        super(SoftmaxBandit, self).__init__(exp_name)
        self.tau = tau
        self.exp_name=exp_name

    def _compute_weights(self):
        weights = []
        total_reward = sum([exp(x / self.tau) for x in self.confidence])
        for ind, n in enumerate(self.pulls):
            weights.append(exp(self.confidence[ind] / self.tau) / total_reward)
        return weights


class AnnealingSoftmaxBandit(SoftmaxBandit):

    def __init__(self,exp_name):
        super(AnnealingSoftmaxBandit, self).__init__(exp_name)
        self.tau = 1
        self.exp_name=exp_name

    def _compute_weights(self):
        t = sum(self.pulls) + 1
        self.tau = 1 / log(t +  0.0000001)

        weights = []
        total_reward = sum([exp(x / self.tau) for x in self.confidence])
        for ind, n in enumerate(self.pulls):
            weights.append(exp(self.confidence[ind] / self.tau) / total_reward)
        return weights

class ThompsonBandit(NaiveStochasticBandit):

    def __init__(self,exp_name, prior=(1.0,1.0)):
        super(ThompsonBandit, self).__init__(exp_name)
        self.prior = prior
        self.exp_name=exp_name

    def _compute_weights(self):
        sampled_theta = []
        for ind, n in enumerate(self.arms):
            dist = betavariate(self.prior[0] + self.reward[ind], self.prior[1]+self.pulls[ind]-self.reward[ind])
            sampled_theta += [dist]
        return sampled_theta

    def suggest_arm(self):
        weights = self._compute_weights()
        return self[self.arms[weights.index(max(weights))]]

    def reward_arm(self, arm_id, reward):
        if reward != 1.0:
            reward = 1.0
        super(ThompsonBandit, self).reward_arm(arm_id, reward)
        