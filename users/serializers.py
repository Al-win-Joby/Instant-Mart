from rest_framework import serializers
from .models import User, Store , Admin
from django.contrib.auth import authenticate


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ('user')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email','password', 'phone','location')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self,validated_data):
        password= validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data) 
        #print(instance['is_user'])
        if password is not None:
            instance.set_password(password)

        instance.save()            
        return instance   
    

    def validate(self, data):
        print("validatte")
        if 'location' not in data:
            raise serializers.ValidationError("Please provide location")
        else:
            return data
        
class AdminRegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    
    class Meta:
        model = Admin
        fields = '__all__' 
        #fields = ('user')
        extra_kwargs = {'password': {'write_only': True},} 

    def create(self, validated_data, *args, **kwargs):
        #print(validated_data)
        user_data=validated_data.pop('user')
        print(user_data)            
        password=user_data['password']

        user_data['is_admin']=True
        user_data['is_user']=False

        user=UserSerializer.create(UserSerializer(),validated_data=user_data)

        user.set_password(password)     
        user.save()                         
        print(password)
        individual = Admin.objects.create(user=user)
        return individual



class StoreRegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    
    class Meta:
        model  =Store
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True},}

    def create(self,validated_data,*args,**kwargs):
        print(validated_data)
        user_data=validated_data.pop('user')        
        
        password= user_data['password']             
        
        
        user_data['is_store']=True
        user_data['is_user']=False

        user=UserSerializer.create(UserSerializer(),validated_data=user_data)
        user.set_password(password)
        #user['is_store']=True
        user.save() 
        Storex = Store.objects.create(user=user,store_name=validated_data.pop('store_name'))
        return Storex

















# from rest_framework import serializers
# from .models import User, Individual, Company
# from django.contrib.auth import authenticate

# class IndividualSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Individual
#         fields = ('user', 'email_address')

# class CompanySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Company
#         fields = ('user', 'email_address', 'company_name')

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'password', 'is_individual', 'is_company')
#         extra_kwargs = {'password': {'write_only': True}}


# class IndividualRegisterSerializer(serializers.ModelSerializer):
#     user = UserSerializer(required=True)
    
#     class Meta:
#         model = Individual
#         fields = ('user', 'email_address')
#         extra_kwargs = {'password': {'write_only': True}, 'username': {'write_only': True}}

#     def create(self, validated_data, *args, **kwargs):
#         #print(validated_data)
#         user_data=validated_data.pop('user')
#         print(user_data)
#         password=user_data['password']

#         user=UserSerializer.create(UserSerializer(),validated_data=user_data)
#         user.set_password(password)
#         user.save()
#         print(password)
#         #user = User.objects.create_user(validated_data['user']['username'], validated_data['email_address'], validated_data['user']['password'])
#         individual = Individual.objects.create(user=user, email_address=validated_data.pop('email_address'))
#         return individual


# class CompanyRegisterSerializer(serializers.ModelSerializer):
#     user = UserSerializer(required=True)

#     class Meta:
#         model = Company
#         fields = ('user', 'company_name', 'email_address')
#         extra_kwargs = {'password': {'write_only': True}, 'username': {'write_only': True}}

#     def create(self, validated_data, *args, **kwargs):
#         user = User.objects.create_user(validated_data['user']['username'], validated_data['email_address'],
#                                         validated_data['user']['password'])
#         company = Company.objects.create(user=user, email_address=validated_data.pop('email_address'), company_name=validated_data.pop('company_name'))
#         return company

# class IndividualLoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()
#     class Meta:
#         fields = ['username','password','is_individual','is_company']
#         extra_kwargs = {'is_individual': {'required': False},
#                         'is_company': {'required': False}}

#     def validate(self,data):
#         print(data)
#         individual = authenticate(**data)
#         print(individual)
#         if individual is not None:
#             return individual
#         raise serializers.ValidationError("Incorrect Credentials")






