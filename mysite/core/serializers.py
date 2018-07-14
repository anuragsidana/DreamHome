from rest_framework import serializers
from .models import Profile,Customer
from django.contrib.auth.models import User





class CustomerSerializers(serializers.ModelSerializer):
    agent = serializers.ReadOnlyField(source='agent.username')
    class Meta:
        model=Customer
        fields=('agent','first_name','last_name')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('username','first_name','email','password')



class UserUpdateSerialier(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}
    )
    class Meta:
        model = User
        fields = ('pk', 'username', 'password')

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance


class ExecutiveSerializers(serializers.ModelSerializer):

    customer_set=serializers.StringRelatedField(many=True,read_only=True)
    user=UserSerializer(required=True)

    class Meta:
        model=Profile
        fields=('user','bio','location','birth_date','is_admin','customer_set')

    def create(self, validated_data):
       # import pdb;pdb.set_trace()
        """
              Overriding the default create method of the Model serializer.
              :param validated_data: data containing all the details of profile
              :return: returns a successfully created profile record
              """
        user_data=validated_data.pop('user')
        user1=User.objects.create(**user_data)
        #user=UserSerializer.create(UserSerializer(),validated_data=user_data)
        user1.profile.bio=validated_data.pop('bio')
        user1.profile.location=validated_data.pop('location')
        user1.profile.birth_date=validated_data.pop('birth_date')
        user1.profile.is_admin==validated_data.pop('is_admin')
        user1.profile.save()

        # profile,created=Profile.objects.create(user=user1,**validated_data)

        return user1.profile



class ChangePasswordSerializer(serializers.Serializer):
    old_password=serializers.CharField(required=True,help_text="Leave Empty If you are an admin ")
    new_password=serializers.CharField(required=True)







