

class LiquidSwapInfo:

    def __init__(self):
        self.poolId = 0
        self.poolName = ""
    
    @staticmethod
    def json_parse(json_data):
        result = LiquidSwapInfo()
        result.poolId = json_data.get_int("poolId")
        result.poolName = json_data.get_string("poolName")
        result.asset = json_data.get_object("share").convert_2_dict()["asset"]

        return result
