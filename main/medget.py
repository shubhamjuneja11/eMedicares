import infermedica_api
infermedica_api.configure(app_id='38004d4f', app_key='f0d2cfeac82933b5b67a656e8ba46eb0')
mysex = 'male'
myage = '40'
class medget:

    api = infermedica_api.get_api()
    
    def get_data(self,sex_m,age_m):
        print(" he i  am called")
        self.user_data = infermedica_api.Diagnosis(sex=sex_m, age=age_m)
        print(self.user_data)
        print("yup i existttttttttttttttttttttttttt")
        global mysex,myage
        mysex = sex_m
        myage = age_m
        print(myage)



    def add_symptoms(self, ids,request):
        print("shit happens hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        age = request.session['age']
        sex = request.session['sex']
        self.get_data(sex, age)
        try:
            for i in ids:
                self.user_data.add_symptom( str(i[str(u'id')]), str(i[str(u'status')]))
            print("i am fine")
        except:
            print("exception")
        #absent status add

    def search_symptoms(self, symptoms_str):
        search_res = []
        #global api
        #j=0
        for i in symptoms_str:
            res = self.api.search(i)

            #j = 0
            for k in res:
                res_p = {}
                res_p['id'] = str(k[str('id')])
                res_p['label'] = str(k[str('label')])
                search_res.append(res_p)



        #return self.api.search('headache')
        return search_res

    def get_question(self,request):
        try:
            age = request.session['age']
            sex = request.session['sex']
            self.get_data(sex, age)
            self.user_data = self.api.diagnosis(self.user_data)
            optn_list = []
            ques = {}
            ques['text'] = self.user_data.question.text
            ques['option'] = []

            for i in self.user_data.question.items:
                optn = {}
                optn['id'] = i['id']
                optn['name'] = i['name']
                optn['choice'] = i['choices']

                ques['option'].append(optn)
            print(ques)
            return ques
        except:
            print("exception occur here")
            print(mysex)
            print(myage)
            temp=vars(self)
            for i in temp:
                print(i)
        #return optn_list

        #return self.user_data.question.items

    def check_risk(self, ):
        try:
            if self.user_data.conditions[0]['probability'] > 0.7:
                return 1
            else:
                return 0
        except:
            return 0

    def get_result(self, ):
        result = {}
        result['id'] = str(self.user_data.conditions[0][str('id')])
        result['name'] = str(self.user_data.conditions[0][str('name')])
        result['prob'] = str(self.user_data.conditions[0]['probability'])
        k = self.api.condition_details(result['id']).__dict__
        result['hint'] = str(k[str('extras')][str('hint')])
        result['severity'] = str(k[str('severity')])
        result['prevalence'] = str(k[str('prevalence')])
        result['acuteness'] = str(k[str('acuteness')])
        return result
        #return self.user_data.conditions[0]