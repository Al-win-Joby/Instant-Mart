from rest_framework import serializers
from .models import category ,product,productsImage,Size,Colour,Type

from users.models import Store,User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = ('id','name','description','image')   
        #exclude= ('store',)
    
    def update(self,instance,validated_data):
        instance.name= validated_data.get('name',instance.name)
        instance.description=validated_data.get('description',instance.description)
        instance.image=validated_data.get('image',instance.image)
        instance.save()
        return instance
    
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('store_name',)

class UserSerializer(serializers.ModelSerializer):
    store =StoreSerializer()
    class Meta:
        model = User
        fields = ('name','phone','store') 
        #extra_kwargs = {'password': {'write_only': True}}


class ProductsImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = productsImage
        fields = "__all__"

class ProductsSizeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('size',)

class ProductsColourSerializers(serializers.ModelSerializer):
    class Meta:
        model = Colour
        fields = ('colour',)

class ProductsTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ('type',)

class ProductSerializer(serializers.ModelSerializer):
    images =  ProductsImageSerializers(many=True, read_only=True)
    sizes =  ProductsSizeSerializers(many=True,read_only=True)
    colour=  ProductsColourSerializers(many=True,read_only=True)
    type    =ProductsTypeSerializers(many=True,read_only=True)

    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True         
    )

    Size = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,  
        required =False

    ) 

    Colour = serializers.ListField( 
        child=serializers.CharField(), 
        write_only=True,  
        required =False,
        

    ) 

    Type = serializers.ListField( 
        child=serializers.CharField(), 
        write_only=True,  
        required =False     

    ) 
      
    #sizes=serializers.CharField()
    class Meta:
        model = product  
        fields= ('id','name','description','MRP','SellingPrice','stock',
                 'category','store','uploaded_images','images','Size'
                 ,'sizes','Colour','colour','Type','type')       

        #fields= '__all__'    
        #exclude=('slug',)  

    def update(self,instance,validated_data):
        print("putilu")
        
        instance.name =  validated_data.get('name',instance.name)
        instance.description =  validated_data.get('description',instance.description)
        instance.stock = validated_data.get('stock',instance.stock)
        instance.MRP = validated_data.get('MRP',instance.MRP)
        instance.SellingPrice = validated_data.get('SellingPrice',instance.SellingPrice)

        instance.save()
        return instance


    def create(self, validated_data):
       
        uploaded_images = validated_data.pop("uploaded_images")
        
        if 'Size' in validated_data:
            sizes1 = validated_data.pop('Size')   
            sizes=sizes1[0]

        if 'Colour' in validated_data:
            colours1 = validated_data.pop('Colour')   
            colours=colours1[0]
            

        if 'Type' in validated_data:
            type1=validated_data.pop('Type')   
            type=type1[0]

        products1 = product.objects.create(**validated_data) 
        
        try:  
            sizes 
            print("sized")
                            
            Size.objects.create(products=products1,size=sizes)
        except :
            pass 

        try:  
            type 
            print("type")
                            
            Type.objects.create(products=products1,type=type)
        except :
            pass 

        try:  
            colours 
            print("colours")
                            
            Colour.objects.create(products=products1,colour=colours)
        except :
            pass 

        for image in uploaded_images:
            productsImage.objects.create(products=products1, image=image)
        return products1
    

    def validate_stock(self, value): 
        if value<0:
            raise serializers.ValidationError("Stock should be a positive integer")
        else:
            return value    



    def validate(self, data):
        if data['MRP']<0:
            raise serializers.ValidationError("Stock should be a positive integer")

        if data['SellingPrice']<0:
            raise serializers.ValidationError("Stock should be a positive integer")
        
        if 'uploaded_images' not in data:            
            raise serializers.ValidationError("Image?")
        
        return data  