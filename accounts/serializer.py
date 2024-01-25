# from .models import UserData
# from rest_framework.serializers import ModelSerializer, CharField
#
#
# class RegisterSerializer(ModelSerializer):
#     class Meta:
#         model = UserData
#         fields = ['email', 'password', 'birth_date']
#
#
# class UpdateDestroyAccount(ModelSerializer):
#     class Meta:
#         model = UserData
#         fields = ['avatar', 'first_name', 'last_name', 'username', 'email', 'phone_number', 'birth_date']
#
#     def create(self, validated_data):
#         user = UserData.objects.create_user(
#             avatar=validated_data['avatar'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name'],
#             username=validated_data['username'],
#             email=validated_data['email'],
#             phone_number=validated_data['phone_number'],
#             birth_date=validated_data['birth_date'],
#         )
#         return user
