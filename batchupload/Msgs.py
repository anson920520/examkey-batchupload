from flask import jsonify


class ASocMessage():

    def truemsg(data):
        msg = dict(data)
        return jsonify(msg)



class Message:

    def truemsg(returnmsg,data,token=0):
        if token == 0:
            msg = {
                "code": 200,
                "msg": returnmsg,
                "data":data
            }
        else:
            msg = {
                "code": 200,
                "msg": returnmsg,
                "data": data,
                "token":token,
                "token_type":str(type(token))
            }

        return jsonify(msg)

    def errormsg(returnmsg,code=460):
        msg = {
            "code": code,
            "msg": returnmsg
        }
        return jsonify(msg)
    

