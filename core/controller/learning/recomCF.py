from Arthur.core.controller.learning.cf_recommender.recommender import Recommender

class couponRecommendation(object):
    """Real time updating recommendation profile
    """
    cf = None
    cf_settings = {
    # redis
    'expire': 3600 * 24 * 30,
    'redis': {
        'host': 'localhost',
        'port': 6379,
        'db': 0
    },
    # recommendation engine settings
    'recommendation_count': 10,
    'recommendation': {
        'update_interval_sec': 600,
        'search_depth': 100,
        'max_history': 10000,
    },
    }
    def __init__(self,model_db=None):
        if model_db is not None:
            self.cf_settings['redis']['db']=model_db
        self.cf = Recommender(self.cf_settings)

    def like(self, user_id, coupon_ids):
        """
        :param player_id: str
        :param guild_ids: list of int
        """
        for coupon_id in coupon_ids:
            self.cf.register(coupon_id)
        self.cf.like(user_id, coupon_ids,realtime_update=True)

    def gets(self, coupon_id, topk=5):
        return self.cf.get(coupon_id, count=topk)
    def update_all(self):
        self.cf.update_all()
    

def recom_train(model_id,user_id,coupon_ids):
    cf=couponRecommendation(model_db=model_id)
    cf.like(user_id,coupon_ids)
    return {"status_code": 200}

def recom_predict(coupon_id,topk):
    cf=couponRecommendation(model_db=model_id)
    return cf.gets(coupon_id,topk)