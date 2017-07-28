# -*- utf-8 -*-

class CustomModel:
    'Used to create new model in Odoo with python code'

    def __init__(self, model, uid, db, password):
        self.model = model
        self.uid = uid
        self.db = db
        self.password = password
    
    def createModelIntoIrModel(self, model, description):
        try:
            if model is None or model[0:2] != 'x_':
                print "Unvalid model, the model must start with x_"
                return
            if description is None or description == '':
                print "Unvalid model name, this field is need"
                return
            record_id = self.model.execute_kw(self.db, self.uid, self.password, 'ir.model', 'create', [{'name': description,
                'model': model,
                'state': 'manual',
            }])
            print "Create model into ir.model successfully, id is %s" %record_id
            return record_id
        except Exception as e:
            print e
            return
    
    def createModelFields(self, parameters):
        try:
            if parameters is None or parameters == '':
                print "You must input valid list object"
                return
            result = self.model.execute_kw(self.db, self.uid, self.password, 'ir.model.fields', 'create', parameters)
            print "Create model's field %s result: %s " %(parameters, result)
            return result
        except Exception as e:
            print e
            return